import cv2
import numpy as np
from ..utils import apply_blend

def laplacian_sharpening(image, blend_mode="Subtract (-)", **kwargs):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    edges = np.clip(np.abs(laplacian), 0, 255).astype(np.uint8)
    return apply_blend(image, edges, blend_mode)

def sobel_sharpening(image, ksize=3, blend_mode="Add (+)", **kwargs):
    ksize = int(ksize)
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
    edges = np.sqrt(sobel_x**2 + sobel_y**2)
    edges_clipped = np.clip(edges, 0, 255).astype(np.uint8)
    return apply_blend(image, edges_clipped, blend_mode)
