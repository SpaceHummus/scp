import argparse
import os, glob, shutil

from common.ImageUtils.UndistortImage import undistorted_image


def undistort_folder(input_folder, output_folder, calibration_data, file_extension='jpg'):
    os.chdir(input_folder)

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder)

    images = glob.glob('*.' + file_extension)
    for image in images:
        undistorted_image(os.path.join(input_folder, image), os.path.join(output_folder, image), calibration_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='undistort folder with images using distortion parameters (from calibration)'
    )
    parser.add_argument("--input_folder", help="path to the folder with images to undistorted", type=str)
    parser.add_argument("--output_folder", help="path to the output dir", type=str)
    parser.add_argument("--calibration_data", help="path to the calibration file", type=str)
    parser.add_argument("--file_extension", help="file extension for the cameras", type=str, default='jpg')

    args = parser.parse_args()

    undistort_folder(args.input_folder, args.output_folder, args.calibration_data, args.file_extension)
