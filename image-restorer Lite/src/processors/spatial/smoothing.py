import cv2
import numpy as np

def arithmetic_mean_filter(image, kernel_size=3, **kwargs):
    kernel_size = int(kernel_size)
    return cv2.blur(image, (kernel_size, kernel_size))

def median_filter(image, kernel_size=3, **kwargs):
    kernel_size = int(kernel_size)
    return cv2.medianBlur(image, kernel_size)
