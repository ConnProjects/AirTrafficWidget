from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
import json

from flights import get_flights
from geo import haversine_nm

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setFixedSize(300, 120)

        self.label = QLabel("Loading...", self)
        self.label.setStyleSheet("color: white; font-size: 14px;")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setStyleSheet("background-color: rgba(20,20,20,200); border-radius: 12px;")

        self.load_settings()
        self.position_widget()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_flight)
        self.timer.start(8000)

        self.update_flight()

    def load_settings(self):
        with open("settings.json") as f:
            self.settings = json.load(f)

    def position_widget(self):
        screen = self.screen().availableGeometry()
        pos = self.settings["position"]

        x = 20 if "left" in pos else screen.width() - 320
        y = 20 if "top" in pos else screen.height() - 140

        self.move(x, y)

    def update_flight(self):
        try:
            flights = get_flights()
            s = self.settings

            nearby = []
            for f in flights:
                if f[5] and f[6]:
                    d = haversine_nm(s["lat"], s["lon"], f[6], f[5])
                    if d <= s["radius"]:
                        nearby.append(f)

            if not nearby:
                self.label.setText("No nearby flights")
                return

            f = nearby[0]
            callsign = f[1].strip() if f[1] else "Unknown"
            alt = int(f[7] * 3.28084) if f[7] else 0

            self.label.setText(f"{callsign}\nAltitude: {alt} ft")

        except Exception as e:
            self.label.setText("Error fetching data")
