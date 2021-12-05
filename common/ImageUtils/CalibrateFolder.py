from ImageCalibrationUtils import calibrate_camera
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calibrate images from a folder into a calibration.yml file')
    parser.add_argument('input_folder', metavar='i', help="path to the images folder for calibration", type=str)
    parser.add_argument("output_calibration_file", metavar='o', help="path to the output calibration yml file",
                        type=str)
    parser.add_argument("--rows", help="number of rows in the chess board pattern", type=int, default=5)
    parser.add_argument("--columns", help="number of columns in the chess board pattern", type=int, default=8)
    parser.add_argument("--scaling", help="size of each square", type=float, default=1.)

    args = parser.parse_args()
    calibrate_camera(images_folder=args.input_folder,
                     calibration_result_path=args.output_calibration_file,
                     rows=args.rows,
                     columns=args.columns,
                     save_result_in_file=True
                     )
