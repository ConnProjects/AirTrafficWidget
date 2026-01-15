import sys
from PySide6.QtWidgets import QApplication
from widget import Widget

app = QApplication(sys.argv)
w = Widget()
w.show()
sys.exit(app.exec())
