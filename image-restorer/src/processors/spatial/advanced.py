import cv2
import numpy as np


def geometric_mean_filter(image, kernel_size=3, **kwargs):
    image_f = image.astype(np.float32) + 1e-6
    log_image = np.log(image_f)
    mean_log = cv2.blur(log_image, (kernel_size, kernel_size))
    return np.exp(mean_log).astype(np.uint8)


def harmonic_mean_filter(image, kernel_size=3, **kwargs):
    image_f = image.astype(np.float32) + 1e-6
    inv_image = 1.0 / image_f
    mean_inv = cv2.blur(inv_image, (kernel_size, kernel_size))
    return np.clip(1.0 / (mean_inv + 1e-6), 0, 255).astype(np.uint8)


def max_filter(image, kernel_size=3, **kwargs):
    return cv2.dilate(image, np.ones((kernel_size, kernel_size), np.uint8))


def min_filter(image, kernel_size=3, **kwargs):
    return cv2.erode(image, np.ones((kernel_size, kernel_size), np.uint8))


def midpoint_filter(image, kernel_size=3, **kwargs):
    min_f = cv2.erode(image, np.ones((kernel_size, kernel_size), np.uint8))
    max_f = cv2.dilate(image, np.ones((kernel_size, kernel_size), np.uint8))
    return ((min_f.astype(np.float32) + max_f.astype(np.float32)) / 2).astype(np.uint8)
