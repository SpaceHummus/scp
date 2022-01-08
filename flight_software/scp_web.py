# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and sett
import yaml
from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired
import logging
import time
from datetime import datetime
import led_handler
import switch_handler
import camera_handler_high_level
from telematry_handler import TelematryHandler
import os
from shutil import copyfile

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("scp_web.log"),
            logging.StreamHandler()
        ]
    )    

app = Flask(__name__)
 #Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'G2HWAV3MGfNTqsrYQg8EcMrdTimkZ724'
Bootstrap(app)

#################### Main Page #####################################################
@app.route('/')
def main_page():
    now = datetime.now()
    time_str = now.strftime("%y-%m-%d__%H_%M")
    return render_template('main.html', rpi_time=time_str)

#################### Set Google Folder Page ########################################
CONF_FILE_NAME = "scp_conf.yaml"
class ConfForm(FlaskForm):
    name = StringField('Google folder id:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/SetGoogleFolder/', methods=['GET', 'POST'])
def set_google_folder():
    form = ConfForm()
    if request.method == 'GET':
        a_yaml_file = open(CONF_FILE_NAME,'r')
        parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
        if parsed_yaml_file["folder_id"] != None:
            form.name.data = parsed_yaml_file["folder_id"]
        else:
            form.name.data = "Please enter folder ID here"

        logging.info("folder ID from file:%s",form.name.data)
        return render_template('scp_conf.html', form=form, message = "")
    else:
        logging.info("got new folder ID:%s",form.name.data)
        dict_file = {'folder_id': form.name.data}
        with open(CONF_FILE_NAME, 'w') as file:
            documents = yaml.dump(dict_file, file)
        return render_template('scp_conf.html', form=form, message = "Data saved!")
        
#################### Simple Commands ###############################################
@app.route('/StopSCPMain/')
def stop_scp_main():    
    os.system('./stop_scp_main.sh')
    return render_template('simple_commands.html', message="Running stop_scp_main.sh right now to stop logic")

@app.route('/Reboot/')
def reboot():    
    os.system('sudo reboot')
    return render_template('simple_commands.html', message="Running 'sudo reboot' right now to stop logic")
    
@app.route('/Shutdown/')
def shutdown():    
    os.system('sudo shutdown now')
    return render_template('simple_commands.html', message="Running 'sudo shutdown now' right now to stop logic")
        
#################### LED Testing ###################################################
class LEDForm(FlaskForm):
    r = StringField('Red (0-255):', validators=[DataRequired()])
    g = StringField('Green (0-255):', validators=[DataRequired()])
    b = StringField('Blue (0-255):', validators=[DataRequired()])
    fr = StringField('Far Red (0-100):', validators=[DataRequired()])
    
    force_reset = BooleanField(label='Power Cycle')
    
    submit = SubmitField('Set LEDs')
@app.route('/LEDTesting/', methods=['GET', 'POST'])
def led_testing():
    
    form = LEDForm()
    if request.method == 'GET':
        # User hadn't submitted information yet, set default values
        form.r.data = 150
        form.g.data = 210
        form.b.data = 255
        form.fr.data = 12
        
        form.force_reset.data = False
        return render_template('led_testing.html', form=form)
    
    # Stop all LEDs before starting illumination
    if form.force_reset.data == True:
        sw_handler = switch_handler.SwitchHandler()
        sw_handler.set_switch(switch_handler.SWITCH_LED_PIN, "off")
        time.sleep(1) # Add a delay to let system stabilize
        sw_handler.set_switch(switch_handler.SWITCH_LED_PIN, "on")
        time.sleep(1) # Add a delay to let system stabilize
        # led_handler.stop_LED()
    
    # Set LEDs - Shade avoidance side   
    led_handler.light_pixel(0,4,int(form.r.data),int(form.g.data),int(form.b.data))
    led_handler.light_pixel(10,14,int(form.r.data),int(form.g.data),int(form.b.data))
    led_handler.light_far_red(int(form.fr.data))
    
    # Set LEDs - Control side
    led_handler.light_pixel(5,9,int(form.r.data),int(form.g.data),int(form.b.data))
    led_handler.light_pixel(15,19,int(form.r.data),int(form.g.data),int(form.b.data))    
    
    return render_template('led_testing.html', form=form)
    
#################### Switch & A2D Testing ##########################################
class SwitchForm(FlaskForm):
    switch_LED = BooleanField(label='LEDs')
    switch_medtronic = BooleanField(label='Medtronic')
    switch_air_sensor = BooleanField(label='Air Sensor')
    
    submit = SubmitField('Set Switches')
@app.route('/SwitchesAndAnalogs/', methods=['GET', 'POST'])
def switch_and_analog_testing():
    
    form = SwitchForm()
    if request.method == 'GET':
        # User hadn't submitted information yet, set default values
        form.switch_LED.data = False
        form.switch_air_sensor.data = False
        form.switch_medtronic.data = False
    else:
        # Set switch status
        sw_handler = switch_handler.SwitchHandler()
        sw_handler.set_switch(switch_handler.SWITCH_LED_PIN, form.switch_LED.data)
        sw_handler.set_switch(switch_handler.SWITCH_AIR_SENSE_PIN, form.switch_air_sensor.data)
        sw_handler.set_switch(switch_handler.SWITCH_MEDTRONIC_PIN, form.switch_medtronic.data)
        
        time.sleep(1)
    
    # Read INA status
    tm = TelematryHandler ()
    data = tm.get_ina260_telemetry()
    
    return render_template('switch_and_analog_testing.html', form=form, 
        current_mA=data[0], voltage=data[1], power_mW=data[2])

#################### Camera Testing ################################################
class CameraForm(FlaskForm):
    camera = RadioField(label="Camera", choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    focus_distance_mm = StringField(label="Focus Distance mm")
    
    submit = SubmitField('Take a Picture')
    
@app.route('/Cameras/', methods=['GET', 'POST'])
def camera_testing():
    form = CameraForm()
    if request.method == 'GET':
        # User hadn't submitted information yet, set default values
        form.camera.data = 'A'
        form.focus_distance_mm.data = "100"
    else:    
        distance = float(form.focus_distance_mm.data)
        
        # Take an image
        cam = camera_handler_high_level.CameraHandlerHighLevel()
        file_path = cam.take_pic_all_distances(form.camera.data,[distance])
        
        # Copy to the static folder where iamge is found
        if not os.path.exists('static'):
            os.makedirs('static')
        copyfile(file_path[0][0],'static/1.jpg')
    
    return render_template('camera_testing.html', form=form)
    


#################### Main ##########################################################
if __name__ == '__main__':
    setup_logging()
    logging.info('*** Start ***')
    app.run(host='0.0.0.0', port=80)