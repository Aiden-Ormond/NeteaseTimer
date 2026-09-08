import sys
from PyQt5.QtWidgets import QApplication
from app.main_window import MainWindow
from app.utils import ensure_single_instance

def main():
    if not ensure_single_instance():
        sys.exit(0)

    app = QApplication(sys.argv)
    app.setApplicationName("NeteaseTimer")
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
