import cv2
import numpy as np
from .utils import apply_blend


def point_detection(image, blend_mode="Edges Only", **kwargs):
    mask = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    edges = np.clip(np.abs(filtered), 0, 255).astype(np.uint8)
    return apply_blend(image, edges, blend_mode)


def line_detection_horizontal(image, blend_mode="Edges Only", **kwargs):
    mask = np.array([[-1, -1, -1], [2, 2, 2], [-1, -1, -1]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    edges = np.clip(np.abs(filtered), 0, 255).astype(np.uint8)
    return apply_blend(image, edges, blend_mode)


def line_detection_vertical(image, blend_mode="Edges Only", **kwargs):
    mask = np.array([[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    edges = np.clip(np.abs(filtered), 0, 255).astype(np.uint8)
    return apply_blend(image, edges, blend_mode)


def line_detection_pos_45(image, blend_mode="Edges Only", **kwargs):
    mask = np.array([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    edges = np.clip(np.abs(filtered), 0, 255).astype(np.uint8)
    return apply_blend(image, edges, blend_mode)


def line_detection_neg_45(image, blend_mode="Edges Only", **kwargs):
    mask = np.array([[-1, -1, 2], [-1, 2, -1], [2, -1, -1]], dtype=np.float32)
    filtered = cv2.filter2D(image, -1, mask)
    edges = np.clip(np.abs(filtered), 0, 255).astype(np.uint8)
    return apply_blend(image, edges, blend_mode)
