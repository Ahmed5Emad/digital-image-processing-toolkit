import sys
import cv2
# import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame, QScrollArea
)
from PyQt6.QtGui import QImage, QPixmap, QFont, QColor, QPalette
from PyQt6.QtCore import Qt, QSize, QCoreApplication

import processor


class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class ImageDestroyerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Destroyer")
        self.setMinimumSize(1000, 700)

        self.original_image = None
        self.current_image = None

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
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(15)

        title = QLabel("IMAGE\nDESTROYER")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)

        sidebar_layout.addSpacing(20)

        self.btn_load = ModernButton("Load Image")
        self.btn_load.clicked.connect(self.load_image)
        sidebar_layout.addWidget(self.btn_load)

        sidebar_layout.addSpacing(10)

        noise_label = QLabel("NOISE EFFECTS")
        noise_label.setObjectName("section_label")
        sidebar_layout.addWidget(noise_label)

        self.btn_gaussian = ModernButton("Gaussian Noise")
        self.btn_gaussian.clicked.connect(
            lambda: self.apply_effect(processor.add_gaussian_noise))
        sidebar_layout.addWidget(self.btn_gaussian)

        self.btn_sp = ModernButton("Salt & Pepper")
        self.btn_sp.clicked.connect(lambda: self.apply_effect(
            processor.add_salt_and_pepper_noise))
        sidebar_layout.addWidget(self.btn_sp)

        self.btn_speckle = ModernButton("Speckle Noise")
        self.btn_speckle.clicked.connect(
            lambda: self.apply_effect(processor.add_speckle_noise))
        sidebar_layout.addWidget(self.btn_speckle)

        self.btn_periodic = ModernButton("Periodic Noise")
        self.btn_periodic.clicked.connect(
            lambda: self.apply_effect(processor.add_periodic_noise))
        sidebar_layout.addWidget(self.btn_periodic)

        self.btn_uniform = ModernButton("Uniform Noise")
        self.btn_uniform.clicked.connect(
            lambda: self.apply_effect(processor.add_uniform_noise))
        sidebar_layout.addWidget(self.btn_uniform)

        self.btn_rayleigh = ModernButton("Rayleigh Noise")
        self.btn_rayleigh.clicked.connect(
            lambda: self.apply_effect(processor.add_rayleigh_noise))
        sidebar_layout.addWidget(self.btn_rayleigh)

        self.btn_exponential = ModernButton("Exponential Noise")
        self.btn_exponential.clicked.connect(
            lambda: self.apply_effect(processor.add_exponential_noise))
        sidebar_layout.addWidget(self.btn_exponential)

        sidebar_layout.addSpacing(10)

        transform_label = QLabel("TRANSFORMATIONS")
        transform_label.setObjectName("section_label")
        sidebar_layout.addWidget(transform_label)

        self.btn_grayscale = ModernButton("Grayscale")
        self.btn_grayscale.clicked.connect(
            lambda: self.apply_effect(processor.to_grayscale))
        sidebar_layout.addWidget(self.btn_grayscale)

        self.btn_blur = ModernButton("Apply Blur")
        self.btn_blur.clicked.connect(
            lambda: self.apply_effect(processor.apply_blur))
        sidebar_layout.addWidget(self.btn_blur)

        sidebar_layout.addStretch()

        self.btn_save = ModernButton("Save Image")
        self.btn_save.setObjectName("save_btn")
        self.btn_save.clicked.connect(self.save_image)
        sidebar_layout.addWidget(self.btn_save)

        self.btn_reset = ModernButton("Reset Image")
        self.btn_reset.setObjectName("reset_btn")
        self.btn_reset.clicked.connect(self.reset_image)
        sidebar_layout.addWidget(self.btn_reset)

        main_layout.addWidget(sidebar)

        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(40, 40, 40, 40)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setObjectName("preview_scroll")

        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setObjectName("image_preview")
        self.scroll_area.setWidget(self.image_label)

        preview_layout.addWidget(self.scroll_area)
        main_layout.addWidget(preview_container)

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
            self.current_image = effect_func(self.current_image)
            self.update_preview()

    def reset_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.update_preview()

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
