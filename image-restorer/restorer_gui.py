import sys
import cv2
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame, QScrollArea, QSpacerItem, QSizePolicy,
    QSlider, QSpinBox, QDoubleSpinBox, QComboBox
)
from PyQt6.QtGui import QImage, QPixmap, QFont, QColor, QPalette
from PyQt6.QtCore import Qt, QSize, QCoreApplication, QTimer, pyqtSignal

from src.processors import intensity, frequency
from src.processors.spatial import smoothing, sharpening, advanced
from src.processors.utils import ensure_gray


FILTERS_CONFIG = {
    "POINT": [
        ("Negative", intensity.negative, []),
        ("Thresholding", intensity.thresholding, [
            {"arg": "threshold_value", "label": "Threshold",
                "type": "int", "min": 0, "max": 255, "default": 127},
            {"arg": "max_value", "label": "Max Value",
                "type": "int", "min": 0, "max": 255, "default": 255}
        ]),
        ("Log", intensity.log_transformation, []),
        ("Inverse Log", intensity.inverse_log_transformation, []),
        ("Gamma", intensity.gamma_transformation, [
            {"arg": "gamma", "label": "Gamma", "type": "float",
                "min": 0.1, "max": 5.0, "default": 1.2}
        ]),
        ("Contrast Stretching", intensity.contrast_stretching, [
            {"arg": "r1", "label": "r1", "type": "int",
                "min": 0, "max": 255, "default": 0},
            {"arg": "s1", "label": "s1", "type": "int",
                "min": 0, "max": 255, "default": 0},
            {"arg": "r2", "label": "r2", "type": "int",
                "min": 0, "max": 255, "default": 255},
            {"arg": "s2", "label": "s2", "type": "int",
                "min": 0, "max": 255, "default": 255}
        ]),
        ("Gray Level Slicing", intensity.gray_level_slicing, [
            {"arg": "r1", "label": "r1", "type": "int",
                "min": 0, "max": 255, "default": 100},
            {"arg": "r2", "label": "r2", "type": "int",
                "min": 0, "max": 255, "default": 200}
        ]),
        ("Bit Plane Slicing", intensity.bit_plane_slicing, [
            {"arg": "plane", "label": "Plane", "type": "int",
                "min": 0, "max": 7, "default": 7}
        ]),
    ],
    "HISTOGRAM": [
        ("Equalization", intensity.histogram_equalization, []),
    ],
    "SMOOTHING": [
        ("Arithmetic Mean", smoothing.arithmetic_mean_filter, [
            {"arg": "kernel_size", "label": "Kernel Size",
                "type": "odd", "min": 1, "max": 31, "default": 3}
        ]),
        ("Median", smoothing.median_filter, [
            {"arg": "kernel_size", "label": "Kernel Size",
                "type": "odd", "min": 1, "max": 31, "default": 3}
        ]),
    ],
    "SHARPENING": [
        ("Laplacian", sharpening.laplacian_sharpening, [
            {"arg": "blend_mode", "label": "Blend Mode", "type": "choice",
             "choices": ["Edges Only", "Add (+)", "Subtract (-)"], "default": "Subtract (-)"}
        ]),
        ("Sobel", sharpening.sobel_sharpening, [
            {"arg": "ksize", "label": "Kernel Size",
                "type": "odd", "min": 1, "max": 31, "default": 3},
            {"arg": "blend_mode", "label": "Blend Mode", "type": "choice",
             "choices": ["Edges Only", "Add (+)", "Subtract (-)"], "default": "Add (+)"}
        ]),
    ],
    "ADVANCED RESTORATION": [
        ("Geometric Mean", advanced.geometric_mean_filter, [
            {"arg": "kernel_size", "label": "Kernel Size",
                "type": "odd", "min": 1, "max": 31, "default": 3}
        ]),
        ("Harmonic Mean", advanced.harmonic_mean_filter, [
            {"arg": "kernel_size", "label": "Kernel Size",
                "type": "odd", "min": 1, "max": 31, "default": 3}
        ]),
        ("Contraharmonic Mean", advanced.contraharmonic_mean_filter, [
            {"arg": "kernel_size", "label": "Kernel Size",
                "type": "odd", "min": 1, "max": 31, "default": 3},
            {"arg": "Q", "label": "Q Factor", "type": "float",
                "min": -10.0, "max": 10.0, "default": 1.5}
        ]),
        ("Max", advanced.max_filter, [
            {"arg": "kernel_size", "label": "Kernel Size",
             "type": "odd", "min": 1, "max": 31, "default": 3}
        ]),
        ("Min", advanced.min_filter, [
            {"arg": "kernel_size", "label": "Kernel Size",
                "type": "odd", "min": 1, "max": 31, "default": 3}
        ]),
        ("Midpoint", advanced.midpoint_filter, [
            {"arg": "kernel_size", "label": "Kernel Size",
                "type": "odd", "min": 1, "max": 31, "default": 3}
        ]),
        ("Adaptive Median", advanced.adaptive_median_filter, [
            {"arg": "S_max", "label": "S Max", "type": "int",
                "min": 3, "max": 31, "default": 7}
        ]),
    ],
    "FREQUENCY": [
        {
            "group": "Ideal",
            "filters": [
                ("Lowpass", frequency.ideal_lowpass_filter, [
                    {"arg": "cutoff", "label": "Cutoff", "type": "int",
                        "min": 1, "max": 200, "default": 30}
                ]),
                ("Highpass", frequency.ideal_highpass_filter, [
                    {"arg": "cutoff", "label": "Cutoff", "type": "int",
                        "min": 1, "max": 200, "default": 30},
                    {"arg": "blend_mode", "label": "Blend Mode", "type": "choice",
                     "choices": ["Edges Only", "Add (+)", "Subtract (-)"], "default": "Add (+)"}
                ]),
                ("Bandreject", frequency.ideal_bandreject_filter, [
                    {"arg": "cutoff_low", "label": "Cutoff Low",
                        "type": "int", "min": 1, "max": 200, "default": 30},
                    {"arg": "cutoff_high", "label": "Cutoff High",
                        "type": "int", "min": 1, "max": 200, "default": 60}
                ]),
            ]
        },
        {
            "group": "Butterworth",
            "filters": [
                ("Lowpass", frequency.butterworth_lowpass_filter, [
                    {"arg": "cutoff", "label": "Cutoff", "type": "int",
                        "min": 1, "max": 200, "default": 30},
                    {"arg": "n", "label": "Order", "type": "int",
                        "min": 1, "max": 10, "default": 2}
                ]),
                ("Highpass", frequency.butterworth_highpass_filter, [
                    {"arg": "cutoff", "label": "Cutoff", "type": "int",
                        "min": 1, "max": 200, "default": 30},
                    {"arg": "n", "label": "Order", "type": "int",
                        "min": 1, "max": 10, "default": 2},
                    {"arg": "blend_mode", "label": "Blend Mode", "type": "choice",
                     "choices": ["Edges Only", "Add (+)", "Subtract (-)"], "default": "Add (+)"}
                ]),
                ("Bandreject", frequency.butterworth_bandreject_filter, [
                    {"arg": "cutoff_low", "label": "Cutoff Low",
                        "type": "int", "min": 1, "max": 200, "default": 30},
                    {"arg": "cutoff_high", "label": "Cutoff High",
                        "type": "int", "min": 1, "max": 200, "default": 60},
                    {"arg": "n", "label": "Order", "type": "int",
                        "min": 1, "max": 10, "default": 2}
                ]),
            ]
        },
        {
            "group": "Gaussian",
            "filters": [
                ("Lowpass", frequency.gaussian_lowpass_filter, [
                    {"arg": "cutoff", "label": "Cutoff", "type": "int",
                        "min": 1, "max": 200, "default": 30}
                ]),
                ("Highpass", frequency.gaussian_highpass_filter, [
                    {"arg": "cutoff", "label": "Cutoff", "type": "int",
                        "min": 1, "max": 200, "default": 30},
                    {"arg": "blend_mode", "label": "Blend Mode", "type": "choice",
                     "choices": ["Edges Only", "Add (+)", "Subtract (-)"], "default": "Add (+)"}
                ]),
                ("Bandreject", frequency.gaussian_bandreject_filter, [
                    {"arg": "cutoff_low", "label": "Cutoff Low",
                        "type": "int", "min": 1, "max": 200, "default": 30},
                    {"arg": "cutoff_high", "label": "Cutoff High",
                        "type": "int", "min": 1, "max": 200, "default": 60}
                ]),
            ]
        },
    ]
}


class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Fixed)


class ParameterWidget(QWidget):
    valueChanged = pyqtSignal()

    def __init__(self, metadata, parent=None):
        super().__init__(parent)
        self.arg_name = metadata['arg']
        self.type = metadata['type']

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(10)

        label = QLabel(metadata['label'])
        label.setFixedWidth(100)
        label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(label)

        if self.type == 'choice':
            self.combo = QComboBox()
            for choice in metadata['choices']:
                self.combo.addItem(choice)
            self.combo.setCurrentText(metadata['default'])
            self.combo.currentTextChanged.connect(self.valueChanged.emit)
            layout.addWidget(self.combo)
            return

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimumHeight(20)

        if self.type == 'float':
            self.spin = QDoubleSpinBox()
            self.spin.setRange(metadata['min'], metadata['max'])
            self.spin.setSingleStep(0.1)
            self.spin.setValue(metadata['default'])

            # Slider scaling for float (0.1 precision)
            self.slider.setRange(int(metadata['min'] * 10),
                                 int(metadata['max'] * 10))
            self.slider.setValue(int(metadata['default'] * 10))

            self.spin.valueChanged.connect(
                lambda v: self.block_and_set(self.slider, int(v * 10)))
            self.slider.valueChanged.connect(
                lambda v: self.block_and_set(self.spin, v / 10.0))
        else:
            self.spin = QSpinBox()
            self.spin.setRange(metadata['min'], metadata['max'])
            self.spin.setValue(metadata['default'])

            if self.type == 'odd':
                self.spin.setSingleStep(2)
                if self.spin.value() % 2 == 0:
                    self.spin.setValue(self.spin.value() + 1)

            self.slider.setRange(metadata['min'], metadata['max'])
            self.slider.setValue(self.spin.value())

            self.spin.valueChanged.connect(
                lambda v: self.block_and_set(self.slider, v))
            self.slider.valueChanged.connect(
                lambda v: self.block_and_set(self.spin, v))

            if self.type == 'odd':
                self.slider.valueChanged.connect(self._ensure_odd)
                self.spin.valueChanged.connect(self._ensure_odd)

        self.spin.setFixedWidth(60)
        layout.addWidget(self.slider)
        layout.addWidget(self.spin)

        self.spin.valueChanged.connect(self.valueChanged.emit)
        self.slider.valueChanged.connect(self.valueChanged.emit)

    def block_and_set(self, widget, value):
        widget.blockSignals(True)
        if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
            widget.setValue(value)
        else:
            widget.setValue(int(value))
        widget.blockSignals(False)

    def _ensure_odd(self, value):
        if value % 2 == 0:
            new_val = value + 1
            if new_val > self.spin.maximum():
                new_val = value - 1
            self.spin.setValue(new_val)
            self.slider.setValue(new_val)

    def get_value(self):
        if self.type == 'choice':
            return self.combo.currentText()
        return self.spin.value()


class ImageRestorerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Restorer")
        self.setMinimumSize(1100, 800)

        self.original_image = None
        self.current_image = None
        self.snapshot = None
        self.history = []
        self.sidebar_buttons = []
        self.active_filter_metadata = None
        self.active_filter_func = None
        self.active_category = None
        self.param_widgets = []

        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self._run_live_preview)

        self.validate_config()
        self.init_ui()

    def validate_config(self):
        """Validates FILTERS_CONFIG for metadata consistency."""
        required_numeric_keys = {"arg", "label", "type", "min", "max", "default"}
        required_choice_keys = {"arg", "label", "type", "choices", "default"}
        valid_types = {"int", "float", "odd", "choice"}

        def validate_filter(name, func, metadata):
            if not isinstance(metadata, list):
                print(f"Config Error: Metadata for {name} must be a list.")
                return
            for param in metadata:
                if param.get("type") == "choice":
                    missing = required_choice_keys - set(param.keys())
                else:
                    missing = required_numeric_keys - set(param.keys())

                if missing:
                    print(f"Config Error: {name} param missing keys: {missing}")
                    continue

                if param["type"] not in valid_types:
                    print(f"Config Error: {name} has invalid type: {param['type']}")

                if param["type"] != "choice":
                    if not (param["min"] <= param["default"] <= param["max"]):
                        print(f"Config Error: {name} default {param['default']} out of range.")

        for category, items in FILTERS_CONFIG.items():
            for item in items:
                if isinstance(item, dict):
                    group_label = item.get("group")
                    filters = item.get("filters")
                    if not group_label or not filters:
                        print(f"Config Error: Group in {category} missing 'group' or 'filters'.")
                        continue
                    for name, func, metadata in filters:
                        validate_filter(f"{group_label} -> {name}", func, metadata)
                else:
                    name, func, metadata = item
                    validate_filter(name, func, metadata)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setObjectName("sidebar")

        sidebar_scroll = QScrollArea()
        sidebar_scroll.setWidgetResizable(True)
        sidebar_scroll.setObjectName("sidebar_scroll")
        sidebar_scroll.setStyleSheet(
            "QScrollArea { border: none; background-color: transparent; }")

        sidebar_container = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(10, 20, 0, 10)
        sidebar_layout.setSpacing(10)

        title = QLabel("IMAGE RESTORER")
        title.setObjectName("title")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)

        sidebar_layout.addSpacing(5)

        header_layout = QHBoxLayout()
        self.btn_save = ModernButton("Save Image")
        self.btn_save.setObjectName("save_btn")
        self.btn_save.clicked.connect(self.save_image)
        header_layout.addWidget(self.btn_save)
        self.sidebar_buttons.append(self.btn_save)

        self.btn_reset = ModernButton("Reset Image")
        self.btn_reset.setObjectName("reset_btn")
        self.btn_reset.clicked.connect(self.reset_image)
        header_layout.addWidget(self.btn_reset)
        self.sidebar_buttons.append(self.btn_reset)
        sidebar_layout.addLayout(header_layout)

        self.btn_load = ModernButton("Load Image")
        self.btn_load.clicked.connect(self.load_image)
        sidebar_layout.addWidget(self.btn_load)
        self.sidebar_buttons.append(self.btn_load)

        sidebar_layout.addSpacing(10)

        # Dynamic filter generation
        for category, items in FILTERS_CONFIG.items():
            self.add_section_label(sidebar_layout, category)
            for item in items:
                if isinstance(item, dict):
                    self.add_grouped_filter(
                        sidebar_layout, item["group"], item["filters"], category)
                else:
                    name, func, metadata = item
                    self.add_filter_button(
                        sidebar_layout, name, self._make_callback(func, metadata, category))

        sidebar_layout.addStretch()
        sidebar_scroll.setWidget(sidebar_container)

        sidebar_main_layout = QVBoxLayout(sidebar)
        sidebar_main_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_main_layout.addWidget(sidebar_scroll)

        main_layout.addWidget(sidebar)

        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.top_bar_widget = QFrame()
        self.top_bar_widget.setFixedHeight(50)
        self.top_bar_widget.setObjectName("top_bar")
        top_bar_layout = QHBoxLayout(self.top_bar_widget)
        top_bar_layout.setContentsMargins(10, 0, 10, 0)
        top_bar_layout.setSpacing(10)

        # Control container for parameters
        self.control_container = QWidget()
        self.control_layout = QHBoxLayout(self.control_container)
        self.control_layout.setContentsMargins(0, 0, 0, 0)
        self.control_layout.setSpacing(20)
        self.control_container.hide()
        top_bar_layout.addWidget(self.control_container)

        top_bar_layout.addStretch()

        # Action buttons (Apply, Reset, Cancel)
        self.action_buttons = QWidget()
        self.action_buttons.setFixedWidth(230)
        self.action_layout = QHBoxLayout(self.action_buttons)
        self.action_layout.setContentsMargins(0, 0, 0, 0)
        self.action_layout.setSpacing(5)

        self.btn_apply = ModernButton("Apply")
        self.btn_apply.setFixedWidth(70)
        self.btn_apply.setFixedHeight(30)
        self.btn_apply.setObjectName("apply_btn")
        self.btn_apply.clicked.connect(self.apply_active_filter)

        self.btn_reset_params = ModernButton("Reset")
        self.btn_reset_params.setFixedWidth(70)
        self.btn_reset_params.setFixedHeight(30)
        self.btn_reset_params.setObjectName("reset_params_btn")
        self.btn_reset_params.clicked.connect(self.reset_active_params)

        self.btn_cancel = ModernButton("Cancel")
        self.btn_cancel.setFixedWidth(70)
        self.btn_cancel.setFixedHeight(30)
        self.btn_cancel.setObjectName("cancel_btn")
        self.btn_cancel.clicked.connect(self.hide_top_panel)

        self.action_layout.addWidget(self.btn_apply)
        self.action_layout.addWidget(self.btn_reset_params)
        self.action_layout.addWidget(self.btn_cancel)
        self.action_buttons.hide()
        top_bar_layout.addWidget(self.action_buttons)

        self.btn_undo = ModernButton("⟲")
        self.btn_undo.setStyleSheet("font-size: 20px;")
        self.btn_undo.setFixedSize(35, 35)
        self.btn_undo.clicked.connect(self.undo_last_effect)
        top_bar_layout.addWidget(self.btn_undo)

        right_layout.addWidget(self.top_bar_widget)

        preview_container = QWidget()
        preview_layout = QHBoxLayout(preview_container)

        self.original_scroll = QScrollArea()
        self.original_scroll.setWidgetResizable(True)
        self.original_scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_scroll.setObjectName("preview_scroll")
        self.original_label = QLabel("No image loaded")
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_scroll.setWidget(self.original_label)

        self.restored_scroll = QScrollArea()
        self.restored_scroll.setWidgetResizable(True)
        self.restored_scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.restored_scroll.setObjectName("preview_scroll")
        self.restored_label = QLabel("No image loaded")
        self.restored_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.restored_scroll.setWidget(self.restored_label)

        preview_layout.addWidget(self.original_scroll)
        preview_layout.addWidget(self.restored_scroll)
        right_layout.addWidget(preview_container)
        main_layout.addWidget(right_container)

    def enter_adjustment_mode(self, metadata, func, category, group_filters=None):
        if self.current_image is None:
            return

        self.snapshot = self.current_image.copy()
        self.toggle_sidebar(False)
        self.active_category = category

        while self.control_layout.count():
            item = self.control_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.param_widgets = []

        if group_filters:
            variant_combo = QComboBox()
            variant_combo.setFixedWidth(150)
            for name, f, m in group_filters:
                variant_combo.addItem(name)

            variant_combo.currentIndexChanged.connect(
                lambda idx: self._rebuild_params(
                    group_filters[idx][1], group_filters[idx][2])
            )
            self.control_layout.addWidget(variant_combo)

            self._rebuild_params(group_filters[0][1], group_filters[0][2])
        else:
            self._rebuild_params(func, metadata)

        self.control_container.show()
        self.action_buttons.show()
        self.btn_undo.hide()

    def _rebuild_params(self, func, metadata):
        self.active_filter_func = func
        self.active_filter_metadata = metadata

        for pw in self.param_widgets:
            self.control_layout.removeWidget(pw)
            pw.deleteLater()
        self.param_widgets = []

        for m in metadata:
            pw = ParameterWidget(m)
            pw.valueChanged.connect(self.live_preview)
            self.control_layout.addWidget(pw)
            self.param_widgets.append(pw)

        self.live_preview()

    def live_preview(self):
        if self.active_category == "FREQUENCY":
            self.preview_timer.start(300)
        else:
            self._run_live_preview()

    def _run_live_preview(self):
        if self.active_filter_func and self.snapshot is not None:
            kwargs = {pw.arg_name: pw.get_value() for pw in self.param_widgets}
            try:
                self.current_image = self.active_filter_func(
                    self.snapshot.copy(), **kwargs)
                self.update_preview()
                self.restored_scroll.setStyleSheet("")
            except Exception as e:
                print(f"Live preview error: {e}")
                self.restored_scroll.setStyleSheet("border: 2px solid red;")

    def toggle_sidebar(self, enabled):
        if not enabled:
            self.setFocus()
        for btn in self.sidebar_buttons:
            btn.setEnabled(enabled)

    def apply_active_filter(self):
        if self.active_filter_func and self.snapshot is not None:
            self.history.append(self.snapshot)
            self.snapshot = None
            self.hide_top_panel()

    def reset_active_params(self):
        if self.active_filter_metadata:
            for pw in self.param_widgets:
                for m in self.active_filter_metadata:
                    if m['arg'] == pw.arg_name:
                        if pw.type == 'choice':
                            pw.combo.setCurrentText(m['default'])
                        else:
                            pw.spin.setValue(m['default'])
                        break
            self.live_preview()

    def hide_top_panel(self):
        if self.snapshot is not None:
            self.current_image = self.snapshot
            self.snapshot = None
            self.update_preview()

        self.control_container.hide()
        self.action_buttons.hide()
        self.btn_undo.show()
        self.toggle_sidebar(True)
        self.active_filter_metadata = None
        self.active_filter_func = None
        self.active_category = None
        self.param_widgets = []
        self.restored_scroll.setStyleSheet("")

    def add_section_label(self, layout, text):
        label = QLabel(text)
        label.setObjectName("section_label")
        layout.addWidget(label)

    def add_filter_button(self, layout, text, callback):
        btn = ModernButton(text)
        btn.clicked.connect(callback)
        layout.addWidget(btn)
        self.sidebar_buttons.append(btn)

    def add_grouped_filter(self, layout, group_label, filters, category):
        wrapped_filters = [(name, ensure_gray(func), metadata)
                           for name, func, metadata in filters]
        btn = ModernButton(group_label)
        btn.clicked.connect(lambda: self.enter_adjustment_mode(
            None, None, category, group_filters=wrapped_filters))
        layout.addWidget(btn)
        self.sidebar_buttons.append(btn)

    def _make_callback(self, func, metadata, category):
        wrapped_func = ensure_gray(func)

        def callback():
            if metadata:
                self.enter_adjustment_mode(metadata, wrapped_func, category)
            else:
                self.apply_effect(wrapped_func)
        return callback

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if file_path:
            self.original_image = cv2.imread(file_path)
            if self.original_image is not None:
                self.current_image = self.original_image.copy()
                self.update_preview()

    def save_image(self):
        if self.current_image is not None:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Image", "", "PNG Files (*.png);;JPG Files (*.jpg);;All Files (*)"
            )
            if file_path:
                cv2.imwrite(file_path, self.current_image)

    def apply_effect(self, effect_func):
        if self.current_image is not None:
            try:
                self.history.append(self.current_image.copy())
                self.current_image = effect_func(self.current_image)
                self.update_preview()
            except Exception as e:
                print(f"Error applying effect: {e}")
                self.history.pop()

    def undo_last_effect(self):
        if self.history:
            self.current_image = self.history.pop()
            self.update_preview()

    def reset_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.history = []
            self.update_preview()

    def _display_image(self, image, label, scroll_area):
        if image is not None:
            if len(image.shape) == 3:
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_img = QImage(rgb_image.data, w, h,
                               bytes_per_line, QImage.Format.Format_RGB888)
            else:
                h, w = image.shape
                bytes_per_line = w
                q_img = QImage(image.data, w, h, bytes_per_line,
                               QImage.Format.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)

            scaled_pixmap = pixmap.scaled(
                scroll_area.size() - QSize(20, 20),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            label.setPixmap(scaled_pixmap)
            label.setStyleSheet("border: none; background-color: transparent;")

    def update_preview(self):
        self._display_image(self.original_image,
                            self.original_label, self.original_scroll)
        self._display_image(self.current_image,
                            self.restored_label, self.restored_scroll)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_image is not None:
            self.update_preview()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.action_buttons.isVisible():
                self.hide_top_panel()
        super().keyPressEvent(event)


if __name__ == "__main__":
    QCoreApplication.addLibraryPath('/usr/lib/qt6/plugins')

    app = QApplication(sys.argv)
    window = ImageRestorerGUI()
    window.show()
    sys.exit(app.exec())
