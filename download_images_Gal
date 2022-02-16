import sys
sys.path.insert(1, '../common')
from gdrive_handler import GDriveHandler
import logging
import sys
from datetime import datetime


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("gdrive.log"),
            logging.StreamHandler()
        ]
    )   


setup_logging()
if len(sys.argv)==7:
    logging.info("start g-drive testing")
    folder_ID=sys.argv[1]
    g_drive_handler = GDriveHandler(folder_ID)
    # usage example: python3 download_images.py 1usWtERCev43R107ccgdIZG83ORlwGnyB 21-09-14__06_20 21-09-14__06_22 A,C 160,260 /home/pi/dev/scp/ground_station/down_images
    start_date = sys.argv[2]
    start_date_new = datetime.strptime(start_date,"%y-%m-%d__%H_%M")
    end_date = sys.argv[3]
    end_date_new = datetime.strptime(end_date,"%y-%m-%d__%H_%M")
    list_camera = sys.argv[4]
    list_camera_new=list_camera.split(",")
    list_focus = sys.argv[5]
    list_focus_split = list_focus.split(",")
    list_focus_new = [int(i) for i in list_focus_split]
    my_path = sys.argv[6]
    print(start_date_new,end_date_new,list_camera_new,list_focus_new)
    g_drive_handler.download_images(start_date_new,end_date_new,list_camera_new,list_focus_new,my_path)
else:
    print("please enter 6 parameters:folder ID, start date, end date, list cameras, list focuses, path")
    print("for example: python3 download_images.py 1usWtERCev43R107ccgdIZG83ORlwGnyB 21-09-14__06_20 21-09-14__06_22 A,C 160,260 /home/pi/dev/scp/ground_station/down_images")
    quit()
