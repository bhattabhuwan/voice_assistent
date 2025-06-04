from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QPushButton, QLabel, QWidget
from PyQt6.QtCore import Qt, QPoint
import sys

class TitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: #1e1e1e;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)

        self.title_label = QLabel("ZILNOVA", self)
        self.title_label.setStyleSheet("color: #00FF00; font-size: 14px;")

        self.minimize_btn = QPushButton("−", self)
        self.maximize_btn = QPushButton("□", self)
        self.close_btn = QPushButton("×", self)

        for btn in [self.minimize_btn, self.maximize_btn, self.close_btn]:
            btn.setFixedSize(30, 25)
            btn.setStyleSheet("background: transparent; color: #00FF00;")

        self.minimize_btn.clicked.connect(parent.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(parent.close)

        layout.addWidget(self.title_label)
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.maximize_btn)
        layout.addWidget(self.close_btn)

        self.start = QPoint()

    def toggle_maximize(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.start
            self.window().move(self.window().pos() + delta)
            self.start = event.globalPosition().toPoint()

class AssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZILNOVA")
        self.setFixedSize(800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.title_bar = TitleBar(self)
        self.layout.addWidget(self.title_bar)

        self.content_label = QLabel("Voice Assistant GUI Placeholder", self)
        self.content_label.setStyleSheet("color: #00FF00; font-size: 18px;")
        self.layout.addWidget(self.content_label)
