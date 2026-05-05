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

def prewitt_sharpening(image, blend_mode="Add (+)", **kwargs):
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    img_prewittx = cv2.filter2D(image.astype(np.float32), -1, kernelx)
    img_prewitty = cv2.filter2D(image.astype(np.float32), -1, kernely)
    edges = np.sqrt(img_prewittx**2 + img_prewitty**2)
    edges_clipped = np.clip(edges, 0, 255).astype(np.uint8)
    return apply_blend(image, edges_clipped, blend_mode)

def roberts_sharpening(image, blend_mode="Add (+)", **kwargs):
    kernelx = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernely = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    img_robertsx = cv2.filter2D(image.astype(np.float32), -1, kernelx)
    img_robertsy = cv2.filter2D(image.astype(np.float32), -1, kernely)
    edges = np.sqrt(img_robertsx**2 + img_robertsy**2)
    edges_clipped = np.clip(edges, 0, 255).astype(np.uint8)
    return apply_blend(image, edges_clipped, blend_mode)
