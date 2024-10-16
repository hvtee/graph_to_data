import sys

from PyQt5.QtWidgets import QApplication

from ui.main_window import Main_Window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = Main_Window()
    main_window.show()
    sys.exit(app.exec_())
