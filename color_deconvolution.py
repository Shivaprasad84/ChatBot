import cv2
import numpy as np

from histolab.filters.image_filters import EosinChannel, HematoxylinChannel

from PIL import Image

def perform_segmentation(image):
    name, type = image.split('.')
    image_path = f'images/{image}'
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0

    markers = cv2.watershed(img,markers)
    img[markers == -1] = [0,0,255]

    # Crop  to remove border
    w, h, _ = img.shape
    crop_img = img[1:w - 1, 1:h - 1]
    res = Image.fromarray(crop_img)
    res.save(f'images/{name}_segmented.{type}')
    return f'{name}_segmented.{type}'


def get_image_from_file(name, type):
    image_file = f'images/{name}.{type}'
    image = Image.open(image_file)
    return image


def apply_color_deconvolution(image, channel) -> str:
    deconv_image = channel(image)
    deconv_image_ndarray = np.array(deconv_image)
    result = Image.fromarray(deconv_image_ndarray, 'RGB')
    return result


def hematoxylin_channel(name, type):
    image = get_image_from_file(name, type)
    channel = HematoxylinChannel()
    result = apply_color_deconvolution(image, channel)
    result.save(f'images/{name}_deconv.{type}')
    return f'{name}_deconv.{type}'


def eosin_channel(name, type):
    image = get_image_from_file(name, type)
    channel = EosinChannel()
    result = apply_color_deconvolution(image, channel)
    result.save(f'images/{name}_deconv.{type}')
    return f'{name}_deconv.{type}'
