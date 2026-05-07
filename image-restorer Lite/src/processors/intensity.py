import cv2
import numpy as np


def negative(image, **kwargs):
    return cv2.bitwise_not(image)


def thresholding(image, threshold_value=127, max_value=255, **kwargs):
    _, thresh = cv2.threshold(image, threshold_value, max_value, cv2.THRESH_BINARY)
    return thresh


def log_transformation(image, **kwargs):
    image_f = image.astype(np.float32)
    max_val = np.max(image_f)
    if max_val == 0:
        return image
    c = 255 / np.log(1 + max_val)
    log_image = c * (np.log(1 + image_f))
    return np.clip(log_image, 0, 255).astype(np.uint8)


def gamma_transformation(image, gamma=1.2, **kwargs):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


def gray_level_slicing(image, r1=100, r2=200, highlight_value=255, preserve_others=True, **kwargs):
    output = image.copy()
    mask = (image >= r1) & (image <= r2)
    if preserve_others:
        output[mask] = highlight_value
    else:
        output[:] = 0
        output[mask] = highlight_value
    return output


def bit_plane_slicing(image, plane=7, **kwargs):
    return ((image >> plane) & 1) * 255
