# Plan: Rework `image-restorer` into Modular Engine

## Goal
Implement all filters from `filters.md` in a modularized Python engine while simplifying the GUI and adding a testing infrastructure.

## Architecture
- **Contract-based Functional Engine**: Each filter follows a standard `(image: np.ndarray, **params) -> np.ndarray` signature.
- **Hierarchical Modular Structure**: Logic partitioned into `intensity`, `spatial`, `frequency`, `segmentation` modules.
- **Simplified Registry**: `FILTERS_CONFIG` updated to use static inputs for non-parameterized filters and clear parameter schemas.
- **Error Handling**: Centralized validation for filter parameters and image format compatibility.

## Verification Strategy
- **PoC**: Validate registry-backend contract with one filter per category.
- **Unit Testing**: `pytest` suite for each processing module, utilizing synthetic NumPy images.
- **Automated CI**: GitHub Actions workflow.

## Modular Structure
```text
image-restorer/src/
├── processors/
│   ├── intensity.py
│   ├── spatial/
│   │   ├── smoothing.py
│   │   ├── sharpening.py
│   │   └── advanced.py
│   ├── frequency.py
│   ├── segmentation.py
│   └── utils.py
└── ...
```

## Tasks

1. [x] Setup `pytest` environment and create `src/` directory structure.
2. [x] Implement `src/processors/utils.py` with `@ensure_gray` and a parameter validator contract.
3. [x] Develop PoC: Create `src/processors/intensity.py`, implement `NegativeImage`, and update `restorer_gui.py` to use the new static/dynamic input registry.
4. Implement full `src/processors/intensity.py` including all intensity filters.
5. Implement `src/processors/spatial/smoothing.py` (Averaging, Median, Alpha-Trimmed).
6. Implement `src/processors/spatial/sharpening.py` (Laplacian, Sobel, Prewitt, Roberts).
7. Implement `src/processors/spatial/advanced.py` (Geometric/Harmonic/Contraharmonic/Max/Min/Midpoint/Adaptive).
8. Implement `src/processors/frequency.py` (Ideal/Butterworth/Gaussian Low/High Pass variants, Band Reject).
9. Implement `src/processors/segmentation.py` (Point and Line detection).
10. Update all `FILTERS_CONFIG` in `restorer_gui.py`, simplify inputs (static vs. dynamic).
11. [PERMISSION REQUIRED] Create `pytest` suite for all modules and setup GitHub Actions CI workflow.


## Final Verification Wave
- Automated tests pass.
- All 30+ filters from `filters.md` registered.
- GUI dynamic input generation handles static/dynamic cases.
- Performance meets baseline.

---
## Decions Needed
- None. The plan addresses Metis recommendations through the PoC phase and standardized engine contract.
