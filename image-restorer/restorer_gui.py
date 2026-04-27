import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame, QScrollArea, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QImage, QPixmap, QFont, QColor, QPalette
from PyQt6.QtCore import Qt, QSize, QCoreApplication

import restorer_processor as processor


FILTERS_CONFIG = {
    "POINT": [
        ("Negative", processor.negative),
        ("Thresholding", lambda img: processor.thresholding(img, 127)),
        ("Log Transform", processor.log_transformation),
        ("Gamma Transform", processor.gamma_transformation),
    ],
    "HISTOGRAM": [
        ("Equalization", processor.histogram_equalization),
    ],
    "SMOOTHING": [
        ("Arithmetic Mean", processor.arithmetic_mean_filter),
        ("Geometric Mean", processor.geometric_mean_filter),
        ("Harmonic Mean", processor.harmonic_mean_filter),
        ("Contraharmonic Mean", processor.contraharmonic_mean_filter),
        ("Gaussian Filter", processor.gaussian_filter),
        ("Bilateral Filter", processor.bilateral_filter),
        ("Box Filter", processor.box_filter),
    ],
    "ORDER": [
        ("Median Filter", processor.median_filter),
        ("Min Filter", processor.min_filter),
        ("Max Filter", processor.max_filter),
        ("Midpoint Filter", processor.midpoint_filter),
    ],
    "SHARPENING": [
        ("Laplacian", processor.laplacian_sharpening),
        ("Sobel", processor.sobel_sharpening),
        ("Prewitt", processor.prewitt_sharpening),
        ("Roberts", processor.roberts_sharpening),
    ],
    "FREQUENCY": [
        ("Butterworth High", processor.butterworth_highpass_filter),
    ]
}


class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Fixed)


class ImageRestorerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Restorer")
        self.setMinimumSize(1100, 800)

        self.original_image = None
        self.current_image = None
        self.history = []

        self.init_ui()

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

        self.btn_reset = ModernButton("Reset Image")
        self.btn_reset.setObjectName("reset_btn")
        self.btn_reset.clicked.connect(self.reset_image)
        header_layout.addWidget(self.btn_reset)
        sidebar_layout.addLayout(header_layout)

        self.btn_load = ModernButton("Load Image")
        self.btn_load.clicked.connect(self.load_image)
        sidebar_layout.addWidget(self.btn_load)

        sidebar_layout.addSpacing(10)

        # Dynamic filter generation
        for category, filters in FILTERS_CONFIG.items():
            self.add_section_label(sidebar_layout, category)
            for name, func in filters:
                self.add_filter_button(
                    sidebar_layout, name, self._make_callback(func))

        sidebar_layout.addStretch()
        sidebar_scroll.setWidget(sidebar_container)

        sidebar_main_layout = QVBoxLayout(sidebar)
        sidebar_main_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_main_layout.addWidget(sidebar_scroll)

        main_layout.addWidget(sidebar)

        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 10, 10, 0)
        top_bar.addStretch()

        self.btn_undo = ModernButton("⟲")
        self.btn_undo.setStyleSheet("font-size: 24px;")
        self.btn_undo.setFixedSize(45, 45)
        self.btn_undo.clicked.connect(self.undo_last_effect)

        top_bar.addWidget(self.btn_undo)

        right_layout.addLayout(top_bar)

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

    def add_section_label(self, layout, text):
        label = QLabel(text)
        label.setObjectName("section_label")
        layout.addWidget(label)

    def add_filter_button(self, layout, text, callback):
        btn = ModernButton(text)
        btn.clicked.connect(callback)
        layout.addWidget(btn)

    def _make_callback(self, func):
        return lambda: self.apply_effect(func)

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


if __name__ == "__main__":
    QCoreApplication.addLibraryPath('/usr/lib/qt6/plugins')

    app = QApplication(sys.argv)
    window = ImageRestorerGUI()
    window.show()
    sys.exit(app.exec())
