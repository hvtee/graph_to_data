import os.path

from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, \
    QMainWindow, QMessageBox, QFileDialog


class Add_Graph_Window(QWidget):
    def __init__(self, main_window):
        super(Add_Graph_Window, self).__init__()
        self.main_window = main_window
        self.setupUi(self)

    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(410, 220)
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 391, 201))
        self.general_layout = QVBoxLayout(self.widget)
        self.general_layout.setObjectName(u"general_layout")
        self.general_layout.setContentsMargins(0, 0, 0, 0)
        self.add_graph_button = QPushButton(self.widget)
        self.add_graph_button.setObjectName(u"add_graph_button")

        self.general_layout.addWidget(self.add_graph_button)

        self.axes_layout = QHBoxLayout()
        self.axes_layout.setObjectName(u"axes_layout")
        self.x_layout = QVBoxLayout()
        self.x_layout.setObjectName(u"x_layout")
        self.min_x_layout = QHBoxLayout()
        self.min_x_layout.setObjectName(u"min_x_layout")
        self.min_x_label = QLabel(self.widget)
        self.min_x_label.setObjectName(u"min_x_label")

        self.min_x_layout.addWidget(self.min_x_label)

        self.min_x_line_edit = QLineEdit(self.widget)
        self.min_x_line_edit.setObjectName(u"min_x_line_edit")

        self.min_x_layout.addWidget(self.min_x_line_edit)

        self.x_layout.addLayout(self.min_x_layout)

        self.max_x_layout = QHBoxLayout()
        self.max_x_layout.setObjectName(u"max_x_layout")
        self.max_x_label = QLabel(self.widget)
        self.max_x_label.setObjectName(u"max_x_label")

        self.max_x_layout.addWidget(self.max_x_label)

        self.max_x_line_edit = QLineEdit(self.widget)
        self.max_x_line_edit.setObjectName(u"max_x_line_edit")

        self.max_x_layout.addWidget(self.max_x_line_edit)

        self.x_layout.addLayout(self.max_x_layout)

        self.axes_layout.addLayout(self.x_layout)

        self.y_layout = QVBoxLayout()
        self.y_layout.setObjectName(u"y_layout")
        self.min_y_layout = QHBoxLayout()
        self.min_y_layout.setObjectName(u"min_y_layout")
        self.min_y_label = QLabel(self.widget)
        self.min_y_label.setObjectName(u"min_y_label")

        self.min_y_layout.addWidget(self.min_y_label)

        self.min_y_line_edit = QLineEdit(self.widget)
        self.min_y_line_edit.setObjectName(u"min_y_line_edit")

        self.min_y_layout.addWidget(self.min_y_line_edit)

        self.y_layout.addLayout(self.min_y_layout)

        self.max_y_layout = QHBoxLayout()
        self.max_y_layout.setObjectName(u"max_y_layout")
        self.max_y_label = QLabel(self.widget)
        self.max_y_label.setObjectName(u"max_y_label")

        self.max_y_layout.addWidget(self.max_y_label)

        self.max_y_line_edit = QLineEdit(self.widget)
        self.max_y_line_edit.setObjectName(u"max_y_line_edit")

        self.max_y_layout.addWidget(self.max_y_line_edit)

        self.y_layout.addLayout(self.max_y_layout)

        self.axes_layout.addLayout(self.y_layout)

        self.general_layout.addLayout(self.axes_layout)

        self.dialog_box = QDialogButtonBox(self.widget)
        self.dialog_box.setObjectName(u"dialog_box")
        self.dialog_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.general_layout.addWidget(self.dialog_box)

        QWidget.setTabOrder(self.add_graph_button, self.min_x_line_edit)
        QWidget.setTabOrder(self.min_x_line_edit, self.max_x_line_edit)
        QWidget.setTabOrder(self.max_x_line_edit, self.min_y_line_edit)

        self.retranslateUi(Dialog)

        # Event Handlers
        self.dialog_box.accepted.connect(self.on_ok_pressed)
        self.dialog_box.rejected.connect(self.close)
        self.add_graph_button.clicked.connect(self.open_file_dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.add_graph_button.setText(QCoreApplication.translate("Dialog", u"Add graph", None))
        self.min_x_label.setText(QCoreApplication.translate("Dialog", u"min x", None))
        self.max_x_label.setText(QCoreApplication.translate("Dialog", u"max x", None))
        self.min_y_label.setText(QCoreApplication.translate("Dialog", u"min y", None))
        self.max_y_label.setText(QCoreApplication.translate("Dialog", u"max y", None))

    def open_file_dialog(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Choose file", "", "All Files (*)")
            if file_path:
                self.add_graph_button.setText(os.path.basename(file_path))
        except Exception as e:
            self.main_window.log_message(f"Error while choosing file: {e}")

    def on_ok_pressed(self):
        try:
            min_x = self.min_x_line_edit.text()
            max_x = self.max_x_line_edit.text()
            min_y = self.min_y_line_edit.text()
            max_y = self.max_y_line_edit.text()
            file_path = self.add_graph_button.text()

            if not (min_x and max_x and min_y and max_y and file_path != "Add graph"):
                QMessageBox.warning(self, "Error", "All spaces should be filled!")
                return

            try:
                min_x = float(min_x)
                max_x = float(max_x)
                min_y = float(min_y)
                max_y = float(max_y)
            except ValueError:
                QMessageBox.warning(self, "Error", "X и Y must be numbers!")
                return

            self.main_window.graph_data.append({
                "file_path": file_path,
                "min_x": min_x,
                "max_x": max_x,
                "min_y": min_y,
                "max_y": max_y
            })
            self.main_window.log_message(
                f"Graph added: {file_path}; X: ({min_x}, {max_x}); Y: ({min_y}, {max_y})")

            self.close()

        except Exception as e:
            self.main_window.log_message(f"Error while adding file: {e}")
