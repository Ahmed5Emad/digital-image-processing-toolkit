# Modular Image Restorer Learnings

## Utilities
- Implemented `ensure_gray` decorator using `functools.wraps` to preserve function metadata.
- Implemented `validate_params` for parameter clamping and type conversion based on a schema `(type, min, max)`.
- Cleaned up code by removing unnecessary docstrings and comments as per project standards.

## Modularization PoC
- Successfully moved the `negative` filter to a dedicated `src/processors/intensity.py` module.
- Verified that relative imports (`from .utils import ensure_gray`) work correctly within the `src.processors` package.
- Updated `FILTERS_CONFIG` in `restorer_gui.py` to dynamically use the new modular processor while maintaining backward compatibility for other filters.

## Intensity Transformation Filters Implementation
- Implemented all point processing filters in `image-restorer/src/processors/intensity.py`.
- All functions follow the `(image, **kwargs)` contract to allow flexible parameter passing from the GUI/orchestrator.
- Used `@ensure_gray` decorator to handle color images by converting them to grayscale before processing and back to BGR after.
- Robust implementation of `contrast_stretching` to handle edge cases like `r1=0` or `r2=255` which would otherwise cause division by zero.
- Verified module loading and imports within the project's virtual environment.

## Spatial Smoothing Filters Implementation
- Implemented `arithmetic_mean_filter`, `median_filter`, and `alpha_trimmed_mean_filter` in `image-restorer/src/processors/spatial/smoothing.py`.
- Used `numpy.lib.stride_tricks.sliding_window_view` for an efficient vectorized implementation of the Alpha-Trimmed Mean Filter.
- Ensured all filters follow the `(image, **kwargs)` contract and use the `@ensure_gray` decorator.
- Verified that `d` pixels are correctly trimmed from the sorted neighborhood in the Alpha-Trimmed Mean Filter (d/2 from each end).
