import os

import cv2
import numpy as np
from PyQt5.QtCore import QSize, QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QSizePolicy, QAction, QWidget, QGridLayout, QPushButton, QTextBrowser, QMenuBar, QMenu, \
    QStatusBar, QMainWindow
from matplotlib import pyplot as plt

from funcs import evaluate_curve, average_curve, find_closest_point, evaluate_square, div_coords, recalculate_h, \
    save_to_excel
from ui.add_graph_window import Add_Graph_Window


class Main_Window(QMainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.graph_data = []

    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(640, 480))
        MainWindow.setMaximumSize(QSize(640, 480))
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 621, 421))
        self.main_window_layout = QGridLayout(self.gridLayoutWidget)
        self.main_window_layout.setObjectName(u"main_window_layout")
        self.main_window_layout.setContentsMargins(0, 0, 0, 0)
        self.add_graph_button = QPushButton(self.gridLayoutWidget)
        self.add_graph_button.setObjectName(u"add_graph_button")

        self.main_window_layout.addWidget(self.add_graph_button, 0, 0, 1, 1)

        self.analyse_button = QPushButton(self.gridLayoutWidget)
        self.analyse_button.setObjectName(u"analyse_button")

        self.main_window_layout.addWidget(self.analyse_button, 0, 1, 1, 1)

        self.main_window_text_browser = QTextBrowser(self.gridLayoutWidget)
        self.main_window_text_browser.setObjectName(u"main_window_text_browser")

        self.main_window_layout.addWidget(self.main_window_text_browser, 1, 0, 1, 2)

        self.add_graph_button.raise_()
        self.analyse_button.raise_()
        self.main_window_text_browser.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 21))
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.add_graph_button, self.main_window_text_browser)
        QWidget.setTabOrder(self.main_window_text_browser, self.analyse_button)

        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuSettings.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        self.add_graph_button.clicked.connect(self.open_add_graph_window)
        self.analyse_button.clicked.connect(self.analyse_data)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.add_graph_button.setText(QCoreApplication.translate("MainWindow", u"Add graph", None))
        self.analyse_button.setText(QCoreApplication.translate("MainWindow", u"Analyse", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))

    def open_add_graph_window(self):
        try:
            self.add_graph_window = Add_Graph_Window(self)
            self.add_graph_window.show()
        except Exception as e:
            self.log_message(f"Error opening add_graph_window: {e}")

    def analyse_data(self):
        try:
            print(self.graph_data)
            image_path = 'graphs/loop_3.jpg'
            image = cv2.imread(image_path)
            image_name = os.path.basename(image_path)
            x_range = (-40, 40)
            y_range = (-80, 80)

            red_coords, green_coords = evaluate_curve(image_path, x_range, y_range)
            red_sorted_coords = sorted(np.asarray(red_coords).tolist(), key=lambda coord: coord[0])
            green_sorted_coords = sorted(np.asarray(green_coords).tolist(), key=lambda coord: coord[0])
            red_average_coords = average_curve(red_sorted_coords)
            green_average_coords = average_curve(green_sorted_coords)

            fig, ax = plt.subplots(1, 3, figsize=(12, 6))

            ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            ax[0].set_title('Source graph:')
            ax[0].axis('off')
            ax[1].plot(red_average_coords[0], red_average_coords[1], lw=2)
            ax[1].set_title('Rebuilt graph (main)')
            ax[1].set_xlabel('H, kOe')
            ax[1].set_ylabel('M, emu/g')
            ax[1].grid(True)
            ax[2].plot(green_average_coords[0], green_average_coords[1], lw=2)
            ax[2].set_title('Rebuilt graph (secondary)')
            ax[2].set_xlabel('H, kOe')
            ax[2].set_ylabel('M, emu/g')
            ax[2].grid(True)
            plt.tight_layout()
            plt.show()

            print(f"PARAMS:")

            params = []
            Ms = red_average_coords[-1][1]
            Msmin = red_average_coords[0][1]

            # max_y = max(coords, key=lambda coord: coord[1])[1]
            # min_y = min(coords, key=lambda coord: coord[1])[1]

            Mr_point = find_closest_point(red_coords, target_x=0)
            Mr = Mr_point[1]

            Hc_point = find_closest_point(red_coords, target_y=0)
            Hc = Hc_point[0]

            curve_square = evaluate_square(red_average_coords, green_average_coords)

            params.append(Ms)
            params.append(abs(Mr))
            params.append(abs(Hc))
            params.append(curve_square)

            print(f"Ms: {Ms}")
            print(f"Msmin: {Msmin}")
            if Mr:
                print(f"Mr: {Mr}")
            if Hc:
                print(f"Hc: {Hc}")
            print(f"Square:{curve_square}")

            d_coords = div_coords(red_average_coords, Ms)
            x = [i[0] for i in d_coords]
            y = [i[1] for i in d_coords]
            plt.plot(x, y, lw=2)
            plt.title('Rebuilt graph (secondary)')
            plt.xlabel('H, kOe')
            plt.ylabel('M, emu/g')
            plt.grid(True)
            plt.show()

            inv_h_coords = recalculate_h(red_average_coords)
            x = [i[0] for i in inv_h_coords]
            y = [i[1] for i in inv_h_coords]
            plt.plot(x, y, lw=2)
            plt.title('Rebuilt graph (secondary)')
            plt.xlabel('H, kOe')
            plt.ylabel('M, emu/g')
            plt.grid(True)
            plt.show()

            if red_average_coords and green_average_coords is not None:
                save_to_excel(red_average_coords, green_average_coords, d_coords, inv_h_coords, params, image_name)
        except Exception as e:
            self.log_message(f"Ошибка при анализе данных: {e}")

    def log_message(self, message):
        self.main_window_text_browser.append(message)
