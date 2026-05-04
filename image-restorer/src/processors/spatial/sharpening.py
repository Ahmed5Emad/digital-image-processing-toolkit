import cv2
import numpy as np
from ..utils import ensure_gray

@ensure_gray
def laplacian_sharpening(image, **kwargs):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    sharpened = image.astype(np.float64) - laplacian
    return np.clip(sharpened, 0, 255).astype(np.uint8)

@ensure_gray
def sobel_sharpening(image, ksize=3, **kwargs):
    ksize = int(ksize)
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
    sobel = np.sqrt(sobel_x**2 + sobel_y**2)
    sharpened = image.astype(np.float64) + sobel
    return np.clip(sharpened, 0, 255).astype(np.uint8)

@ensure_gray
def prewitt_sharpening(image, **kwargs):
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    img_prewittx = cv2.filter2D(image.astype(np.float32), -1, kernelx)
    img_prewitty = cv2.filter2D(image.astype(np.float32), -1, kernely)
    sharpened = image.astype(np.float64) + np.sqrt(img_prewittx**2 + img_prewitty**2)
    return np.clip(sharpened, 0, 255).astype(np.uint8)

@ensure_gray
def roberts_sharpening(image, **kwargs):
    kernelx = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernely = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    img_robertsx = cv2.filter2D(image.astype(np.float32), -1, kernelx)
    img_robertsy = cv2.filter2D(image.astype(np.float32), -1, kernely)
    sharpened = image.astype(np.float64) + np.sqrt(img_robertsx**2 + img_robertsy**2)
    return np.clip(sharpened, 0, 255).astype(np.uint8)
