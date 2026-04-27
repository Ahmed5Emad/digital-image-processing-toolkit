# Work Plan: Fix Filter Control Bugs

Address reported issues with the new dynamic filter controls, including slider functionality, UI spacing, and keyboard shortcuts.

## 1. Context & Objectives
Users report that sliders for Threshold, Gamma, Q-factor, and Butterworth filters are not updating the image. Additionally, the top bar is too tall, buttons are far apart, and the Escape key does not cancel the adjustment mode.

### Success Criteria:
- All sliders and spinboxes correctly trigger real-time image updates.
- Top bar height reduced to 40px.
- Apply/Reset/Cancel buttons grouped together.
- Escape key cancels adjustment mode.

## 2. Technical Decisions
- **Signal Refactoring**: Add a custom `pyqtSignal` named `valueChanged` to the `ParameterWidget` class. Emit this signal whenever the slider or spinbox is changed. Connect this signal to the GUI's `live_preview`.
- **UI Tightening**: Reduce `top_bar_widget` height. Wrap the action buttons in a fixed-width container to prevent them from spreading across the layout.
- **Shortcut Handling**: Override `keyPressEvent` in the main window to detect `Qt.Key.Key_Escape`.

## 3. Implementation Steps

### Phase 1: ParameterWidget Fixes
1. Modify `ParameterWidget` in `image-restorer/restorer_gui.py`:
   - Import `pyqtSignal`.
   - Add `valueChanged = pyqtSignal()`.
   - Connect both `self.spin.valueChanged` and `self.slider.valueChanged` to `self.valueChanged.emit`.
   - Reduce font sizes and margins for a more compact look.

### Phase 2: UI Compactness
2. Update `ImageRestorerGUI.init_ui`:
   - Reduce `top_bar_widget.setFixedHeight` to 40.
   - Reduce `ModernButton` minimum height to 30.
   - Set fixed width for `self.action_buttons` (approx. 230px).
   - Adjust layout spacings (reduce from 10/20 to 5).

### Phase 3: Logic & Shortcuts
3. Update `ImageRestorerGUI.enter_adjustment_mode`:
   - Connect `pw.valueChanged` (the new custom signal) to `self.live_preview` instead of only the spinbox.
4. Add `keyPressEvent` to `ImageRestorerGUI`:
   - If key is `Qt.Key.Key_Escape` and adjustment mode is active, call `hide_top_panel()`.

## 4. Acceptance Tests
- **Sliders**: Move "Threshold" slider; verify image updates instantly.
- **Float Parameters**: Adjust "Gamma"; verify image updates and spinbox shows decimal precision.
- **Top Bar**: Measure height; verify it is slimmer and buttons are close together.
- **Keyboard**: Enter "Gaussian Filter" mode -> Press ESC; verify mode closes and sidebar re-enables.

## 5. Final Verification Wave
- [x] No regression in "Undo" history.
- [x] Sliders and Spinboxes remain perfectly synced.
- [x] No layout "jumps" when entering/exiting adjustment mode.
