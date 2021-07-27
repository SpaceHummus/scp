# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and sett
import yaml
from flask import Flask, request, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import logging


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
CONF_FILE_NAME = "scp_conf.yaml"

Bootstrap(app)
class ConfForm(FlaskForm):
    name = StringField('Google folder id:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def main():
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

if __name__ == '__main__':
    setup_logging()
    logging.info('*** Start ***')
    app.run(host='0.0.0.0', port=80)