import cv2
import numpy as np
from .utils import ensure_gray


@ensure_gray
def point_detection(image, **kwargs):
    mask = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    return np.clip(np.abs(filtered), 0, 255).astype(np.uint8)


@ensure_gray
def line_detection_horizontal(image, **kwargs):
    mask = np.array([[-1, -1, -1], [2, 2, 2], [-1, -1, -1]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    return np.clip(np.abs(filtered), 0, 255).astype(np.uint8)


@ensure_gray
def line_detection_vertical(image, **kwargs):
    mask = np.array([[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    return np.clip(np.abs(filtered), 0, 255).astype(np.uint8)


@ensure_gray
def line_detection_pos_45(image, **kwargs):
    mask = np.array([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    return np.clip(np.abs(filtered), 0, 255).astype(np.uint8)


@ensure_gray
def line_detection_neg_45(image, **kwargs):
    mask = np.array([[-1, -1, 2], [-1, 2, -1], [2, -1, -1]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    return np.clip(np.abs(filtered), 0, 255).astype(np.uint8)
