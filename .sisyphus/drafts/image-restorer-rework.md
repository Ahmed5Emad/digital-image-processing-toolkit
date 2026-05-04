# Plan: Rework `image-restorer`

## Goal
Implement all filters listed in `filters.md` and establish a robust, testable architecture for the `image-restorer` project.

## Current State
- **Architecture**: Registry-Driven Functional Pipeline (`restorer_gui.py` -> `restorer_processor.py`).
- **Testing**: Zero automation.
- **Coverage**: Missing Frequency Domain filters, Segmentation masks, and advanced spatial filters. Some existing filters are not exposed in the GUI.

## Proposed Scope
1. **Infrastructure**: Setup `pytest` for unit testing the processing engine.
2. **Implementation Wave 1 (Intensity & Spatial)**: Add Alpha-Trimmed Mean, Adaptive Median. Expose existing hidden filters.
3. **Implementation Wave 2 (Frequency Domain)**: Add missing Low Pass (Ideal, Butterworth, Gaussian) and High Pass (Ideal, Gaussian) filters.
4. **Implementation Wave 3 (Segmentation)**: Add Point and Line detection masks.
5. **CI/CD**: Add GitHub Actions workflow for automated test execution.

## Key Decisions Needed
- Prioritization of filter waves?
- Testing framework preference?
- GUI limitations for advanced filters (e.g., frequency spectrum visualization)?
