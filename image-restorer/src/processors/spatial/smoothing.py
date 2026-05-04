import cv2
import numpy as np
from ..utils import ensure_gray

@ensure_gray
def arithmetic_mean_filter(image, kernel_size=3, **kwargs):
    kernel_size = int(kernel_size)
    return cv2.blur(image, (kernel_size, kernel_size))

@ensure_gray
def median_filter(image, kernel_size=3, **kwargs):
    kernel_size = int(kernel_size)
    return cv2.medianBlur(image, kernel_size)

@ensure_gray
def alpha_trimmed_mean_filter(image, kernel_size=3, d=2, **kwargs):
    kernel_size = int(kernel_size)
    d = int(d)
    
    pad = kernel_size // 2
    padded = cv2.copyMakeBorder(image, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    
    from numpy.lib.stride_tricks import sliding_window_view
    windows = sliding_window_view(padded, (kernel_size, kernel_size))
    
    flat_windows = windows.reshape(image.shape[0], image.shape[1], -1)
    sorted_windows = np.sort(flat_windows, axis=-1)
    
    low = d // 2
    high = sorted_windows.shape[-1] - (d - low)
    
    trimmed = sorted_windows[:, :, low:high]
    return np.mean(trimmed, axis=-1).astype(np.uint8)
