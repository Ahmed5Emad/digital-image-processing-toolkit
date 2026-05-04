import cv2
from .utils import ensure_gray


@ensure_gray
def negative(image):
    return cv2.bitwise_not(image)
