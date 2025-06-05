from PyQt6.QtWidgets import (QApplication, QMainWindow, QFrame, QVBoxLayout, 
                          QPushButton, QLabel, QWidget, QHBoxLayout, QTextEdit,
                          QGraphicsOpacityEffect)
from PyQt6.QtCore import (Qt, QPoint, pyqtSignal, QPropertyAnimation, QTimer, 
                         QSize, QRectF, QPointF)
from PyQt6.QtGui import (QFont, QIcon, QPixmap, QPainter, QColor, QPainterPath, 
                        QLinearGradient, QPen)
import sys
import os
import math

class RobotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 200)
        self.angle = 0
        self.pulse_size = 0
        
        # Animation timer using QTimer instead of QBasicTimer
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.animate)
        self.anim_timer.start(50)
        
        # Pulse animation
        self.pulse_timer = QTimer(self)
        self.pulse_timer.timeout.connect(self.pulse)
        self.pulse_timer.start(30)
        
        self.is_listening = False

    def animate(self):
        self.angle = (self.angle + 5) % 360
        self.update()

    def pulse(self):
        self.pulse_size = (self.pulse_size + 0.1) % (2 * math.pi)
        self.update()

    def setListening(self, listening):
        self.is_listening = listening
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate center and sizes
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        size = min(width, height) * 0.8
        
        # Draw outer circle with gradient
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor(0, 255, 0, 30))
        gradient.setColorAt(1, QColor(0, 255, 0, 10))
        
        # Pulsing outer circle
        pulse_radius = size/2 + math.sin(self.pulse_size) * 10
        outer_rect = QRectF(
            center_x - pulse_radius,
            center_y - pulse_radius,
            pulse_radius * 2,
            pulse_radius * 2
        )
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(outer_rect)

        # Draw robot face
        pen = QPen(QColor("#00FF00"), 2)
        painter.setPen(pen)
        
        # Head
        head_size = size * 0.6
        head_rect = QRectF(
            center_x - head_size/2,
            center_y - head_size/2,
            head_size,
            head_size
        )
        painter.drawRoundedRect(head_rect, 15, 15)
        
        # Eyes
        eye_size = head_size * 0.2
        eye_y = center_y - eye_size/2
        
        # Left eye
        left_eye_x = center_x - head_size/4 - eye_size/2
        left_eye_rect = QRectF(left_eye_x, eye_y, eye_size, eye_size)
        painter.drawEllipse(left_eye_rect)
        
        # Right eye
        right_eye_x = center_x + head_size/4 - eye_size/2
        right_eye_rect = QRectF(right_eye_x, eye_y, eye_size, eye_size)
        painter.drawEllipse(right_eye_rect)
        
        # Animated mouth
        mouth_width = head_size * 0.4
        mouth_height = head_size * 0.1
        
        if self.is_listening:
            # Animated waveform mouth when listening
            path = QPainterPath()
            start_x = center_x - mouth_width/2
            y = center_y + head_size/4
            path.moveTo(start_x, y)
            
            for i in range(int(mouth_width)):
                x = start_x + i
                offset = math.sin((i + self.angle) * 0.2) * mouth_height
                path.lineTo(x, y + offset)
            
            painter.drawPath(path)
        else:
            # Simple smile when not listening
            mouth_rect = QRectF(
                center_x - mouth_width/2,
                center_y + head_size/4 - mouth_height/2,
                mouth_width,
                mouth_height
            )
            painter.drawArc(mouth_rect, 0, 180 * 16)

class WaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(50)
        self.waves = [0] * 10  # Initialize with 10 zero values
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateWaves)
        
    def startAnimation(self):
        self.timer.start(50)
        
    def stopAnimation(self):
        self.timer.stop()
        self.waves = [0] * 10
        self.update()
        
    def updateWaves(self):
        import random
        self.waves = self.waves[1:] + [random.randint(10, 40)]
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setPen(QPen(QColor("#00FF00"), 2))
        
        width = self.width()
        height = self.height()
        center_y = height / 2
        
        if len(self.waves) > 1:  # Only draw if we have at least 2 points
            path_width = width / (len(self.waves) - 1)
            for i in range(len(self.waves) - 1):
                x1 = i * path_width
                x2 = (i + 1) * path_width
                y1 = center_y - self.waves[i]
                y2 = center_y - self.waves[i + 1]
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))

class TitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)

        # Add icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        if os.path.exists(icon_path):
            icon_label = QLabel()
            pixmap = QPixmap(icon_path).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
            icon_label.setPixmap(pixmap)
            layout.addWidget(icon_label)

        self.title_label = QLabel("ZILNOVA AI Assistant", self)
        self.title_label.setStyleSheet("color: #00FF00; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Window control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        self.minimize_btn = QPushButton("−", self)
        self.maximize_btn = QPushButton("□", self)
        self.close_btn = QPushButton("×", self)

        for btn in [self.minimize_btn, self.maximize_btn, self.close_btn]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #00FF00;
                    border: none;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #2d2d2d;
                }
            """)
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)

        self.minimize_btn.clicked.connect(parent.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(parent.close)

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
    start_listening = pyqtSignal()
    stop_listening = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZILNOVA AI Assistant")
        self.setMinimumSize(900, 700)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Apply glass effect style
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(25, 25, 25, 245);
                border-radius: 15px;
                border: 2px solid rgba(0, 255, 0, 100);
            }
        """)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Add title bar
        self.title_bar = TitleBar(self)
        self.layout.addWidget(self.title_bar)

        # Main content area
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        self.layout.addWidget(self.content_widget)

        # Add robot animation in the center
        self.robot = RobotWidget(self)
        content_layout.addWidget(self.robot)

        # Add waveform visualization
        self.waveform = WaveformWidget(self)
        content_layout.addWidget(self.waveform)

        # Status label
        self.status_label = QLabel("Ready", self)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #00FF00;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                background-color: rgba(0, 255, 0, 10);
                border-radius: 10px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.status_label)

        # Command history
        self.history_text = QTextEdit(self)
        self.history_text.setReadOnly(True)
        self.history_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(20, 20, 20, 200);
                color: #00FF00;
                border: 1px solid rgba(0, 255, 0, 50);
                border-radius: 10px;
                font-family: 'Consolas', monospace;
                font-size: 14px;
                padding: 15px;
                selection-background-color: rgba(0, 255, 0, 50);
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 255, 0, 20);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 255, 0, 130);
                border-radius: 5px;
            }
        """)
        content_layout.addWidget(self.history_text)

        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.start_button = QPushButton("Start Listening", self)
        self.stop_button = QPushButton("Stop Listening", self)
        self.clear_button = QPushButton("Clear History", self)

        for btn in [self.start_button, self.stop_button, self.clear_button]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 255, 0, 20);
                    color: #00FF00;
                    border: 2px solid #00FF00;
                    border-radius: 10px;
                    padding: 5px 20px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(0, 255, 0, 40);
                    border-color: rgba(0, 255, 0, 200);
                }
                QPushButton:pressed {
                    background-color: rgba(0, 255, 0, 60);
                    border-color: rgba(0, 255, 0, 255);
                }
            """)
            button_layout.addWidget(btn)

        content_layout.addLayout(button_layout)

        # Connect signals
        self.start_button.clicked.connect(self._on_start)
        self.stop_button.clicked.connect(self._on_stop)
        self.clear_button.clicked.connect(self.clear_history)

        # Auto-start after initialization
        QTimer.singleShot(1000, self._on_start)

    def _on_start(self):
        self.start_listening.emit()
        self.waveform.startAnimation()
        self.robot.setListening(True)
        
    def _on_stop(self):
        self.stop_listening.emit()
        self.waveform.stopAnimation()
        self.robot.setListening(False)

    def update_status(self, text):
        self.status_label.setText(text)
        if text == "Listening...":
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #00FF00;
                    font-size: 24px;
                    font-weight: bold;
                    padding: 10px;
                    background-color: rgba(0, 255, 0, 20);
                    border-radius: 10px;
                }
            """)
        else:
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #00FF00;
                    font-size: 24px;
                    font-weight: bold;
                    padding: 10px;
                    background-color: rgba(0, 255, 0, 10);
                    border-radius: 10px;
                }
            """)

    def add_to_history(self, text, is_user=False):
        prefix = "👤 You: " if is_user else "🤖 ZILNOVA: "
        self.history_text.append(f"{prefix}{text}")
        
        # Scroll to bottom
        self.history_text.verticalScrollBar().setValue(
            self.history_text.verticalScrollBar().maximum()
        )

    def clear_history(self):
        self.history_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssistantGUI()
    window.show()
    sys.exit(app.exec())
