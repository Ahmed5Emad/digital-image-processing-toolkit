import cv2
import numpy as np


RNG = np.random.default_rng()


def clip_uint8(image):
    return np.clip(image, 0, 255).astype(np.uint8)


def to_grayscale(image):
    if len(image.shape) == 2:
        return image.copy()
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def add_gaussian_noise(image, mean=0, sigma=10):
    noise = RNG.normal(mean, sigma, image.shape)
    return clip_uint8(image.astype(np.float32) + noise)


def add_salt_and_pepper_noise(image, amount=0.005, s_vs_p=0.5):
    amount = float(np.clip(amount, 0, 1))
    s_vs_p = float(np.clip(s_vs_p, 0, 1))

    out = image.copy()
    rows, cols = image.shape[:2]
    pixel_count = rows * cols

    num_salt = int(np.ceil(amount * pixel_count * s_vs_p))
    salt_rows = RNG.integers(0, rows, num_salt)
    salt_cols = RNG.integers(0, cols, num_salt)
    out[salt_rows, salt_cols] = 255

    num_pepper = int(np.ceil(amount * pixel_count * (1 - s_vs_p)))
    pepper_rows = RNG.integers(0, rows, num_pepper)
    pepper_cols = RNG.integers(0, cols, num_pepper)
    out[pepper_rows, pepper_cols] = 0

    return out


def add_speckle_noise(image, strength=0.2):
    noise = RNG.normal(0, strength, image.shape)
    noisy = image.astype(np.float32) + image.astype(np.float32) * noise
    return clip_uint8(noisy)


def add_periodic_noise(image, amplitude=10, frequency=0.05):
    rows, cols = image.shape[:2]
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))
    noise = amplitude * np.sin(2 * np.pi * frequency * (x + y))

    if len(image.shape) == 3:
        noise = np.repeat(noise[:, :, np.newaxis], image.shape[2], axis=2)

    return clip_uint8(image.astype(np.float32) + noise)


def add_uniform_noise(image, low=-20, high=20):
    noise = RNG.uniform(low, high, image.shape)
    return clip_uint8(image.astype(np.float32) + noise)


def add_rayleigh_noise(image, scale=10):
    raw_noise = RNG.rayleigh(scale, image.shape)
    centered_noise = raw_noise - scale * np.sqrt(np.pi / 2)
    return clip_uint8(image.astype(np.float32) + centered_noise)


def add_exponential_noise(image, scale=10):
    raw_noise = RNG.exponential(scale, image.shape)
    centered_noise = raw_noise - scale
    return clip_uint8(image.astype(np.float32) + centered_noise)


def apply_blur(image, kernel_size=5):
    kernel_size = max(1, int(kernel_size))
    return cv2.blur(image, (kernel_size, kernel_size))
