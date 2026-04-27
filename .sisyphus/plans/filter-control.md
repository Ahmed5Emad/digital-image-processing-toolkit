# Work Plan: Dynamic Filter Control for Image Restorer

Implement a metadata-driven UI that provides real-time control over image processing parameters using PyQt6 sliders and spinboxes.

## 1. Context & Objectives
The current `ImageRestorerGUI` applies filters with hardcoded or default parameters. This plan adds a "Parameter Panel" that dynamically populates based on the selected filter, allowing users to tune results in real-time.

### Success Criteria:
- Metadata-driven UI (no hardcoding of individual sliders).
- Real-time preview updates during slider movement.
- Preservation of "Undo" history (only committing the final result).
- Enforcement of mathematical constraints (e.g., odd kernel sizes).

## 2. Technical Decisions
- **Metadata Structure**: `FILTERS_CONFIG` will be expanded to include a list of dictionaries defining `name`, `type` (int, float, odd), `min`, `max`, and `default`.
- **Preview Snapshot**: When a filter is clicked, the app stores a copy of the current image. All slider adjustments apply to this copy, preventing cumulative error or history bloat.
- **Workflow Mode**: Selection of a filter enters "Adjustment Mode." Other filter buttons are disabled. User must click "Apply" (pushes to history) or "Cancel" (reverts to snapshot).

## 3. Implementation Steps

### Phase 1: Metadata Definition
1. Update `image-restorer/restorer_gui.py` to redefine `FILTERS_CONFIG`. [x]
   - Add parameters for: Threshold, Gamma, Sigma, Kernel Size, and Highpass Cutoff.
   - Example: `("Gaussian", processor.gaussian, [{"arg": "kernel_size", "label": "Kernel", "type": "odd", "min": 1, "max": 31, "default": 5}, ...])`

### Phase 2: UI Expansion (Top Bar Panel)
2. Create `ParameterWidget(QWidget)` class to encapsulate a Label, Slider, and SpinBox in a compact horizontal layout. [x]
3. Refactor `ImageRestorerGUI` top bar: [x]
   - Create a `self.control_container` (QHBoxLayout) in the top bar area.
   - This container will be hidden by default.
4. Implement `rebuild_top_panel(metadata)`: [x]
   - Clears the horizontal container.
   - Injects the active filter name and a `ParameterWidget` for each metadata entry.
   - Injects the Apply/Reset/Cancel buttons.

### Phase 3: Real-time Logic & Workflow
- [x] 5. Update `ImageRestorerGUI` state.
- [x] 6. Refactor button callbacks.
- [x] 7. Implement "Apply", "Reset", and "Cancel" buttons.

### Phase 4: Performance & Safety
- [x] 8. Add a `try/except` block in the preview loop to catch invalid OpenCV operations.
- [x] 9. Implement a "Debounce" for expensive filters (e.g., Frequency Domain) using `QTimer`.
- [x] 10. Add a startup validation check to ensure metadata (min/max/default) is consistent.

## 4. Acceptance Tests
- **Gaussian Blur**: Verify slider moves in steps of 2 (odd numbers).
- **Gamma**: Verify real-time updates with float values (e.g., 0.1 to 5.0).
- **Undo**: Apply a filter -> Undo. Verify it returns to the state *before* the adjustment mode started.
- **Robustness**: Rapidly move the slider for Butterworth Highpass; ensure the app doesn't crash or freeze.

## 5. Final Verification Wave
- [x] UI correctly maps all parameters defined in metadata.
- [x] "Apply" button is required to save changes to history.
- [x] No OpenCV errors for kernel_size=0 or even numbers.
