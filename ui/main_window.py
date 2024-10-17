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
            if len(self.graph_data) == 0:
                self.log_message("Graphs not chosen!")
                return

            for graph in self.graph_data:
                image_path = "graphs/" + os.path.basename(graph['file_path'])
                min_x = graph['min_x']
                max_x = graph['max_x']
                min_y = graph['min_y']
                max_y = graph['max_y']

                image = cv2.imread(image_path)
                image_name = os.path.basename(image_path)
                x_range = (min_x, max_x)
                y_range = (min_y, max_y)

                red_coords, green_coords = evaluate_curve(image_path, x_range, y_range)
                red_sorted_coords = sorted(np.asarray(red_coords).tolist(), key=lambda coord: coord[0])
                green_sorted_coords = sorted(np.asarray(green_coords).tolist(), key=lambda coord: coord[0])
                red_average_coords = average_curve(red_sorted_coords)
                green_average_coords = average_curve(green_sorted_coords)

                # Plotting the original graph and the combined curves
                fig, ax = plt.subplots(1, 2, figsize=(12, 6))

                # Original Image
                ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                ax[0].set_title('Source Graph:')
                ax[0].axis('off')

                # Combined Curves
                x = [i[0] for i in red_average_coords]
                y = [i[1] for i in red_average_coords]
                ax[1].plot(x, y, color='red', lw=2, label='Main Curve')
                x = [i[0] for i in green_average_coords]
                y = [i[1] for i in green_average_coords]
                ax[1].plot(x, y, color='green', lw=2, label='Secondary Curve')
                ax[1].set_title('Extracted hysteresis loop')
                ax[1].set_xlabel('H, kOe')
                ax[1].set_ylabel('M, emu/g')
                ax[1].grid(True)
                ax[1].legend()

                plt.tight_layout()
                plt.show()

                print(f"PARAMS:")

                params = []
                Ms = red_average_coords[-1][1]
                Msmin = red_average_coords[0][1]

                red_Mr_point = find_closest_point(red_average_coords, target_x=0)
                red_Mr = abs(red_Mr_point[1])
                green_Mr_point = find_closest_point(green_average_coords, target_x=0)
                green_Mr = abs(green_Mr_point[1])

                red_Hc_point = find_closest_point(red_average_coords, target_y=0)
                red_Hc = abs(red_Hc_point[0])
                green_Hc_point = find_closest_point(green_average_coords, target_y=0)
                green_Hc = abs(green_Hc_point[0])

                curve_square = evaluate_square(red_average_coords, green_average_coords)

                params.append(Ms)
                params.append(red_Mr)
                params.append(red_Hc)
                params.append(green_Mr)
                params.append(green_Hc)
                params.append(curve_square)

                print(f"Ms: {Ms}")
                print(f"Msmin: {Msmin}")
                if red_Mr:
                    print(f"red_Mr: {red_Mr}")
                if red_Hc:
                    print(f"red_Hc: {red_Hc}")
                if green_Mr:
                    print(f"green_Mr: {green_Mr}")
                if green_Hc:
                    print(f"green_Hc: {green_Hc}")
                print(f"Square:{curve_square}")

                red_d_coords = div_coords(red_average_coords, Ms)
                green_d_coords = div_coords(green_average_coords, Ms)

                red_inv_h_coords = recalculate_h(red_average_coords)
                green_inv_h_coords = recalculate_h(green_average_coords)

                # Plotting derivatives and recalculated 1/h
                fig, ax2 = plt.subplots(1, 2, figsize=(12, 6))

                # Plot derivatives
                x = [i[0] for i in red_d_coords]
                y = [i[1] for i in red_d_coords]
                ax2[0].plot(x, y, color='red', lw=2, label='Main curve')
                x = [i[0] for i in green_d_coords]
                y = [i[1] for i in green_d_coords]
                ax2[0].plot(x, y, color='green', lw=2, label='Secondary curve')
                ax2[0].set_title('δM/Ms')
                ax2[0].set_xlabel('H, kOe')
                ax2[0].set_ylabel('M')
                ax2[0].grid(True)
                ax2[0].legend()

                # Plot recalculated 1/h
                x = [i[0] for i in red_inv_h_coords]
                y = [i[1] for i in red_inv_h_coords]
                ax2[1].plot(x, y, color='red', lw=2, label='Main curve')
                x = [i[0] for i in green_inv_h_coords]
                y = [i[1] for i in green_inv_h_coords]
                ax2[1].plot(x, y, color='green', lw=2, label='Secondary curve')
                ax2[1].set_title('M(1/H)')
                ax2[1].set_xlabel('1/H, 1/kOe')
                ax2[1].set_ylabel('M, emu/g')
                ax2[1].grid(True)
                ax2[1].legend()

                plt.tight_layout()
                plt.show()

                if red_average_coords and green_average_coords is not None:
                    try:
                        save_to_excel(red_average_coords, green_average_coords, red_d_coords, red_inv_h_coords, params,
                                      image_name)
                    except Exception as e:
                        self.log_message(f"Error saving to excel: {e}")
                self.log_message("\nSaved successfully")

                self.log_message("")
                self.log_message(f"Ms: {Ms}")
                self.log_message(f"Msmin: {Msmin}")
                self.log_message(f"red_Mr: {red_Mr}")
                self.log_message(f"red_Hc: {red_Hc}")
                self.log_message(f"green_Mr: {green_Mr}")
                self.log_message(f"green_Hc: {green_Hc}")
                self.log_message(f"Square:{curve_square}")
                self.log_message("")
        except Exception as e:
            self.log_message(f"Error analysing graph: {e}")

    def log_message(self, message):
        self.main_window_text_browser.append(message)
