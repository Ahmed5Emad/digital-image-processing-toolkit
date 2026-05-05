import cv2
import numpy as np
from functools import wraps


def apply_blend(image, edges, blend_mode):
    if blend_mode == "Edges Only":
        return edges
    elif blend_mode == "Add (+)":
        blended = image.astype(np.float64) + edges.astype(np.float64)
        return np.clip(blended, 0, 255).astype(np.uint8)
    elif blend_mode == "Subtract (-)":
        blended = image.astype(np.float64) - edges.astype(np.float64)
        return np.clip(blended, 0, 255).astype(np.uint8)
    return edges


def ensure_gray(func):
    @wraps(func)
    def wrapper(image, *args, **kwargs):
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            result = func(gray, *args, **kwargs)
            if len(result.shape) == 2:
                return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
            return result
        return func(image, *args, **kwargs)
    return wrapper


def validate_params(params, schema):
    validated = {}
    for key, (param_type, min_val, max_val) in schema.items():
        val = params.get(key)
        if val is None:
            continue

        try:
            val = param_type(val)
        except (ValueError, TypeError):
            continue

        if min_val is not None and val < min_val:
            val = min_val
        if max_val is not None and val > max_val:
            val = max_val

        validated[key] = val
    return validated
