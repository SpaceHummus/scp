import cv2 as cv
import numpy as np
from alive_progress import alive_it
from scipy import linalg

from ImageUtils import ImageCalibrationUtils


class PhotogrammetryTool:

    def __init__(self, cam_mtx1, cam_mtx2, R, T):
        self.cam_mtx2 = cam_mtx2
        self.cam_mtx1 = cam_mtx1

        # RT matrix for C1 is identity.
        self.RT1 = np.concatenate([np.eye(3), [[0], [0], [0]]], axis=-1)
        self.P1 = self.cam_mtx1 @ self.RT1  # projection matrix for C1
        # RT matrix for C2 is the R and T obtained from stereo calibration.
        self.RT2 = np.concatenate([R, T], axis=-1)
        self.P2 = self.cam_mtx2 @ self.RT2  # projection matrix for C2

    def update_RT(self, R, T):
        self.RT2 = np.concatenate([R, T], axis=-1)
        self.P2 = self.cam_mtx2 @ self.RT2  # projection matrix for C2

    @staticmethod
    def from_file(stereo_calibration_file_path):
        cam_mtx1, _, cam_mtx2, _, R, T = ImageCalibrationUtils.read_stereo_calibration_file(
            stereo_calibration_file_path)

        return PhotogrammetryTool(cam_mtx1, cam_mtx2, R, T)

    def get_updated_transformation_and_projection(self, R, T):
        """
        return updated projections and transformation from cam2 to cam1 for point triangulation
        :return:
        """
        # RT matrix for C1 is identity.
        self.RT1 = np.concatenate([np.eye(3), [[0], [0], [0]]], axis=-1)
        self.P1 = self.cam_mtx1 @ self.RT1  # projection matrix for C1

        # RT matrix for C2 is the R and T obtained from stereo calibration.
        self.RT2 = np.concatenate([R, T], axis=-1)
        self.P2 = self.cam_mtx2 @ self.RT2  # projection matrix for C2

    @staticmethod
    def DLT(P1, P2, point1, point2):
        """
        direct linear transform (DLT) for estimation of 3D space from two corresponding pixels
        :param P1: projection of the first pixels to camera coordinates
        :param P2:projection of the second image pixels to ***the first*** camera coordinates
        :param point1: (u,j) in the first image (in pixels)
        :param point2:(u,j) in the second image (in pixels)
        :return: (x,y,z) in 3d space
        """
        A = [point1[1] * P1[2, :] - P1[1, :],
             P1[0, :] - point1[0] * P1[2, :],
             point2[1] * P2[2, :] - P2[1, :],
             P2[0, :] - point2[0] * P2[2, :]
             ]
        A = np.array(A).reshape((4, 4))
        # print('A: ')
        # print(A)

        B = A.transpose() @ A
        U, s, Vh = linalg.svd(B, full_matrices=False)

        return Vh[3, 0:3] / Vh[3, 3]

    def triangulate_point_set(self, uvs1, uvs2):
        """
        triangulate points from corresponding points on the first camera to the second, returns points
        in 3d space according to the reference system of RT1 and RT2 fields (most of the time its the coordinate system
        of the first camera)
        :param uvs1: Nx2 list of pixels from the first image (the reference one)
        :param uvs2: Nx2 list of pixels from the second image
        :return: list of Nx3 [x,y,z] points
        """
        uvs1 = np.array(uvs1)
        uvs2 = np.array(uvs2)

        p3ds = []
        print('triangulating points')
        for uv1, uv2 in alive_it(zip(uvs1, uvs2), total=len(uvs1)):
            _p3d = self.DLT(self.P1, self.P2, uv1, uv2)
            p3ds.append(_p3d)

        p3ds = np.array(p3ds)
        return p3ds

    def calculate_HRT_from_points(self, uvs1, uvs2):
        """
        solving camera Rotation and transformation matrices according to corresponding points
        :param uvs1: list of Nx2 pixels from image 1
        :param uvs2: list of Nx2 pixels from image 2
        :return: (H,R,T) where R and T are the new Rotation and translation matrices, and H is the Homography matrix
        """
        uvs1 = np.asarray(uvs1)
        uvs2 = np.asarray(uvs2)
        H, status = cv.findHomography(uvs1, uvs2)
        H = H.T
        h1 = H[0]
        h2 = H[1]
        h3 = H[2]
        K_inv = np.linalg.inv(self.cam_mtx1)
        L = 1 / np.linalg.norm(np.dot(K_inv, h1))
        r1 = L * np.dot(K_inv, h1)
        r2 = L * np.dot(K_inv, h2)
        r3 = np.cross(r1, r2)
        T = L * (K_inv @ h3.reshape(3, 1))
        R = np.array([[r1], [r2], [r3]])
        R = np.reshape(R, (3, 3))

        return H, R, T

    @staticmethod
    def parse_points_from_csv(csv_path):
        import csv
        uvs1 = []
        uvs2 = []
        with open(csv_path, newline='') as csv_file:
            lines = csv.reader(csv_file, delimiter=',')
            for row in lines:
                if len(row) > 0 and row[0].isdigit():
                    if row[1] == '1':
                        uvs1.append([float(row[2]), float(row[3])])
                    else:
                        uvs2.append([float(row[2]), float(row[3])])

        return uvs1, uvs2

    @staticmethod
    def visualize_3d_points(p3ds) -> None:
        """
        visualize 3d points in a graph
        :param p3ds: Nx3 list of [x,y,z] points
        """
        from matplotlib import pyplot as plt
        p3ds = np.asarray(p3ds)
        max(p3ds)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim3d(0, 100)
        ax.set_ylim3d(0, 100)
        ax.set_zlim3d(0, 100)
        ax.scatter(p3ds[:, 0], p3ds[:, 1], p3ds[:, 2])
        plt.show()


if __name__ == '__main__':
    calib_file = r"C:\SpaceHummus\Test_cycle\Hummus_images_ordered\stereo_CC_CA_110 - Copy.yml"
    points_path = r"C:\SpaceHummus\Test_cycle\Hummus_images_ordered\tble_pnts.txt"

    photo_tools = PhotogrammetryTool.from_file(calib_file)

    uvs1, uvs2 = PhotogrammetryTool.parse_points_from_csv(points_path)
    frame1_path = r"C:\SpaceHummus\Test_cycle\Hummus_images_ordered\F0110\CA\21-08-16__23_49_CA_F0110.jpg"
    frame2_path = r"C:\SpaceHummus\Test_cycle\Hummus_images_ordered\F0110\CC\21-08-16__23_50_CC_F0110.jpg"

    PhotogrammetryTool.sift_features(frame1_path, frame2_path)

    # Read source image.
    im_src = cv.imread(frame1_path)
    # Four corners of the book in source image
    pts_src = np.array(uvs1)

    # Read destination image.
    im_dst = cv.imread(frame2_path)
    # Four corners of the book in destination image.
    pts_dst = np.array(uvs2)

    # Calculate Homography

    h, r, t = photo_tools.calculate_HRT_from_points(uvs1, uvs2)

    p3d_pre_homography = photo_tools.triangulate_point_set(uvs1, uvs2)

    photo_tools.update_RT(r, t)
    p3d_post_homography = photo_tools.triangulate_point_set(uvs1, uvs2)

    # Warp source image to destination based on homography
    im_out = cv.warpPerspective(im_src, h, (im_dst.shape[1], im_dst.shape[0]))

    cv.namedWindow("output", cv.WINDOW_NORMAL)
    # Display images
    cv.imshow("Source Image", cv.resize(im_src, (960, 540)))
    cv.imshow("Destination Image", cv.resize(im_dst, (960, 540)))
    cv.imshow("Warped Source Image", cv.resize(im_out, (960, 540)))

    cv.waitKey(0)
