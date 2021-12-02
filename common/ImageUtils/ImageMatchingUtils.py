import cv2 as cv
# import numpy as np
# from skimage.measure import ransac
# from skimage.transform import AffineTransform


def siftMatching(img1_path, img2_pth):
    # Input : image1 and image2 in opencv format
    # Output : corresponding key points for source and target images
    # Output Format : Numpy matrix of shape: [No. of Correspondences X 2]

    template_detect = cv.ima

    sift = cv.SIFT()
    dense = cv.FeatureDetector_create("Dense")
    kp1 = dense.detect(template_detect)
    _, des1 = sift.compute(template_detect, kp1)
    kp2 = dense.detect(image_detect)
    _, des2 = sift.compute(image_detect, kp2)


if __name__ == '__main__':
    f1 = r"C:\SpaceHummus\Render_test\L.jpg"
    f2 = r"C:\SpaceHummus\Render_test\R.jpg"


    siftMatching(f1,f2)


    main