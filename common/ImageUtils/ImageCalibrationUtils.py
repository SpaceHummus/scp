import glob

import cv2 as cv
import numpy as np
from alive_progress import alive_it


def save_cv_file(file_path, **kwargs) -> None:
    """
    saves the arguments to a yml file
    :param file_path: path to the output file
    :param kwargs: parameters to save
    :return:
    """
    cv_file = cv.FileStorage(file_path, cv.FILE_STORAGE_WRITE)
    print('saving file...')
    for arg in alive_it(kwargs):
        cv_file.write(arg, kwargs[arg])

    cv_file.release()
    print(f'finished saving to {file_path}')


def calibrate_camera(images_folder, rows=5, columns=8, world_scaling=1., save_result_in_file=False,
                     calibration_result_path='camera_calibration.yml', show_debug_images=False):
    """
    calibrate camera using folder's images
    :param images_folder: path to the folder containing the images,
        using regEx to find the images (eg. use *.jpg for all the jpgs in the folder or *R*.jpg for all the images with R
        in then of type jpg)
    :param rows: number of rows in the checkers calibration board
    :param columns:  number of columns in the checkers calibration board
    :param world_scaling: scale of each square
    :param show_debug_images: hide or show the images with the chess corners
    :param save_result_in_file: bool, should the process save the result in a yml file
    :param calibration_result_path:  path to the yml calibration result
    :return: (ret, mtx, dist, rvecs, tvecs ) >>>>
        ret, 'rms'
        mtx, 'camera matrix'
        dist, 'distortion coeffs:'
        rvecs, 'Rs rotation vectors'
        tvecs, 'Ts translation vectors'
    """

    # read the images from a folder
    images = read_images_from_folder(images_folder)

    # criteria used by checkerboard pattern detector.
    # Change this if the code can't find the checkerboard
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # coordinates of squares in the checkerboard world space
    reference_points = np.zeros((rows * columns, 3), np.float32)
    reference_points[:, :2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
    reference_points = world_scaling * reference_points

    # frame dimensions. Frames should be the same size.
    width = images[0].shape[1]
    height = images[0].shape[0]

    # Pixel coordinates of checkerboards
    img_points = []  # 2d points in image plane.

    # coordinates of the checkerboard in checkerboard world space.
    obj_points = []  # 3d point in real world space

    print('calibrating frames')
    for frame in alive_it(images):
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # find the checkerboard
        ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)

        if ret == True:
            # Convolution size used to improve corner detection. Don't make this too large.
            conv_size = (11, 11)

            # opencv can attempt to improve the checkerboard coordinates
            corners = cv.cornerSubPix(gray, corners, conv_size, (-1, -1), criteria)

            # shows the image with the chess corners for debug)
            if show_debug_images:
                show_chess_board_image(columns, corners, frame, ret, rows)

            obj_points.append(reference_points)
            img_points.append(corners)

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, (width, height), None, None)

    print(f'finished calibrating {images_folder}, rmse:', ret)
    if save_result_in_file:
        save_cv_file(file_path=calibration_result_path, ret=ret, mtx=mtx, dist=dist)

    return ret, mtx, dist, rvecs, tvecs


def read_stereo_calibration_file(file_path):
    """
    read the parameters from the calibration yml file
    the file should contain the following : mtx1, dist1, mtx2, dist2, R, T by those names
    :param file_path: path to the calibration store data
    :return: mtx1, dist1, mtx2, dist2, R, T
    """
    cv_file = cv.FileStorage(file_path, cv.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    mtx1 = cv_file.getNode("mtx1").mat()
    dist1 = cv_file.getNode("dist1").mat()
    mtx2 = cv_file.getNode("mtx2").mat()
    dist2 = cv_file.getNode("dist2").mat()
    R = cv_file.getNode("R").mat()
    T = cv_file.getNode("T").mat()
    return mtx1, dist1, mtx2, dist2, R, T


def stereo_calibrate(mtx1, dist1, mtx2, dist2, frames_folder, rows=5, columns=8, world_scaling=1.,
                     show_debug_images=False, save_result_in_file=False,
                     calibration_result_path='stereo_calibration.yml'):
    """
    calibrate pose estimation or the stereo sensors
    :param mtx1: camera matrix for the first camera
    :param dist1: distortion coeffs for the first camera
    :param mtx2: camera matrix for the second camera
    :param dist2:  distortion coeffs for the second camera
    :param frames_folder: path to the folder containing the images,
        using regEx to find the images (eg. use *.jpg for all the jpgs in the folder or *R*.jpg for all the images with R
        in then of type jpg)
    :param rows: number of rows in the checkers calibration board
    :param columns:  number of columns in the checkers calibration board
    :param world_scaling: scale of each square
    :param show_debug_images: show chess images for debug
    :param save_result_in_file: bool, should the process save the result in a yml file
    :param calibration_result_path:  path to the yml calibration result
    :return: retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F >>> R , T- Rotation (R) and Transformation (T) matrix from camera 2 to 1
    """
    print(f"calibrating stereo images for folder {frames_folder}")
    # read the synced frames
    images_names = glob.glob(frames_folder)
    images_names = sorted(images_names)
    c1_images_names = images_names[:len(images_names) // 2]
    c2_images_names = images_names[len(images_names) // 2:]

    c1_images = []
    c2_images = []

    print('reading images...')
    for im1, im2 in alive_it(zip(c1_images_names, c2_images_names)):
        _im = cv.imread(im1, 1)
        c1_images.append(_im)

        _im = cv.imread(im2, 1)
        c2_images.append(_im)

    # change this if stereo calibration not good.
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.0001)

    # coordinates of squares in the checkerboard world space
    world_reference_points = np.zeros((rows * columns, 3), np.float32)
    world_reference_points[:, :2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
    world_reference_points = world_reference_points * world_scaling

    # frame dimensions. Frames should be the same size.
    width = c1_images[0].shape[1]
    height = c1_images[0].shape[0]

    # Pixel coordinates of checkerboards
    img_points_left = []  # 2d points in image plane.
    img_points_right = []

    # coordinates of the checkerboard in checkerboard world space.
    obj_points = []  # 3d point in real world space

    print('matching images...')
    for frame1, frame2 in alive_it(zip(c1_images, c2_images), total=len(c1_images)):
        gray1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        c_ret1, corners1 = cv.findChessboardCorners(gray1, (rows, columns), None)
        c_ret2, corners2 = cv.findChessboardCorners(gray2, (rows, columns), None)

        if c_ret1 == True and c_ret2 == True:
            corners1 = cv.cornerSubPix(gray1, corners1, (11, 11), (-1, -1), criteria)
            corners2 = cv.cornerSubPix(gray2, corners2, (11, 11), (-1, -1), criteria)

            if show_debug_images:
                cv.drawChessboardCorners(frame1, (rows, columns), corners1, c_ret1)
                cv.imshow('img', frame1)

                cv.drawChessboardCorners(frame2, (rows, columns), corners2, c_ret2)
                cv.imshow('img2', frame2)
                cv.waitKey(500)

            obj_points.append(world_reference_points)
            img_points_left.append(corners1)
            img_points_right.append(corners2)

    stereo_calibration_flags = cv.CALIB_FIX_INTRINSIC

    ret, cm1, dist1, cm2, dist2, R, T, E, F = cv.stereoCalibrate(obj_points, img_points_left, img_points_right, mtx1,
                                                                 dist1,
                                                                 mtx2, dist2, (width, height), criteria=criteria,
                                                                 flags=stereo_calibration_flags)

    if save_result_in_file:
        save_cv_file(file_path=calibration_result_path, mtx1=cm1, dist1=dist1, mtx2=cm2, dist2=dist2, R=R, T=T, E=E,
                     F=F)

    print(ret)
    return ret, cm1, dist1, cm2, dist2, R, T, E, F


def show_chess_board_image(columns, corners, frame, ret, rows):
    cv.drawChessboardCorners(frame, (rows, columns), corners, ret)
    cv.imshow('img', frame)
    cv.waitKey(500)


def read_images_from_folder(images_folder):
    print(f'calibrating images for folder {images_folder}')
    images_names = glob.glob(images_folder)
    images = []
    print('reading images')
    for image_name in alive_it(images_names):
        im = cv.imread(image_name, 1)
        images.append(im)
    return images

