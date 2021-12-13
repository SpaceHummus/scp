import glob
import os
import shutil

import numpy as np

from ImageCalibrationUtils import calibrate_camera
import argparse


def get_unique_focus_levels(calibration_images):
    unique_lvls = np.unique([os.path.splitext(img.split('_')[-1])[0] for img in calibration_images])
    focuses = {}

    for lvl in unique_lvls:
        focuses[lvl] = [img for img in calibration_images if os.path.splitext(img.split('_')[-1])[0] == lvl]

    return focuses


def calibrate_folder_camera(images_folder: str, calibration_result_path: str, rows=5, columns=8, world_scaling=0.1,
                            camera_prefix=''):
    os.chdir(images_folder)

    calibration_images = glob.glob('*.jpg')
    tmp_folder_path = os.path.join(images_folder, '_tmp')

    focus_img_dict = get_unique_focus_levels(calibration_images)

    if os.path.exists(tmp_folder_path):
        i = 0
        tmp_folder_path = f'{tmp_folder_path}_{i}'
        while os.path.exists(i_tmp_name):
            i += 1
            i_tmp_name = f'{tmp_folder_path}_{i}'
        tmp_folder_path = tmp_folder_path
        # shutil.rmtree(tmp_folder_path)

    os.makedirs(tmp_folder_path)

    for f in list(focus_img_dict)[::-1]:
        print(f'calibration focus level: {f}')
        tmp_focus_folder = os.path.join(tmp_folder_path, f)
        os.makedirs(tmp_focus_folder)
        for img in focus_img_dict[f]:
            shutil.copy2(src=os.path.join(images_folder, img), dst=os.path.join(tmp_focus_folder, img))

        calibrate_camera(images_folder=tmp_focus_folder,
                         calibration_result_path=os.path.join(calibration_result_path, f'{camera_prefix}_{f}.yaml'),
                         rows=rows,
                         columns=columns,
                         world_scaling=world_scaling,
                         save_result_in_file=True
                         )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calibrate images from a folder into a calibration.yml file')
    parser.add_argument('input_folder', metavar='i', help="path to the images folder for calibration", type=str)
    parser.add_argument("output_calibration_dir", metavar='o',
                        help="path to the folder in which the yaml files will be written",
                        type=str)
    parser.add_argument("--camera_prefix", help="prefix for the camera name, default is \'\'", type=str, default='')
    parser.add_argument("--rows", help="number of rows in the chess board pattern, default 5", type=int, default=12)
    parser.add_argument("--columns", help="number of columns in the chess board pattern, default 8", type=int,
                        default=14)
    parser.add_argument("--scaling", help="size of each square, default 1.0", type=float, default=2.)

    args = parser.parse_args()
    calibrate_folder_camera(images_folder=args.input_folder,
                            calibration_result_path=args.output_calibration_dir,
                            rows=args.rows,
                            columns=args.columns,
                            world_scaling=args.scaling,
                            camera_prefix=args.camera_prefix
                            )
