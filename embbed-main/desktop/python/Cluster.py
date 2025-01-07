
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen
import sys
import math

class SpeedometerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.speed = 0
        self.setMinimumSize(200, 200)

    def setSpeed(self, speed):
        self.speed = speed
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Desenha o círculo do velocímetro
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 2 - 10
        painter.setPen(QPen(Qt.white, 2))
        painter.drawEllipse(center, radius, radius)

        # Desenha os marcadores
        for i in range(0, 220, 20):
            angle = math.radians(i * 1.5 - 120)  # -120 a 120 graus
            start_x = center.x() + (radius - 15) * math.cos(angle)
            start_y = center.y() + (radius - 15) * math.sin(angle)
            end_x = center.x() + radius * math.cos(angle)
            end_y = center.y() + radius * math.sin(angle)
            painter.drawLine(int(start_x), int(start_y), int(end_x), int(end_y))

        # Desenha o ponteiro
        angle = math.radians(self.speed * 1.5 - 120)
        painter.setPen(QPen(Qt.red, 3))
        end_x = center.x() + (radius - 10) * math.cos(angle)
        end_y = center.y() + (radius - 10) * math.sin(angle)
        painter.drawLine(center, int(end_x), int(end_y))

        # Desenha o texto da velocidade
        painter.setPen(Qt.white)
        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            f"{self.speed}\nkm/h"
        )

class BatteryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.level = 100
        self.setMinimumSize(200, 50)

    def setLevel(self, level):
        self.level = level
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Desenha a borda da bateria
        painter.setPen(QPen(Qt.white, 2))
        bat_rect = self.rect().adjusted(10, 10, -30, -10)
        painter.drawRect(bat_rect)
        
        # Desenha o terminal da bateria
        terminal_rect = self.rect().adjusted(bat_rect.width() + 10, 20, -10, -20)
        painter.drawRect(terminal_rect)

        # Desenha o nível da bateria
        if self.level > 20:
            color = QColor(0, 255, 0)  # Verde
        else:
            color = QColor(255, 0, 0)  # Vermelho
        
        level_width = int(bat_rect.width() * self.level / 100)
        level_rect = bat_rect.adjusted(2, 2, -2, -2)
        level_rect.setWidth(level_width)
        painter.fillRect(level_rect, color)

        # Desenha o texto do nível
        painter.setPen(Qt.white)
        painter.drawText(
            bat_rect,
            Qt.AlignCenter,
            f"{self.level}%"
        )

class ClusterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Cluster")
        self.setStyleSheet("background-color: black;")
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Widgets do cluster
        self.speedometer = SpeedometerWidget()
        self.battery = BatteryWidget()

        # Adiciona widgets ao layout
        layout.addWidget(self.speedometer)
        layout.addWidget(self.battery)

        # Timer para simular atualizações
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(100)  # 100ms = 10Hz

        self.test_speed = 0
        self.test_battery = 100

    def updateData(self):

        self.test_speed = (self.test_speed + 1) % 220
        self.test_battery = max(0, self.test_battery - 0.1)
        
        self.speedometer.setSpeed(self.test_speed)
        self.battery.setLevel(self.test_battery)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClusterWindow()
    window.resize(800, 480)
    window.show()
    sys.exit(app.exec())