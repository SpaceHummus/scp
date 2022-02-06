# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and sett
import yaml
from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask import request
from wtforms import StringField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired
import logging
import time
from datetime import datetime
import led_handler
import switch_handler
import camera_handler_high_level
from telematry_handler import TelematryHandler
import glob,os
from shutil import copyfile
import root_image_handler
import led_handler_high_level

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
    
# This web page deletes old logs, telemetry and images
@app.route('/DeleteExperimentFiles/')
def delete_logs_telemetry_images():  
    # Stop main file from running
    os.system('./stop_scp_main.sh')
    
    # Delete logs
    log_files = glob.glob('*.log')
    for fp in log_files:
        os.remove(fp)
    
    # Delete csvs
    csv_files = glob.glob('*.csv')
    for fp in csv_files:
        os.remove(fp)
        
    # Delete images
    image_list = glob.glob('./images/*.*')
    for fp in image_list:
        os.remove(fp)
    
    return render_template('simple_commands.html', message="Removed old logs csv and images files, please reboot Pi")
        
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
@app.route('/SwitchesAndAnalogsTesting/', methods=['GET', 'POST'])
def switch_and_analog_testing():
    
    form = SwitchForm()
    sw_handler = switch_handler.SwitchHandler()
    if request.method == 'GET':
        # User hadn't submitted information yet, set default values
        form.switch_LED.data = sw_handler.get_switch_status(switch_handler.SWITCH_LED_PIN) == "on"
        form.switch_air_sensor.data = sw_handler.get_switch_status(switch_handler.SWITCH_AIR_SENSE_PIN) == "on"
        form.switch_medtronic.data = sw_handler.get_switch_status(switch_handler.SWITCH_MEDTRONIC_PIN) == "on"
    else:
        # Set switch status
        sw_handler.set_switch(switch_handler.SWITCH_LED_PIN, form.switch_LED.data)
        sw_handler.set_switch(switch_handler.SWITCH_AIR_SENSE_PIN, form.switch_air_sensor.data)
        sw_handler.set_switch(switch_handler.SWITCH_MEDTRONIC_PIN, form.switch_medtronic.data)
        
        time.sleep(1)
    
    # Read INA status
    tm = TelematryHandler ()
    data_ina = tm.get_ina260_telemetry()
    data_bme = tm.get_bme680_telemetry()
    
    return render_template('switch_and_analog_testing.html', form=form, 
        current_mA=data_ina[0], voltage=data_ina[1], power_mW=data_ina[2], temperature=data_bme[0], gas=data_bme[1], humidity=data_bme[2],pressure=data_bme[3])

#################### Camera Testing ################################################
class CameraForm(FlaskForm):
    camera = RadioField(label="Camera", choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    focus_units= StringField(label="Focus Setting")
    
    LED_on = BooleanField(label='Turn LEDs before taking a picture?')
    r = StringField('Red (0-255):', validators=[DataRequired()])
    g = StringField('Green (0-255):', validators=[DataRequired()])
    b = StringField('Blue (0-255):', validators=[DataRequired()])
    fr = StringField('Far Red (0-100):', validators=[DataRequired()])
    medtronic_white_LEDs = BooleanField(label='Use Medtronic White LEDs?')
    
    submit = SubmitField('Take a Picture')
    
@app.route('/CamerasTesting/', methods=['GET', 'POST'])
def camera_testing():
    form = CameraForm()
    if request.method == 'GET':
        # User hadn't submitted information yet, set default values
        form.camera.data = 'A'
        form.focus_units.data = "200"
        form.r.data = 150
        form.g.data = 210
        form.b.data = 255
        form.fr.data = 12
        
        form.LED_on.data = False
        form.medtronic_white_LEDs.data = False
        
        out_file_path = ""
    else:    
        focus_units = int(form.focus_units.data)
        sw_handler = switch_handler.SwitchHandler()
        cam = camera_handler_high_level.CameraHandlerHighLevel()
        cam.init_camera_handler()
        
        # If needed turn on LEDs
        # Stop all LEDs before starting illumination
        if form.medtronic_white_LEDs.data == True:
            mw = 1
        else:
            mw = 0
        if form.LED_on.data == True:
            r_g_b_fr_mw = [int(form.r.data),int(form.g.data),int(form.b.data),int(form.fr.data),int(mw)]
        else:
            r_g_b_fr_mw = None
        
        # Take an image
        file_path = cam.take_pic_all_focus(form.camera.data,[focus_units],
            file_name_prefix="SingleImage_{0}".format(round(time.time()*24*60*60)),
            r_g_b_fr_mw = r_g_b_fr_mw)
        
        # Copy to the static folder where iamge is found
        out_file_path = file_path[0][1]
        if not os.path.exists('static'): # Make dir if it doesn't exist
            os.makedirs('static')
        if os.path.exists('static/'+out_file_path): # Remove file if it's already there
            os.remove('static/'+out_file_path)
            
        copyfile(file_path[0][0],'static/'+out_file_path)
    
    return render_template('camera_testing.html', form=form, out_file_path=out_file_path)
      
class CameraForm2(FlaskForm):
    camera = RadioField(label="Camera", choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    focus_start_units= StringField(label="Focus Start")
    focus_jump_units= StringField(label="Focus Jump")
    focus_end_units= StringField(label="Focus End")
    
    LED_on = BooleanField(label='Turn LEDs before taking a picture?')
    r = StringField('Red (0-255):', validators=[DataRequired()])
    g = StringField('Green (0-255):', validators=[DataRequired()])
    b = StringField('Blue (0-255):', validators=[DataRequired()])
    fr = StringField('Far Red (0-100):', validators=[DataRequired()])
    medtronic_white_LEDs = BooleanField(label='Use Medtronic White LEDs?')
    
    submit = SubmitField('Take Pictures')
     
@app.route('/CameraFocusCalibration/', methods=['GET', 'POST'])
def camera_focus_calibration():
    form = CameraForm2()
    if request.method == 'GET':
        # User hadn't submitted information yet, set default values
        form.focus_start_units.data = 20
        form.focus_jump_units.data = 20
        form.focus_end_units.data = 340
        form.r.data = 150
        form.g.data = 210
        form.b.data = 255
        form.fr.data = 12
        
        form.camera.data = 'A'
        
        form.LED_on.data = False
        form.medtronic_white_LEDs.data = False

    else:    
        focus_start_units = int(form.focus_start_units.data)
        focus_jump_units = int(form.focus_jump_units.data)
        focus_end_units = int(form.focus_end_units.data)
        sw_handler = switch_handler.SwitchHandler()
        cam = camera_handler_high_level.CameraHandlerHighLevel()
        cam.init_camera_handler()
        
        # If needed turn on LEDs
        # Stop all LEDs before starting illumination
        if form.medtronic_white_LEDs.data == True:
            mw = 1
        else:
            mw = 0
        if form.LED_on.data == True:
            r_g_b_fr_mw = [int(form.r.data),int(form.g.data),int(form.b.data),int(form.fr.data),int(mw)]
        else:
            r_g_b_fr_mw = None
        
        # Take an image
        file_path = cam.take_pic_all_focus(form.camera.data,
            range(focus_start_units,focus_end_units,focus_jump_units),
            file_name_prefix="CameraFocusCalibration_{0}".format(round(time.time()*24*60*60)), 
            r_g_b_fr_mw = r_g_b_fr_mw)
    
    return render_template('camera_testing.html', form=form, out_file_path="")
    

@app.route('/TakeHeroShots/')
def take_hero_shots():    
    os.system('sudo python3 take_hero_shots.py')
    return render_template('simple_commands.html', message="Hero shot taken, restart OBC in 15 minutes")

#################### Medtronic #####################################################
class MedtronicForm(FlaskForm):
    white_LEDs = BooleanField(label='White LEDs')
    IR_LEDs = BooleanField(label='IR LEDs')
    
    submit = SubmitField('Set LEDs')
    
@app.route('/MedtronicTesting/', methods=['GET', 'POST'])
def medtronic_testing():
    form = MedtronicForm()
    
    # Turn on medtronic
    sw_handler = switch_handler.SwitchHandler()
    sw_handler.set_switch(switch_handler.SWITCH_MEDTRONIC_PIN, "on")
    
    if request.method == 'GET':
        # User hadn't submitted information yet, set default values
        form.white_LEDs.data = False
        form.IR_LEDs.data = False
    else:
        # Switch LEDs acordingly
        image_handler = root_image_handler.RootImageHandler()
        if form.white_LEDs.data:
            image_handler.white_led_on()
        else:
            image_handler.white_led_off()
            
        if form.IR_LEDs.data:
            image_handler.IR_led_on()
        else:
            image_handler.IR_led_off()
    
    # Read Ilumination status
    time.sleep(1) # Let light turn on before querry intensity
    tm = TelematryHandler ()
    data1 = tm.get_veml7700_telemetry(1)
    data2 = tm.get_veml7700_telemetry(2)
    
    return render_template('medtronic_testing.html', form=form, 
        data1_0=data1[0], data1_1=data1[1], data2_0=data2[0], data2_1=data2[1])
        
#################### Party Mode ####################################################
@app.route('/PartyMode/') # Set PartyMode?mode=x, replace x with 1,2 
def party_mode():   

    def change_color(r_s,g_s,b_s,fr_s,r_e,g_e,b_e,fr_e,n_steps=50):
        delta_r = (r_e-r_s)/n_steps
        delta_g = (g_e-g_s)/n_steps
        delta_b = (b_e-b_s)/n_steps
        delta_fr = (fr_e-fr_s)/n_steps
        
        r = r_s
        g = g_s
        b = b_s
        fr = fr_s
        
        for i in range(n_steps+1):
            led_handler.light_pixel(0,19,int(r),int(g),int(b))
            led_handler.light_far_red(int(fr))
            
            r = r + delta_r
            g = g + delta_g
            b = b + delta_b
            
            time.sleep(0.01)
    
    # Figure out which party mode to use
    party_mode = request.args.get('mode')
    if type(party_mode) == str:
        party_mode = float(party_mode)
    else:
        party_mode = 1 # Default value
        
    if party_mode==1: # First party mode
        for i in range(2):
            change_color(255,0,0,0,       255,255,0,0)    
            change_color(255,255,0,0,     0,255,0,0)  
            change_color(0,255,0,0,       0,255,255,0)  
            change_color(0,255,255,0,     0,0,255,0)  
            change_color(0,0,255,0,       255,0,255,0)  
            change_color(255,0,255,0,     255,0,0,0) 
            
        change_color(255,0,0,0,     255,255,255,0)
    else:
        for i in range(4):
            change_color(0,0,0,0,           150,210,255,0)
            change_color(150,210,255,0,     0,0,0,0)
            change_color(0,0,0,0,           255,0,0,12)
            change_color(255,0,0,12,        0,0,0,0)
    
    return render_template('simple_commands.html', message="Party Over")

#################### Main ##########################################################
if __name__ == '__main__':
    setup_logging()
    logging.info('*** Start ***')
    app.run(host='0.0.0.0', port=80)