import sys
import cv2
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame, QScrollArea, QSlider,
    QSpinBox, QDoubleSpinBox, QComboBox, QSizePolicy
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QSize, QCoreApplication, pyqtSignal

import processor

DESTROY_CONFIG = {
    "NOISE EFFECTS": [
        ("Gaussian Noise", processor.add_gaussian_noise, [
            {"arg": "sigma", "label": "Sigma", "type": "int", "min": 1, "max": 100, "default": 10, "suffix": " px"}
        ]),
        ("Salt & Pepper", processor.add_salt_and_pepper_noise, [
            {"arg": "amount", "label": "Amount", "type": "float", "min": 0.001, "max": 0.2, "default": 0.005, "scale": 1000},
            {"arg": "s_vs_p", "label": "Ratio", "type": "float", "min": 0.0, "max": 1.0, "default": 0.5, "scale": 100}
        ]),
        ("Speckle Noise", processor.add_speckle_noise, [
            {"arg": "strength", "label": "Strength", "type": "float", "min": 0.01, "max": 1.0, "default": 0.2, "scale": 100}
        ]),
        ("Periodic Noise", processor.add_periodic_noise, [
            {"arg": "amplitude", "label": "Amplitude", "type": "int", "min": 1, "max": 100, "default": 10, "suffix": " px"},
            {"arg": "frequency", "label": "Frequency", "type": "float", "min": 0.001, "max": 0.5, "default": 0.05, "scale": 1000}
        ]),
        ("Uniform Noise", processor.add_uniform_noise, [
            {"arg": "low", "label": "Low", "type": "int", "min": -100, "max": 0, "default": -20},
            {"arg": "high", "label": "High", "type": "int", "min": 0, "max": 100, "default": 20}
        ]),
        ("Rayleigh Noise", processor.add_rayleigh_noise, [
            {"arg": "scale", "label": "Scale", "type": "int", "min": 1, "max": 100, "default": 10, "suffix": " px"}
        ]),
        ("Exponential Noise", processor.add_exponential_noise, [
            {"arg": "scale", "label": "Scale", "type": "int", "min": 1, "max": 100, "default": 10, "suffix": " px"}
        ]),
    ],
    "TRANSFORMATIONS": [
        ("Grayscale", processor.to_grayscale, []),
        ("Apply Blur", processor.apply_blur, [
            {"arg": "kernel_size", "label": "Kernel Size", "type": "int", "min": 1, "max": 75, "default": 5, "suffix": " px"}
        ]),
    ]
}


class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


class ParameterWidget(QWidget):
    valueChanged = pyqtSignal()

    def __init__(self, metadata, parent=None):
        super().__init__(parent)
        self.arg_name = metadata['arg']
        self.type = metadata['type']
        self.scale = metadata.get('scale', 1)
        self.suffix = metadata.get('suffix', '')

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        label = QLabel(metadata['label'])
        label.setFixedWidth(80)
        layout.addWidget(label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        
        min_val = int(metadata['min'] * self.scale)
        max_val = int(metadata['max'] * self.scale)
        val = int(metadata['default'] * self.scale)
        
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(val)
        
        self.value_label = QLabel(f"{metadata['default']}{self.suffix}")
        self.value_label.setFixedWidth(50)
        
        self.slider.valueChanged.connect(self._update_label)
        self.slider.valueChanged.connect(self.valueChanged.emit)
        
        layout.addWidget(self.slider)
        layout.addWidget(self.value_label)

    def _update_label(self, value):
        display_val = value / self.scale
        formatted_val = f"{display_val:.0f}" if self.scale == 1 else f"{display_val:.2f}"
        self.value_label.setText(f"{formatted_val}{self.suffix}")

    def get_value(self):
        return self.slider.value() / self.scale


class ImageDestroyerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Destroyer")
        self.setMinimumSize(1100, 800)

        self.original_image = None
        self.current_image = None
        self.snapshot = None
        self.history = []
        self.param_widgets = []
        self.is_adjusting = False
        self.sidebar_buttons = []
        
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setObjectName("sidebar")
        
        sidebar_scroll = QScrollArea()
        sidebar_scroll.setWidgetResizable(True)
        sidebar_scroll.setObjectName("sidebar_scroll")
        
        sidebar_container = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(10, 20, 10, 10)
        sidebar_layout.setSpacing(10)

        title = QLabel("IMAGE\nDESTROYER")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)

        self.btn_load = ModernButton("Load Image")
        self.btn_load.clicked.connect(self.load_image)
        sidebar_layout.addWidget(self.btn_load)
        self.sidebar_buttons.append(self.btn_load)

        self.btn_save = ModernButton("Save Image")
        self.btn_save.setObjectName("save_btn")
        self.btn_save.clicked.connect(self.save_image)
        sidebar_layout.addWidget(self.btn_save)
        self.sidebar_buttons.append(self.btn_save)

        self.btn_reset = ModernButton("Reset Image")
        self.btn_reset.setObjectName("reset_btn")
        self.btn_reset.clicked.connect(self.reset_image)
        sidebar_layout.addWidget(self.btn_reset)
        self.sidebar_buttons.append(self.btn_reset)

        sidebar_layout.addSpacing(10)

        # Dynamic filter generation
        for category, items in DESTROY_CONFIG.items():
            self.add_section_label(sidebar_layout, category)
            for name, func, metadata in items:
                self.add_filter_button(
                    sidebar_layout, name, self._make_callback(func, metadata))

        sidebar_layout.addStretch()
        sidebar_scroll.setWidget(sidebar_container)
        
        sidebar_main_layout = QVBoxLayout(sidebar)
        sidebar_main_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_main_layout.addWidget(sidebar_scroll)
        main_layout.addWidget(sidebar)

        preview_container = QWidget()
        self.preview_layout = QVBoxLayout(preview_container)
        self.preview_layout.setContentsMargins(20, 20, 20, 20)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setObjectName("preview_scroll")

        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setObjectName("image_preview")
        self.scroll_area.setWidget(self.image_label)
        
        self.preview_layout.addWidget(self.scroll_area)
        main_layout.addWidget(preview_container)

    def add_section_label(self, layout, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; color: #555; margin-top: 10px;")
        layout.addWidget(label)

    def add_filter_button(self, layout, text, callback):
        btn = ModernButton(text)
        btn.clicked.connect(callback)
        layout.addWidget(btn)
        self.sidebar_buttons.append(btn)

    def _make_callback(self, func, metadata):
        def callback():
            if metadata:
                self.enter_adjustment_mode(metadata, func)
            else:
                self.apply_effect(func)
        return callback

    def set_sidebar_enabled(self, enabled):
        for btn in self.sidebar_buttons:
            btn.setEnabled(enabled)

    def enter_adjustment_mode(self, metadata, func):
        if self.current_image is None or self.is_adjusting:
            return
        
        self.is_adjusting = True
        self.set_sidebar_enabled(False)
        self.snapshot = self.current_image.copy()

        self.adjustment_panel = QWidget()
        self.adjustment_panel.setFixedHeight(50)
        self.adjustment_layout = QHBoxLayout(self.adjustment_panel)
        self.adjustment_layout.setContentsMargins(5, 5, 5, 5)
        
        self.param_widgets = []
        for m in metadata:
            pw = ParameterWidget(m)
            pw.valueChanged.connect(self._run_live_preview)
            self.adjustment_layout.addWidget(pw)
            self.param_widgets.append(pw)
            
        self.btn_apply = ModernButton("Apply")
        self.btn_apply.setFixedSize(60, 30)
        self.btn_apply.clicked.connect(self.apply_adjustment)
        self.adjustment_layout.addWidget(self.btn_apply)
        
        self.btn_cancel = ModernButton("Cancel")
        self.btn_cancel.setFixedSize(60, 30)
        self.btn_cancel.clicked.connect(self.cancel_adjustment)
        self.adjustment_layout.addWidget(self.btn_cancel)

        self.preview_layout.insertWidget(0, self.adjustment_panel)
        
        self.active_filter_func = func
        self._run_live_preview()

    def _run_live_preview(self):
        if self.active_filter_func and self.snapshot is not None:
            kwargs = {pw.arg_name: pw.get_value() for pw in self.param_widgets}
            self.current_image = self.active_filter_func(self.snapshot.copy(), **kwargs)
            self.update_preview()

    def apply_adjustment(self):
        self.snapshot = None
        self.cleanup_adjustment_mode()

    def cancel_adjustment(self):
        if self.snapshot is not None:
            self.current_image = self.snapshot
            self.snapshot = None
            self.update_preview()
        self.cleanup_adjustment_mode()

    def cleanup_adjustment_mode(self):
        if hasattr(self, 'adjustment_panel') and self.adjustment_panel:
            self.adjustment_panel.deleteLater()
            self.adjustment_panel = None
        self.active_filter_func = None
        self.param_widgets = []
        self.is_adjusting = False
        self.set_sidebar_enabled(True)


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
        if self.current_image is not None and not self.is_adjusting:
            self.current_image = effect_func(self.current_image)
            self.update_preview()

    def reset_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.update_preview()

    def create_slider(self, minimum, maximum, value, scaling_factor=1, decimals=0, suffix=""):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(int(minimum * scaling_factor), int(maximum * scaling_factor))
        slider.setValue(int(value * scaling_factor))
        slider.scaling_factor = scaling_factor
        slider.decimals = decimals
        slider.suffix = suffix
        return slider

    def update_preview(self):
        if self.current_image is not None:
            if len(self.current_image.shape) == 3:
                rgb_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_img = QImage(rgb_image.data, w, h,
                               bytes_per_line, QImage.Format.Format_RGB888)
            else:
                h, w = self.current_image.shape
                bytes_per_line = w
                q_img = QImage(self.current_image.data, w, h,
                               bytes_per_line, QImage.Format.Format_Grayscale8)

            pixmap = QPixmap.fromImage(q_img)

            scaled_pixmap = pixmap.scaled(
                self.scroll_area.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setStyleSheet(
                "border: none; background-color: transparent;")


if __name__ == "__main__":
    QCoreApplication.addLibraryPath('/usr/lib/qt6/plugins')
    app = QApplication(sys.argv)
    window = ImageDestroyerGUI()
    window.show()
    sys.exit(app.exec())
