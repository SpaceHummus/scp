import argparse
import sys
import numpy as np

sys.path.insert(1, '../../common')
from gdrive_handler import GDriveHandler
from flask import Flask, request, render_template, redirect, url_for
import logging
from datetime import datetime
from ImageUtils.PhotogrametricUtils import PhotogrammetryTool


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
global photo_tools_tmp


@app.route('/')
def index():
    g_drive_handler = GDriveHandler()
    exp_list = g_drive_handler.get_folder_content(g_drive_handler.main_folder_id)
    return render_template('imagesparams.html', experiments=exp_list)


@app.route('/searchImages', methods=['POST'])
def search_images():
    experiment = request.form['experiments']
    image_date_time = request.form['imagedatetime']
    cameras_bundle = request.form['thecamaras']
    focus_level = request.form['thefocus']
    logging.info("experiment:%s\nimagedatetime:%s\nthecamaras:%s\nthefocus:%s", experiment, image_date_time,
                 cameras_bundle,
                 focus_level)

    img_date_time = datetime.strptime(image_date_time, "%Y-%m-%dT%H:%M")
    g_drive_handler = GDriveHandler(experiment)
    if cameras_bundle == "ac":
        im1_id = g_drive_handler.get_image_id(img_date_time, "A", focus_level)
        im2_id = g_drive_handler.get_image_id(img_date_time, "C", focus_level)
    else:
        im1_id = g_drive_handler.get_image_id(img_date_time, "B", focus_level)
        im2_id = g_drive_handler.get_image_id(img_date_time, "D", focus_level)

    return render_template('pinpoint.html',
                           experiment=experiment,
                           im1_id=im1_id,
                           im2_id=im2_id,
                           focus=focus_level,
                           cams=cameras_bundle.upper())
    # "1zLAZaQfZnBKc8kXVBMvAkZYg3WggNvBr"


@app.route('/dataImages', methods=['POST'])
def data_images():
    # global photo_tools_tmp
    experiment = request.form['experiment']
    cams = request.form['cams']
    focus = request.form['focus']
    im1_id = request.form['im1_id']
    im2_id = request.form['im2_id']
    out_data = request.form['outVals']
    try:
        x1 = int(request.form['xname1'])
        y1 = int(request.form['yname1'])
        x2 = int(request.form['xname2'])
        y2 = int(request.form['yname2'])
        g_drive_handler = GDriveHandler(experiment)
        bundle_file_data = g_drive_handler.get_bundle_adjustment_file(cams, focus)
        photo_tools = PhotogrammetryTool.from_yaml_str(bundle_file_data)
        tri_points = photo_tools.triangulate_point_set([[x1, y1]], [[x2, y2]])
        # tri_points = photo_tools_tmp.triangulate_point_set([[x1, y1]], [[x2, y2]])
        print("x1:%d,y1:%d - x2:%d,y2:%d" % (x1, y1, x2, y2))
        print(tri_points)
    except:
        print("none valid inputs were inserted")
        return render_template('pinpoint.html', experiment=experiment,
                               im1_id=im1_id,
                               im2_id=im2_id,
                               focus=focus,
                               cams=cams.upper(), out_data=out_data)

    return_str = ','.join(list(np.round(tri_points[0], 3).astype(str)))
    if out_data == '':
        out_data = return_str
    else:
        out_data += '\n' + return_str
    return render_template('pinpoint.html',
                           out_data=out_data,
                           im1_id=im1_id,
                           im2_id=im2_id,
                           cams=cams,
                           focus=focus,
                           experiment=experiment
                           )


@app.route('/get-all')
def get_all_experiments():
    g_drive_handler = GDriveHandler()
    exp_list = g_drive_handler.get_folder_content(g_drive_handler.main_folder_id)
    return {"asd": "asd"}


if __name__ == '__main__':
    setup_logging()
    parser = argparse.ArgumentParser(description='run the web server for the growth estimation UI')
    parser.add_argument('--host', help="host name for the app", default='0.0.0.0', type=str)
    parser.add_argument('--port', help="port number for the app", default=8090, type=int)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)
