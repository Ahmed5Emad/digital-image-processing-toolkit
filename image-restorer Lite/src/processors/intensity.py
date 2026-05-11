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


def inverse_log_transformation(image, **kwargs):
    image_f = image.astype(np.float32)
    image_norm = image_f / 255.0
    c = 255 / (np.exp(1) - 1)
    inv_log_image = c * (np.exp(image_norm) - 1)
    return np.clip(inv_log_image, 0, 255).astype(np.uint8)


def gamma_transformation(image, gamma=1.2, **kwargs):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


def contrast_stretching(image, r1=0, s1=0, r2=255, s2=255, **kwargs):
    image_f = image.astype(np.float32)
    output = np.zeros_like(image_f)

    mask1 = image_f < r1
    if r1 > 0:
        output[mask1] = (s1 / r1) * image_f[mask1]
    else:
        output[mask1] = 0

    mask2 = (image_f >= r1) & (image_f < r2)
    if r2 > r1:
        output[mask2] = ((s2 - s1) / (r2 - r1)) * (image_f[mask2] - r1) + s1
    else:
        output[mask2] = s1

    mask3 = image_f >= r2
    if 255 > r2:
        output[mask3] = ((255 - s2) / (255 - r2)) * (image_f[mask3] - r2) + s2
    else:
        output[mask3] = s2

    return np.clip(output, 0, 255).astype(np.uint8)


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


def histogram_equalization(image, **kwargs):
    return cv2.equalizeHist(image)
