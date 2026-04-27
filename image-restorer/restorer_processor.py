import cv2
import numpy as np

def negative(image):
    return cv2.bitwise_not(image)

def ensure_gray(func):
    def wrapper(image, *args, **kwargs):
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            result = func(gray, *args, **kwargs)
            return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR) if len(result.shape) == 2 else result
        return func(image, *args, **kwargs)
    return wrapper

@ensure_gray
def thresholding(image, threshold_value, max_value=255):
    _, thresh = cv2.threshold(image, threshold_value, max_value, cv2.THRESH_BINARY)
    return thresh

def gray_level_slicing(image, r1, r2, highlight_value=255, preserve_others=True):
    output = image.copy()
    mask = (image >= r1) & (image <= r2)
    if preserve_others:
        output[mask] = highlight_value
    else:
        output[:] = 0
        output[mask] = highlight_value
    return output

def bit_plane_slicing(image, plane):
    return ((image >> plane) & 1) * 255

def inverse_log_transformation(image):
    image_f = image.astype(np.float32)
    image_norm = image_f / 255.0
    c = 255 / (np.exp(1) - 1)
    inv_log_image = c * (np.exp(image_norm) - 1)
    return np.clip(inv_log_image, 0, 255).astype(np.uint8)

def contrast_stretching(image, r1, s1, r2, s2):
    image_f = image.astype(np.float32)
    output = np.zeros_like(image_f)
    
    mask1 = image_f < r1
    output[mask1] = (s1 / r1) * image_f[mask1]
    
    mask2 = (image_f >= r1) & (image_f < r2)
    output[mask2] = ((s2 - s1) / (r2 - r1)) * (image_f[mask2] - r1) + s1
    
    mask3 = image_f >= r2
    output[mask3] = ((255 - s2) / (255 - r2)) * (image_f[mask3] - r2) + s2
    
    return np.clip(output, 0, 255).astype(np.uint8)

@ensure_gray
def histogram_equalization(image):
    return cv2.equalizeHist(image)

def arithmetic_mean_filter(image, kernel_size=3):
    return cv2.blur(image, (kernel_size, kernel_size))

def geometric_mean_filter(image, kernel_size=3):
    image_f = image.astype(np.float32) + 1e-6
    log_image = np.log(image_f)
    mean_log = cv2.blur(log_image, (kernel_size, kernel_size))
    return np.exp(mean_log).astype(np.uint8)

def harmonic_mean_filter(image, kernel_size=3):
    image_f = image.astype(np.float32) + 1e-6
    inv_image = 1.0 / image_f
    sum_inv = cv2.blur(inv_image, (kernel_size, kernel_size))
    return (kernel_size**2 / sum_inv).astype(np.uint8)

def contraharmonic_mean_filter(image, kernel_size=3, Q=1.5):
    image_f = image.astype(np.float32) + 1e-6
    num = cv2.blur(np.power(image_f, Q + 1), (kernel_size, kernel_size))
    den = cv2.blur(np.power(image_f, Q), (kernel_size, kernel_size))
    return (num / den).astype(np.uint8)

def median_filter(image, kernel_size=3):
    return cv2.medianBlur(image, kernel_size)

def min_filter(image, kernel_size=3):
    return cv2.erode(image, np.ones((kernel_size, kernel_size), np.uint8))

def max_filter(image, kernel_size=3):
    return cv2.dilate(image, np.ones((kernel_size, kernel_size), np.uint8))

def midpoint_filter(image, kernel_size=3):
    min_f = min_filter(image, kernel_size)
    max_f = max_filter(image, kernel_size)
    return ((min_f.astype(np.float32) + max_f.astype(np.float32)) / 2).astype(np.uint8)

def laplacian_sharpening(image, ddepth=cv2.CV_64F):
    laplacian = cv2.Laplacian(image, ddepth)
    abs_laplacian = cv2.convertScaleAbs(laplacian)
    return abs_laplacian


def sobel_sharpening(image, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3):
    sobel_x = cv2.Sobel(image, ddepth, dx=dx, dy=0, ksize=ksize)
    sobel_y = cv2.Sobel(image, ddepth, dx=0, dy=dy, ksize=ksize)
    sobel = cv2.magnitude(sobel_x, sobel_y)
    abs_sobel = cv2.convertScaleAbs(sobel)
    return abs_sobel

def prewitt_sharpening(image):
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    img_prewittx = cv2.filter2D(image, -1, kernelx)
    img_prewitty = cv2.filter2D(image, -1, kernely)
    return cv2.addWeighted(img_prewittx, 0.5, img_prewitty, 0.5, 0)

def roberts_sharpening(image):
    kernelx = np.array([[1, 0], [0, -1]])
    kernely = np.array([[0, 1], [-1, 0]])
    img_robertsx = cv2.filter2D(image, -1, kernelx)
    img_robertsy = cv2.filter2D(image, -1, kernely)
    return cv2.addWeighted(img_robertsx, 0.5, img_robertsy, 0.5, 0)

def log_transformation(image):
    image_f = image.astype(np.float32)
    max_val = np.max(image_f)
    if max_val == 0:
        return image
    c = 255 / np.log(1 + max_val)
    log_image = c * (np.log(1 + image_f))
    return np.clip(log_image, 0, 255).astype(np.uint8)

def gamma_transformation(image, gamma=1.2):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def gaussian_filter(image, kernel_size=5, sigma=0):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

def bilateral_filter(image, d=9, sigmaColor=75, sigmaSpace=75):
    return cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)

def box_filter(image, kernel_size=5):
    return cv2.boxFilter(image, -1, (kernel_size, kernel_size))

def butterworth_highpass_filter(image, cutoff=30, n=2):
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    
    x = np.linspace(-ccol, ccol, cols)
    y = np.linspace(-crow, crow, rows)
    X, Y = np.meshgrid(x, y)
    D = np.sqrt(X**2 + Y**2)
    
    mask = 1 / (1 + (cutoff / (D + 1e-6))**(2*n))
    
    dft = np.fft.fft2(image)
    dft_shift = np.fft.fftshift(dft)
    
    dft_shift_filtered = dft_shift * mask
    
    dft_ishift = np.fft.ifftshift(dft_shift_filtered)
    img_back = np.fft.ifft2(dft_ishift)
    img_back = np.abs(img_back)
    
    return np.clip(img_back, 0, 255).astype(np.uint8)
