import sys

from PySide6.QtWidgets import QApplication

from gui import GUI

if __name__ == "__main__":
    app = QApplication([])

    widget = GUI()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
