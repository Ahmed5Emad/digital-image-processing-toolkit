import cv2
import numpy as np


def to_grayscale(image):
    if len(image.shape) == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def add_gaussian_noise(image, mean=0, sigma=25):
    gauss = np.random.normal(mean, sigma, image.shape)
    noisy = image + gauss
    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_salt_and_pepper_noise(image, amount=0.02):
    row, col, ch = image.shape if len(image.shape) == 3 else (*image.shape, 1)
    s_vs_p = 0.5
    out = np.copy(image)

    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    out[tuple(coords)] = 255

    num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape]
    out[tuple(coords)] = 0
    return out


def add_speckle_noise(image):
    gauss = np.random.randn(*image.shape)
    noisy = image + image * gauss
    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_periodic_noise(image, amplitude=20, frequency=0.1):
    rows, cols = image.shape[:2]
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))
    noise = amplitude * np.sin(2 * np.pi * frequency * (x + y))
    if len(image.shape) == 3:
        noise = np.stack([noise]*3, axis=-1)
    noisy = image + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_uniform_noise(image, low=-50, high=50):
    noise = np.random.uniform(low, high, image.shape)
    noisy = image + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_rayleigh_noise(image, scale=25):
    noise = np.random.rayleigh(scale, image.shape)
    noisy = image + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def add_exponential_noise(image, scale=1.0):
    noise = np.random.exponential(scale, image.shape)
    noisy = image + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def apply_blur(image, kernel_size=15):
    return cv2.blur(image, (kernel_size, kernel_size))
