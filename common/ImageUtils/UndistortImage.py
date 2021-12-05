import cv2 as cv
import argparse


# def update_image_metadata(in_img, out_img):
#     from exif import Image
#     with open(in_img, 'rb') as image_file:
#         with open(out_img, 'wb') as new_image_file:
#             new_image_file.write(Image(image_file).get_file())


def read_image_parameters_file(image_params_file):
    """ Loads camera matrix and distortion coefficients. """
    # FILE_STORAGE_READ
    cv_file = cv.FileStorage(image_params_file, cv.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]


def undistorted_image(input_image_path, output_image_path, image_params_file):
    mtx, dist = read_image_parameters_file(image_params_file)
    img = cv.imread(input_image_path)
    h, w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    # undistort
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    cv.imwrite(output_image_path, dst)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='undistorted image using distortion parameters (from calibration)')
    parser.add_argument("--input_image", help="path to the first image", type=str)
    parser.add_argument("--output_image", help="path to the second image", type=str)
    parser.add_argument("--calibration_data", help="path to the calibration file", type=str)

    args = parser.parse_args()

    undistorted_image(args.input_image, args.output_image, args.calibration_data)
