import numpy as np

from histolab.filters.image_filters import EosinChannel, HematoxylinChannel
from PIL import Image


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
