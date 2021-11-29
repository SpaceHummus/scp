import sys
sys.path.insert(1, '../common')
from gdrive_handler import GDriveHandler
from flask import Flask, request, render_template, redirect, url_for
import logging
from datetime import datetime

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("picWeb.log"),
            logging.StreamHandler()
        ]
    )   


app = Flask(__name__)

@app.route('/')
def index():
    g_drive_handler = GDriveHandler()
    exp_list = g_drive_handler.get_folder_content(g_drive_handler.main_folder_id)
    return render_template('imagesparams.html', experiments=exp_list)


@app.route('/searchImages', methods=['POST'])
def search_images():
    experiment = request.form['experiments']
    imagedatetime = request.form['imagedatetime']
    thecamaras = request.form['thecamaras']
    thefocus = request.form['thefocus']
    logging.info("experiment:%s\nimagedatetime:%s\nthecamaras:%s\nthefocus:%s",experiment,imagedatetime,thecamaras,thefocus)
    
    img_date_time = datetime.strptime(imagedatetime,"%Y-%m-%dT%H:%M")
    g_drive_handler = GDriveHandler(experiment)
    if thecamaras =="ac":
        im1_id = g_drive_handler.get_image_id(img_date_time,"A",thefocus)
        im2_id = g_drive_handler.get_image_id(img_date_time,"C",thefocus)
    else:
        im1_id = g_drive_handler.get_image_id(img_date_time,"B",thefocus)
        im2_id = g_drive_handler.get_image_id(img_date_time,"D",thefocus)
    return render_template('pinpoint.html',im1_id=im1_id,im2_id=im2_id)
    #"1zLAZaQfZnBKc8kXVBMvAkZYg3WggNvBr"

@app.route('/dataImages', methods=['POST'])
def data_images():
    xname1 = int(request.form['xname1'])
    yname1 = int(request.form['yname1'])
    xname2 = int(request.form['xname2'])
    yname2 = int(request.form['yname2'])
    print("x1:%d,y1:%d - x2:%d,y2:%d" % (xname1,yname1,xname2,yname2))
    return render_template('pinpoint.html')


if __name__ == '__main__':

    setup_logging()
    # img_date_time = datetime.strptime("2021-11-29T07:07","%Y-%m-%dT%H:%M")
    # g_drive_handler = GDriveHandler("1usWtERCev43R107ccgdIZG83ORlwGnyB")
    # g_drive_handler.get_image_id(img_date_time,"C","160")
    app.run(host='0.0.0.0', port=8090)