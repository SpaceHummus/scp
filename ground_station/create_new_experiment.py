import sys
sys.path.insert(1, '../common')
from gdrive_handler import GDriveHandler
import logging

ROOT_FOLDER_ID="1TeYo5TB0DSDe4QAPa_7Wjta79ZxSd4pQ"


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("new_experiment.log"),
            logging.StreamHandler()
        ]
    )   


if __name__ == "__main__":
    setup_logging()
    logging.info("start")

    if len(sys.argv)<=1:
        print("usage: creates a new experiment on g-drive with new folder structures. parametrs: <experiment name> <experiment date in YYYY/M/D hh:mm:ss> . prints the new folder id of the experiment\n")
        print("for example: python3 create_new_experiment.py \"2023-07-08 B0.1 Yerucham Dev1\" \"2023/07/15 10:00:00\"")
        quit()
    else:
        if len(sys.argv)<=2:
            print("missing parameter")
            quit()
        g_drive_handler = GDriveHandler(ROOT_FOLDER_ID)
        f_id = g_drive_handler.create_experiment_struct(sys.argv[1],sys.argv[2])
        logging.info("created new experiment. its folder id is:%s",f_id)
  