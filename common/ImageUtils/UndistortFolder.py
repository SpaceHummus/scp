import argparse

from common.ImageUtils.UndistortImage import undistorted_image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='undistorted folder with images using distortion parameters (from calibration)')
    parser.add_argument("--input_folder", help="path to the folder with images to undistorted", type=str)
    parser.add_argument("--output_folder", help="path to the output dir", type=str)
    parser.add_argument("--calibration_data", help="path to the calibration file", type=str)

    args = parser.parse_args()

    undistorted_image(args.input_image, args.output_image, args.calibration_data)
