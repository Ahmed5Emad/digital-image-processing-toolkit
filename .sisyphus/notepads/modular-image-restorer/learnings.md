# Modular Image Restorer Learnings

## Utilities
- Implemented `ensure_gray` decorator using `functools.wraps` to preserve function metadata.
- Implemented `validate_params` for parameter clamping and type conversion based on a schema `(type, min, max)`.
- Cleaned up code by removing unnecessary docstrings and comments as per project standards.

## Modularization PoC
- Successfully moved the `negative` filter to a dedicated `src/processors/intensity.py` module.
- Verified that relative imports (`from .utils import ensure_gray`) work correctly within the `src.processors` package.
- Updated `FILTERS_CONFIG` in `restorer_gui.py` to dynamically use the new modular processor while maintaining backward compatibility for other filters.
