from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np

import time

from stitching import Stitcher

#plt.ion()

def plot_image(img, figsize_in_inches=(5,5)):
    fig, ax = plt.subplots(figsize=figsize_in_inches)
    ax.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.show()
    
def plot_images(imgs, figsize_in_inches=(5,5)):
    fig, axs = plt.subplots(1, len(imgs), figsize=figsize_in_inches)
    for col, img in enumerate(imgs):
        axs[col].imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.show()


def stitching_img(camera_images):
    img1 = cv.imread(camera_images[0])
    img2 = cv.imread(camera_images[1])

    mask1 = np.zeros(img1.shape[:2], np.uint8)
    mask1[0:2592, 2800:4608] = 255

    mask2 = np.zeros(img2.shape[:2], np.uint8)
    mask2[0:2592, 0:1800] = 255

    masks = [mask1, mask2]

    panorama = stitcher.stitch(camera_images, masks)

    return panorama


stitcher = Stitcher()

stitcher = Stitcher(detector="orb", confidence_threshold=0.2, nfeatures=500, try_use_gpu=1, crop=False)

'''camera_images = ["img01.jpg", "img02.jpg"]

img1 = cv.imread('img01.jpg')
img2 = cv.imread('img02.jpg')

mask1 = np.zeros(img1.shape[:2], np.uint8)
mask1[0:2592, 2800:4608] = 255

mask2 = np.zeros(img2.shape[:2], np.uint8)
mask2[0:2592, 0:1800] = 255

masks = [mask1, mask2]

#masked1_img = cv.bitwise_and(img1,img1, mask = mask1)
#masked1_img = cv.resize(masked1_img,(0,0),fx=0.4,fy=0.4)

#masked2_img = cv.bitwise_and(img2,img2, mask = mask2)
#masked2_img = cv.resize(masked2_img,(0,0),fx=0.4,fy=0.4)

#cv.imshow('Mask1',mask1)
#cv.waitKey(0)
#cv.imshow('Masked1 Image',masked1_img)
#cv.imshow('Masked2 Image',masked2_img)
#cv.waitKey(0)
#cv.destroyAllWindows()


panorama = stitcher.stitch(camera_images, masks)'''

camera_images = ["img01.jpg", "img02.jpg"]

stitched_image = stitching_img(camera_images)

plot_image(stitched_image, (20,20))




#camera_images = ["img03.jpg", "img04.jpg"]

#img1 = cv.imread('img03.jpg')
#img2 = cv.imread('img04.jpg')