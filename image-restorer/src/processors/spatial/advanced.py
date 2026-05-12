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


def contraharmonic_mean_filter(image, kernel_size=3, Q=1.5, **kwargs):
    image_f = image.astype(np.float32) + 1e-6
    num = cv2.blur(np.power(image_f, Q + 1), (kernel_size, kernel_size))
    den = cv2.blur(np.power(image_f, Q), (kernel_size, kernel_size))
    return np.clip(num / (den + 1e-6), 0, 255).astype(np.uint8)


def max_filter(image, kernel_size=3, **kwargs):
    return cv2.dilate(image, np.ones((kernel_size, kernel_size), np.uint8))


def min_filter(image, kernel_size=3, **kwargs):
    return cv2.erode(image, np.ones((kernel_size, kernel_size), np.uint8))


def midpoint_filter(image, kernel_size=3, **kwargs):
    min_f = cv2.erode(image, np.ones((kernel_size, kernel_size), np.uint8))
    max_f = cv2.dilate(image, np.ones((kernel_size, kernel_size), np.uint8))
    return ((min_f.astype(np.float32) + max_f.astype(np.float32)) / 2).astype(np.uint8)


def adaptive_median_filter(image, S_max=7, **kwargs):
    rows, cols = image.shape
    output = image.copy()
    mask_unprocessed = np.ones((rows, cols), dtype=bool)

    for k in range(3, S_max + 1, 2):
        if not np.any(mask_unprocessed):
            break

        z_min = cv2.erode(image, np.ones((k, k), np.uint8))
        z_max = cv2.dilate(image, np.ones((k, k), np.uint8))
        z_med = cv2.medianBlur(image, k)

        mask_A = (z_min < z_med) & (z_med < z_max)
        mask_process_now = mask_A & mask_unprocessed

        mask_B = (z_min < image) & (image < z_max)

        output[mask_process_now & mask_B] = image[mask_process_now & mask_B]
        output[mask_process_now & ~mask_B] = z_med[mask_process_now & ~mask_B]

        mask_unprocessed[mask_process_now] = False

        if k == S_max:
            output[mask_unprocessed] = z_med[mask_unprocessed]

    return output
