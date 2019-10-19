from __future__ import absolute_import, print_function
import sys
import math
from _ctypes import sizeof

from OpenGL.raw.GLU import gluLookAt
from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt, QCoreApplication, QTimer
from PyQt5.QtGui import QColor, QValidator
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QPushButton, QCheckBox, QLabel,
                             QMenu, QMenuBar, QComboBox, QVBoxLayout, QMessageBox, QWidget, QSpinBox, QLineEdit,
                             QStackedWidget, QFormLayout, QDesktopWidget, QFileDialog, QDoubleSpinBox, QProgressBar)

import OpenGL.GL as gl

from OpenGL import GLU

import pyopencl as cl
import numpy as np
from time import time
from math import pi

import pyrealsense2 as rs
import serial
from serial.tools.list_ports import comports
import os

"""

        #Récupération de la résolution de l'écran pour pouvoir modifier 
        #la taille de l'affichage ultérieurement

        self.screen_size = QDesktopWidget().screenGeometry()
        print(" Screen size : " + str(self.screen_size.height()) + "x" + str(self.screen_size.width()))

"""

from OpenGL.GL import *
from OpenGL.raw import GL
from OpenGL.arrays import ArrayDatatype as ADT

ctx = cl.create_some_context(None, [0])

queue = cl.CommandQueue(ctx)

mf = cl.mem_flags

prg = cl.Program(ctx, """
    __kernel void treatment_mobile(__global const float *point, __global float *trans_x, __global float *trans_y, 
    __global float *trans_z, __global float *lim_x, __global float *lim_y, __global float *lim_z,
    __global float *point_prime)
    {
        float limit_x = *lim_x;
        float limit_y = *lim_y;
        float limit_z = *lim_z;
        int i = (get_global_id(0) * 2) + get_global_id(0);
        if(point[i] < limit_x && point[i] > -(limit_x)){
            if(point[i+1] < (limit_y) && point[i+1] > -(limit_y)){
                if(point[i+2] > -(limit_z)){
                    point_prime[i] = point[i] + *trans_x;
                    point_prime[i+1] = point[i+1] + *trans_y;
                    point_prime[i+2] = point[i+2] + *trans_z;
                }
            }
        }
    }    
    
    __kernel void treatment_platform(__global const float *point, __global float *trans_z, __global float *lim_x,
     __global float *lim_y_high, __global float *lim_y_low, __global float *lim_z, __global float *point_prime)
    {
        float limit_x = *lim_x;
        float limit_z = *lim_z;
        float transition = *trans_z;
        int i = (get_global_id(0) * 2) + get_global_id(0);
        if(point[i] < limit_x && point[i] > -(limit_x)){
            if(point[i+1] < (*lim_y_low) && point[i+1] > -(*lim_y_high)){
                if(point[i+2] < (limit_z)){
                    point_prime[i] = point[i];
                    point_prime[i+1] = point[i+1];
                    point_prime[i+2] = point[i+2] - transition;
                }
            }
        }
    }
    
    __kernel void treatment_test(__global const float *point, __global float *lim_x,
     __global float *lim_y, __global float *lim_z, __global float *point_prime)
    {
        float limit_x = *lim_x;
        float limit_y = *lim_y;
        float limit_z = *lim_z;
        int i = (get_global_id(0) * 2) + get_global_id(0);
        if(point[i] < limit_x && point[i] > -(limit_x)){
            if(point[i+1] < (limit_y) && point[i+1] > -(limit_y)){
                if(point[i+2] < (limit_z)){
                    point_prime[i] = point[i];
                    point_prime[i+1] = point[i+1];
                    point_prime[i+2] = point[i+2];
                }
            }
        }
    }
    
    __kernel void rot_x(__global const float *point, __global float *angle, __global float *point_prime)
    {
        float angle_x = *angle;
        int i = (get_global_id(0) * 2) + get_global_id(0);
        point_prime[i] = point[i];
        point_prime[i+1] = cos(angle_x) * point[i+1] + sin(angle_x) * point[i+2];
        point_prime[i+2] = cos(angle_x) * point[i+2] - sin(angle_x) * point[i+1];
    }

    __kernel void rot_y(__global const float *point, __global float *angle, __global float *point_prime)
    {
        float angle_y = *angle;
        int i = (get_global_id(0) * 2) + get_global_id(0);
        point_prime[i] = cos(angle_y) * point[i] - sin(angle_y) * point[i+2];
        point_prime[i+1] = point[i+1];
        point_prime[i+2] = cos(angle_y) * point[i+2] + sin(angle_y) * point[i];
    }

    __kernel void rot_z(__global const float *point, __global float *angle, __global float *point_prime)
    {
        float angle_z = *angle;
        int i = (get_global_id(0) * 2) + get_global_id(0);
        point_prime[i] = cos(angle_z) * point[i] + sin(angle_z) * point[i+1];
        point_prime[i+1] = cos(angle_z) * point[i+1] - sin(angle_z) * point[i];
        point_prime[i+2] = point[i+2];
    }
    """).build()


class Window(QWidget):


    def __init__(self):
        super(Window, self).__init__()

        self.disable_choice_format()

        self.connect_rs: bool
        self.connect_rs = False

        self.out = ''

        self.port = 0

        self.rs = RealSense()
        self.platform = Platform()

        self.timer = QTimer(self)  # set timer to execute different action

        # self.rs.init_profile_realsense()

        self.list_resolution = QComboBox()
        self.list_resolution.insertItem(0, '720p')
        self.list_resolution.insertItem(1, '480p')
        self.list_resolution.insertItem(2, '360p')

        self.list_resolution.setMaximumWidth(150)

        self.list_resolution.currentIndexChanged.connect(self.choose_resolution)

        self.list_mode = QComboBox()
        self.list_mode.insertItem(0, 'Plateforme')
        self.list_mode.insertItem(1, 'Mobile')
        self.list_mode.insertItem(2, 'Test Réglage')

        self.list_mode.setMaximumWidth(150)

        self.list_mode.currentIndexChanged.connect(self.choose_mode)

        self.glWidget_Model = GLWidget_Model()
        self.glWidget_Model.sizeHint()

        self.pcd = QCheckBox("pcd", self)
        self.obj = QCheckBox("obj", self)
        self.stl = QCheckBox("stl", self)
        self.ply = QCheckBox("ply", self)
        self.vtk = QCheckBox("vtk", self)

        self.filename = QLineEdit()
        self.filename.setMaxLength(10)
        self.filename.setMaximumWidth(150)

        self.quit_button = QPushButton("Quitter", self)
        self.quit_button.setMaximumWidth(150)
        self.quit_button.clicked.connect(self.close)

        self.button_path = QPushButton("Chemin")
        self.button_path.setMaximumWidth(150)
        self.button_path.clicked.connect(self.recover_path)


        """Initialisation de la gestion des modes"""

        """self.SPB_lim_x = QDoubleSpinBox()
        self.SPB_lim_x.setRange(0, 2)
        self.SPB_lim_x.setValue(0.5)
        self.SPB_lim_x.setDecimals(5)
        self.SPB_lim_x.valueChanged.connect(self.rs.set_lim_x)"""

        self.SPB_laps_number = QSpinBox()
        self.SPB_laps_number.setRange(0, 500)

        self.SPB_lim_y_high = QDoubleSpinBox()
        self.SPB_lim_y_high.setRange(0, 2)
        self.SPB_lim_y_high.setValue(0.5)
        self.SPB_lim_y_high.setDecimals(5)
        self.SPB_lim_y_high.setSingleStep(0.01)
        self.SPB_lim_y_high.valueChanged.connect(self.rs.set_lim_y_high)

        self.SPB_lim_y_low = QDoubleSpinBox()
        self.SPB_lim_y_low.setRange(0, 2)
        self.SPB_lim_y_low.setValue(0.5)
        self.SPB_lim_y_low.setDecimals(5)
        self.SPB_lim_y_low.setSingleStep(0.01)
        self.SPB_lim_y_low.valueChanged.connect(self.rs.set_lim_y_low)

        self.SPB_lim_z = QDoubleSpinBox()
        self.SPB_lim_z.setRange(0, 2)
        self.SPB_lim_z.setValue(0.5)
        self.SPB_lim_z.setDecimals(5)
        self.SPB_lim_z.setSingleStep(0.01)
        self.SPB_lim_z.valueChanged.connect(self.rs.set_lim_z)

        self.SPB_lim_x2 = QDoubleSpinBox()
        self.SPB_lim_x2.setRange(0, 2)
        self.SPB_lim_x2.setValue(0.5)
        self.SPB_lim_x2.setDecimals(5)
        self.SPB_lim_x2.setSingleStep(0.01)
        self.SPB_lim_x2.valueChanged.connect(self.rs.set_lim_x)

        self.SPB_lim_y2 = QDoubleSpinBox()
        self.SPB_lim_y2.setRange(0, 2)
        self.SPB_lim_y2.setValue(0.5)
        self.SPB_lim_y2.setDecimals(5)
        self.SPB_lim_y2.setSingleStep(0.01)
        self.SPB_lim_y2.valueChanged.connect(self.rs.set_lim_y)

        self.SPB_lim_z2 = QDoubleSpinBox()
        self.SPB_lim_z2.setRange(0, 2)
        self.SPB_lim_z2.setValue(0.5)
        self.SPB_lim_z2.setDecimals(5)
        self.SPB_lim_z2.setSingleStep(0.01)
        self.SPB_lim_z2.valueChanged.connect(self.rs.set_lim_z)

        self.SPB_lim_y_high2 = QDoubleSpinBox()
        self.SPB_lim_y_high2.setRange(0, 2)
        self.SPB_lim_y_high2.setValue(0.5)
        self.SPB_lim_y_high2.setDecimals(5)
        self.SPB_lim_y_high2.setSingleStep(0.01)
        self.SPB_lim_y_high2.valueChanged.connect(self.rs.set_lim_y_high)
        self.SPB_lim_y_high2.valueChanged.connect(self.SPB_lim_y_high.setValue)

        self.SPB_lim_y_low2 = QDoubleSpinBox()
        self.SPB_lim_y_low2.setRange(0, 2)
        self.SPB_lim_y_low2.setValue(0.5)
        self.SPB_lim_y_low2.setDecimals(5)
        self.SPB_lim_y_low2.setSingleStep(0.01)
        self.SPB_lim_y_low2.valueChanged.connect(self.rs.set_lim_y_low)
        self.SPB_lim_y_low2.valueChanged.connect(self.SPB_lim_y_low.setValue)

        self.SPB_lim_z3 = QDoubleSpinBox()
        self.SPB_lim_z3.setRange(0, 2)
        self.SPB_lim_z3.setValue(0.5)
        self.SPB_lim_z3.setDecimals(5)
        self.SPB_lim_z3.setSingleStep(0.01)
        self.SPB_lim_z3.valueChanged.connect(self.rs.set_lim_z)
        self.SPB_lim_z3.valueChanged.connect(self.SPB_lim_z.setValue)

        self.SPB_dist_center = QDoubleSpinBox()
        self.SPB_dist_center.setRange(0, 2)
        self.SPB_dist_center.setValue(0.35)
        self.SPB_dist_center.setDecimals(5)
        self.SPB_dist_center.setSingleStep(0.01)
        self.SPB_dist_center.valueChanged.connect(self.rs.set_dist_center)

        self.SPB_dist_center2 = QDoubleSpinBox()
        self.SPB_dist_center2.setRange(0, 2)
        self.SPB_dist_center2.setValue(0.35)
        self.SPB_dist_center2.setDecimals(5)
        self.SPB_dist_center2.setSingleStep(0.01)
        self.SPB_dist_center2.valueChanged.connect(self.rs.set_dist_center)
        self.SPB_dist_center2.valueChanged.connect(self.SPB_dist_center.setValue)

        self.progress = QProgressBar()

        self.SPB_angle = QDoubleSpinBox()
        self.SPB_angle.setRange(0, 180)
        self.SPB_angle.setValue(3.6)
        self.SPB_angle.setDecimals(4)
        self.SPB_angle.setSingleStep(0.1)
        self.SPB_angle.valueChanged.connect(self.rs.set_angle_y)

        self.SPB_angle2 = QDoubleSpinBox()
        self.SPB_angle2.setRange(0, 180)
        self.SPB_angle2.setValue(3.6)
        self.SPB_angle2.setDecimals(4)
        self.SPB_angle2.setSingleStep(0.1)
        self.SPB_angle2.valueChanged.connect(self.rs.set_angle_y)
        self.SPB_angle2.valueChanged.connect(self.SPB_angle.setValue)

        self.button_save = QPushButton("Sauvegarde du modèle")
        self.button_save.setMaximumWidth(150)
        self.button_save.clicked.connect(self.save_file)

        self.button_save2 = QPushButton("Sauvegarde du modèle")
        self.button_save2.setMaximumWidth(150)
        self.button_save2.clicked.connect(self.save_file)

        self.rs_button = QPushButton("Connecter Caméra", self)
        self.rs_button.setMaximumWidth(150)
        self.rs_button.clicked.connect(self.init_rs)

        self.platform_button = QPushButton("Connecter Plateforme", self)
        self.platform_button.setMaximumWidth(150)
        self.platform_button.clicked.connect(self.init_platform)

        self.start_scan = QPushButton("Lancement du scan", self)
        self.start_scan.setMaximumWidth(150)
        self.start_scan.clicked.connect(self.click_scan_platform)

        self.start_scan2 = QPushButton("Lancement du scan", self)
        self.start_scan2.setMaximumWidth(150)
        self.start_scan2.clicked.connect(self.click_scan_mobile)

        self.start_test = QPushButton("Lancement du test", self)
        self.start_test.setMaximumWidth(150)
        self.start_test.clicked.connect(self.click_scan_test)

        self.stop_scan = QPushButton("Arrêt du scan", self)
        self.stop_scan.setMaximumWidth(150)
        self.stop_scan.clicked.connect(self.click_stop_scan)

        self.stop_scan2 = QPushButton("Arrêt du scan", self)
        self.stop_scan2.setMaximumWidth(150)
        self.stop_scan2.clicked.connect(self.click_stop_scan)

        self.stop_scan3 = QPushButton("Arrêt du scan", self)
        self.stop_scan3.setMaximumWidth(150)
        self.stop_scan3.clicked.connect(self.click_stop_scan)


        self.mode_platform_widget = QWidget()
        self.mode_mobile_widget = QWidget()
        self.mode_test_platform_widget = QWidget()

        self.layout_mode_platform()
        self.layout_mode_mobile()
        self.layout_mode_test_platform()

        self.stacked_mode = QStackedWidget(self)
        self.stacked_mode.addWidget(self.mode_platform_widget)
        self.stacked_mode.addWidget(self.mode_mobile_widget)
        self.stacked_mode.addWidget(self.mode_test_platform_widget)

        fourLayout = QVBoxLayout()
        fourLayout.addWidget(self.pcd)
        fourLayout.addWidget(self.obj)
        fourLayout.addWidget(self.stl)
        fourLayout.addWidget(self.ply)
        fourLayout.addWidget(self.vtk)

        secondLayout = QFormLayout()
        secondLayout.addRow("Choix de la résolution", self.list_resolution)
        secondLayout.addRow("Nom des fichiers", self.filename)
        secondLayout.addRow("Choix des formats 3D", fourLayout)
        secondLayout.addRow("Récupération du chemin", self.button_path)
        secondLayout.addRow("Connexion Caméra", self.rs_button)
        secondLayout.addRow("Choix du mode", self.list_mode)
        secondLayout.setAlignment(Qt.AlignRight)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.quit_button)

        thirdLayout = QVBoxLayout()
        thirdLayout.addLayout(secondLayout)
        thirdLayout.addWidget(self.stacked_mode)
        thirdLayout.addWidget(self.quit_button)
        thirdLayout.setAlignment(Qt.AlignRight)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.glWidget_Model)
        self.mainLayout.addLayout(thirdLayout)
        self.setLayout(self.mainLayout)

        # self.showFullScreen()
        self.setWindowTitle("Scanner 3D")

    def layout_mode_mobile(self):
        layout = QVBoxLayout()
        # layout.setGeometry(50, 50, 200, 200)
        layout_lim = QFormLayout()
        layout_lim.addRow("Limite X", self.SPB_lim_x2)
        layout_lim.addRow("Limite Y", self.SPB_lim_y2)
        layout_lim.addRow("Limite Z", self.SPB_lim_z2)
        layout_button = QHBoxLayout()
        layout_button.addWidget(self.start_scan2)
        layout_button.addWidget(self.stop_scan2)
        layout.addLayout(layout_lim)
        layout.addLayout(layout_button)
        layout.addWidget(self.button_save2)
        self.mode_mobile_widget.setLayout(layout)

    def layout_mode_platform(self):
        layout = QVBoxLayout()
        # layout.setGeometry(50, 50, 200, 200)
        layout_lim = QFormLayout()
        layout_lim.addRow("Angle Rotation", self.SPB_angle)
        layout_lim.addRow("Limite Y Haut", self.SPB_lim_y_high)
        layout_lim.addRow("Limite Y Bas", self.SPB_lim_y_low)
        layout_lim.addRow("Limite Z", self.SPB_lim_z)
        layout_lim.addRow("Distance Centre", self.SPB_dist_center)
        layout_lim.addRow("Avancement", self.progress)
        layout_button_1 = QHBoxLayout()
        layout_button_1.addWidget(self.platform_button)
        layout_button_1.addWidget(self.start_scan)
        layout.addLayout(layout_lim)
        layout.addLayout(layout_button_1)
        layout_button_2 = QHBoxLayout()
        layout_button_2.addWidget(self.stop_scan)
        layout_button_2.addWidget(self.button_save)
        layout.addLayout(layout_button_2)
        self.mode_platform_widget.setLayout(layout)

    def layout_mode_test_platform(self):
        layout = QVBoxLayout()
        # layout.setGeometry(50, 50, 200, 200)
        layout_lim = QFormLayout()
        layout_lim.addRow("Angle Rotation", self.SPB_angle2)
        layout_lim.addRow("Limite Y Haut", self.SPB_lim_y_high2)
        layout_lim.addRow("Limite Y Bas", self.SPB_lim_y_low2)
        layout_lim.addRow("Limite Z", self.SPB_lim_z3)
        layout_lim.addRow("Distance Centre", self.SPB_dist_center2)
        layout_button = QHBoxLayout()
        layout_button.addWidget(self.start_test)
        layout_button.addWidget(self.stop_scan3)
        layout.addLayout(layout_lim)
        layout.addLayout(layout_button)
        self.mode_test_platform_widget.setLayout(layout)

    def init_rs(self):
        try:
            self.rs.init_realsense()
            self.connect_rs = self.rs.connect
            QMessageBox.information(self, "La caméra est connectée",
                                    "La caméra est maintenant connectée",
                                    QMessageBox.Ok, QMessageBox.Ok)

        except:
            QMessageBox.information(self, "Attention la caméra n'est pas connectée",
                                    "Veuillez connecter une caméra RealSense pour utiliser ce logiciel",
                                    QMessageBox.Ok, QMessageBox.Ok)

    def recover_path(self):
        dialog = QFileDialog()
        self.filepath = dialog.getExistingDirectory(self, 'Récupération du chemin')

    def stream(self):
        self.rs.stream_camera()

    def click_scan_platform(self):
        if self.connect_rs == True and self.platform.port != 0:
            self.disabled_to_scan()
            self.out = 10
            self.rs.set_mode_platform()
            self.rs.setcounter(False)
            self.rs.reset_verts()
            if self.timer.isActive():
                self.disabled_to_scan()
            self.timer.timeout.connect(self.scan_platform)
            self.timer.start(1000)
        else:
            QMessageBox.information(self, "Attention le scan ne peut pas débuté",
                                    "Veuillez connecter une caméra RealSense ainsi que la plateforme"
                                    "pour pouvoir lancer un scan", QMessageBox.Ok, QMessageBox.Ok)

    def click_scan_mobile(self):
        if self.connect_rs:
            self.disabled_to_scan()
            self.rs.set_mode_mobile()
            if self.timer.isActive():
                self.disabled_to_scan()
            self.timer.timeout.connect(self.scan)
            self.timer.start(10)
        else:
            QMessageBox.information(self, "Attention le scan ne peut pas débuté",
                                    "Veuillez connecter une caméra RealSense"
                                    "pour pouvoir lancer un scan", QMessageBox.Ok, QMessageBox.Ok)

    def click_scan_test(self):
        if self.connect_rs:
            self.disabled_to_scan()
            self.rs.set_mode_test()
            if self.timer.isActive():
                self.disabled_to_scan()
            self.timer.timeout.connect(self.scan)
            self.timer.start(10)
        else:
            QMessageBox.information(self, "Attention le test ne peut pas débuté",
                                    "Veuillez connecter une caméra RealSense"
                                    "pour pouvoir lancer un test", QMessageBox.Ok, QMessageBox.Ok)

    def click_stop_scan(self):
        self.timer.stop()
        self.timer.disconnect()
        self.list_resolution.setDisabled(False)
        self.list_mode.setDisabled(False)

    def scan_platform(self):
        if self.out != '':
            self.out = 0
            self.rs.recovery_data_model()
            self.rs.signal_model.connect(self.glWidget_Model.set_data)
            self.platform.write()
        self.out = self.platform.read()

    def scan(self):
        self.rs.recovery_data_model()
        self.rs.signal_model.connect(self.glWidget_Model.set_data)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Attention fermeture de l'application",
                                     "Etes vous sur de vouloir quitter ?", QMessageBox.Close |
                                     QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            event.accept()
        else:
            event.ignore()

    def choose_resolution(self, i):
        if i == 0:
            self.rs.set_resolution(1280, 720)
        elif i == 1:
            self.rs.set_resolution(848, 480)
        else:
            self.rs.set_resolution(640, 360)

        if self.connect_rs:
            self.timer.stop()
            self.rs.profile_stop()
            self.rs.init_realsense()
            self.timer.start(10)
        pass

    def choose_mode(self, i):
        self.stacked_mode.setCurrentIndex(i)

    def save_file(self):  ##A FINIR
        self.disable_choice_format()
        if self.name[0] and self.filepath[0]:
            if self.pcd.isChecked():
                self.pcd_checked = True
            if self.obj.isChecked():
                self.obj_checked = True
            if self.ply.isChecked():
                self.ply_checked = True
            if self.stl.isChecked():
                self.stl_checked = True
            if self.vtk.isChecked():
                self.vtk_checked = True
        self.create_pcd()
        self.convert_format()
        else:
            QMessageBox.information(self, "Attention problème lors de la sauvegarde",
                                    "Veuillez donner un nom aux fichiers ainsi que le chemin pour la sauvegarde",
                                    QMessageBox.Ok,
                                    QMessageBox.Ok)

    def convert_format(self):
        if self.obj_checked:
            cmd = './pcl_converter ' + self.filename.displayText() + '.pcd ' + self.filename.displayText() + '.obj'
            os.popen(cmd)
        if self.ply_checked:
            cmd = './pcl_converter ' + self.filename.displayText() + '.pcd ' + self.filename.displayText() + '.ply'
            os.popen(cmd)
        if self.stl_checked:
            cmd = './pcl_converter ' + self.filename.displayText() + '.pcd ' + self.filename.displayText() + '.stl'
            os.popen(cmd)
        if self.vtk_checked:
            cmd = './pcl_converter ' + self.filename.displayText() + '.pcd ' + self.filename.displayText() + '.vtk'
            os.popen(cmd)

    def disable_choice_format(self):
        self.pcd_checked = False
        self.obj_checked = False
        self.ply_checked = False
        self.stl_checked = False
        self.vtk_checked = False

    def create_pcd(self):
        name = self.filename.displayText()
        file = open(name, "w")
        file.write("")
        file.close()

        file = open(name, "a")
        mot = ("# .PCD v0.7 - Point Cloud Data file format \n" +
               "FIELDS x y z\n" +
               "SIZE 4 4 4\n" +
               "TYPE F F F\n" +
               "COUNT 1 1 1\n" +
               "WIDTH " + str(self.rs.model.shape) + "\n" +
               "HEIGHT 1\n" +
               "VIEWPOINT 0 0 0 1 0 0 0\n" +
               "POINTS " + str(self.rs.model.shape) + "\n" +
               "DATA ascii\n")
        file.write(mot)
        while i < self.rs.model.shape:
            file.write(self.rs.model[i])
            i = i + 1

        file.close()

    def init_platform(self):
        self.platform.ports()

    def disabled_to_scan(self):
        self.list_resolution.setDisabled(True)
        self.list_mode.setDisabled(True)


class Platform(QWidget):

    def __init__(self):
        super(Platform, self).__init__()
        self.ser = serial.Serial()
        self.port = 0

    def start_com(self):
        self.ser.port = self.port
        self.ser.baudrate = 115200
        self.ser.timeout = 0.01
        self.ser.open()

    def ask_for_port(self):
        for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
            if desc == "FT232R USB UART":
                self.port = port
                return
        self.port = 0

    def ports(self):
        self.ask_for_port()
        if self.port == 0:
            reply = QMessageBox.question(self, "Erreur de connexion série",
                                         "Voulez vous ressaye la verification de la connection serie ?",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.ports()
            else:
                return
        else:
            self.start_com()
            QMessageBox.information(self, "La plateforme est connectée",
                                    "La plateforme est connectée !!!",
                                    QMessageBox.Ok,
                                    QMessageBox.Ok)
            return

    def read(self):
        out = self.ser.read()
        out = out.decode()
        return out

    def write(self):
        data = 55
        self.ser.write([data])


class RealSense(QWidget):
    signal_model = pyqtSignal(object)  # signal_model with data_vertices to display model
    signal_camera = pyqtSignal(object, object)  # signal_camera with data_vertices and data_textures to pov camera

    def __init__(self, width=1280, height=720):
        super(RealSense, self).__init__()
        self.counterstep = False
        self.connect = False
        self.angle_x = 0
        self.angle_y = 25 * pi / 180
        self.angle_z = 0

        self.platform = True
        self.mobile = False

        self.dist_center = 0.34

        self.lim_y_high = 0.5
        self.lim_y_low = 0.2

        self.lim_x = 0.5
        self.lim_y = 0.5
        self.lim_z = 0.5

        self.width = 1280
        self.height = 720

        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.model = np.array([[0, 0, 0]])
        # self.init_realsense(width, height)

    def init_realsense(self):
        self.connect = False
        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, 30)
        # other_stream, other_format = rs.stream.infrared, rs.format.y8
        other_stream, other_format = rs.stream.color, rs.format.rgb8
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.rgb8, 30)
        self.pc = rs.pointcloud()
        # Start streaming
        self.pipeline.start(self.config)
        self.decimate_option()
        self.filters_option()
        self.connect = True

    def profile_stop(self):
        self.pipeline.stop()
        self.config.disable_all_streams()
        """self.config.disable_stream(rs.stream.depth, 0)
        self.config.disable_stream(rs.stream.color, 1)"""

    def set_resolution(self, width, height):
        self.width = width
        self.height = height

    def decimate_option(self, value=0):
        self.decimate = rs.decimation_filter()
        self.decimate.set_option(rs.option.filter_magnitude, 2 ** value)

    def filters_option(self):
        self.colorizer = rs.colorizer()
        self.filters = [rs.disparity_transform(),
                        rs.spatial_filter(),
                        rs.temporal_filter(),
                        rs.disparity_transform(False)]

    def recovery_data_model(self):
        starttime = time()
        while time() - starttime != 1:
            continue
        points = rs.points()

        success, frames = self.pipeline.try_wait_for_frames(timeout_ms=0)  # récupération des images
        if not success:
            return

        depth_frame = frames.get_depth_frame()  # récupération de l'image de la profondeur

        depth_frame = self.decimate.process(depth_frame)

        for f in self.filters:  # application des différents filtres
            depth_frame = f.process(depth_frame)

        points = self.pc.calculate(depth_frame)  # calcul des points

        matrice = np.array(points.get_vertices(2))  # restructuration de la donnée dans une matrice 3*1

        if self.platform == True:
            self.construct_model_platform(matrice)
        elif self.mobile == True:
            self.construct_model_mobile(matrice)
        else:
            self.test_construct_model(matrice)

        # self.signal_model.emit(matrice)

    def construct_model_mobile(self, matrice):
        ymax = np.max(matrice[:, 1])

        angle_x_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.angle_x))
        angle_y_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.angle_y))
        angle_z_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.angle_z))
        vert_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrice)

        tr_g = cl.Buffer(ctx, mf.WRITE_ONLY, matrice.nbytes)

        prg.traitement(queue, matrice.shape, None, vert_g, tr_g)

        tr_np = np.empty_like(matrice)

        cl.enqueue_copy(queue, tr_np, tr_g)

        matrice = tr_np[~np.all(tr_np == 0., axis=1)]

        if self.counterstep != 0:
            self.model = np.append(self.model, matrice, axis=0)
        else:
            self.model = matrice

        verts_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.model)
        x_g = cl.Buffer(ctx, mf.WRITE_ONLY, self.model.nbytes)
        y_g = cl.Buffer(ctx, mf.WRITE_ONLY, self.model.nbytes)
        z_g = cl.Buffer(ctx, mf.WRITE_ONLY, self.model.nbytes)
        prg.rot_x(queue, self.model.shape, None, verts_g, angle_x_g, x_g)

        cl.enqueue_copy(queue, self.model, x_g)

        self.counterstep = self.counterstep + 1

        self.signal_model.emit(self.model)

    def construct_model_platform(self, matrice):
        # ymax = np.max(matrice[:, 1])

        angle = self.angle_y * (math.pi / 180)

        self.lim_x = self.dist_center * math.tan(math.radians(self.angle_y))

        dist_center_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.dist_center))

        lim_x_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.lim_x))

        lim_y_high_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.lim_y_high))

        lim_y_low_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.lim_y_low))

        lim_z_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.lim_z))

        vert_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrice)

        tr_g = cl.Buffer(ctx, mf.WRITE_ONLY, matrice.nbytes)

        prg.treatment_platform(queue, matrice.shape, None, vert_g, dist_center_g, lim_x_g,
                               lim_y_high_g, lim_y_low_g, lim_z_g, tr_g)

        tr_np = np.empty_like(matrice)

        cl.enqueue_copy(queue, tr_np, tr_g)

        matrice = tr_np[~np.all(tr_np == 0., axis=1)]

        if self.counterstep:
            self.model = np.append(self.model, matrice, axis=0)
        else:
            self.model = matrice

        self.counterstep = True

        angle_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(angle))
        verts_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.model)
        res_g = cl.Buffer(ctx, mf.WRITE_ONLY, self.model.nbytes)
        prg.rot_y(queue, self.model.shape, None, verts_g, angle_g, res_g)

        cl.enqueue_copy(queue, self.model, res_g)

        self.signal_model.emit(self.model)

    def test_construct_model(self, matrice):
        print(matrice)
        ymax = np.max(matrice[:, 1])

        angle = self.angle_y * (math.pi / 180)

        self.lim_x = self.dist_center * math.tan(math.radians(angle))

        dist_center_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.dist_center))

        lim_x_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.lim_x))

        lim_y_high_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.lim_y_high))

        lim_y_low_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.lim_y_low))

        lim_z_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(self.lim_z))

        vert_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrice)

        tr_g = cl.Buffer(ctx, mf.WRITE_ONLY, matrice.nbytes)

        prg.treatment_platform(queue, matrice.shape, None, vert_g, dist_center_g, lim_x_g,
                               lim_y_high_g, lim_y_low_g, lim_z_g, tr_g)

        tr_np = np.empty_like(matrice)

        cl.enqueue_copy(queue, tr_np, tr_g)

        matrice = tr_np[~np.all(tr_np == 0., axis=1)]

        print(matrice)

        self.signal_model.emit(matrice)

    def set_lim_x(self, x):
        self.lim_x = x

    def set_lim_y_high(self, y):
        self.lim_y_high = y

    def set_lim_y_low(self, y):
        self.lim_y_low = y

    def set_lim_y(self, y):
        self.lim_y = y

    def set_lim_z(self, z):
        self.lim_z = z

    def set_dist_center(self, dist):
        self.dist_center = dist

    def set_angle_y(self, angle):
        self.angle_y = angle
        self.lim_x = self.dist_center * math.tan(math.degrees(angle))

    def set_mode_platform(self):
        self.platform = True
        self.mobile = False

    def set_mode_mobile(self):
        self.platform = False
        self.mobile = True

    def set_mode_test(self):
        self.platform = False
        self.mobile = False

    def setcounter(self, counter):
        self.counterstep = counter

    def reset_verts(self):
        self.model = np.array([[0, 0, 0]])


class GLWidget_Model(QOpenGLWidget):

    def __init__(self):

        super(GLWidget_Model, self).__init__()
        self.zRot = 0
        self.yRot = 0
        self.xRot = 0

        self.lastPos = QPoint()

        self.matrice = np.random.rand(999999).astype(np.float32).reshape(333333, 3)

    def sizeHint(self):
        return QSize(1280, 1280)

    def set_data(self, matrice):
        self.matrice = matrice
        self.update()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)

        glLoadIdentity()

        glRotated(180, 1, 0, 0)

        # gluLookAt(1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glPointSize(1)

        # rotate 3D model
        glRotated(self.xRot / 16, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16, 0.0, 0.0, 1.0)

        # display 3D model
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.matrice)  #Récupération des données pour l'affichage
        glDrawArrays(GL_POINTS, 0, self.matrice.shape[0])  #Affichage des données
        glDisableClientState(GL_VERTEX_ARRAY)

        glFlush()

    def setXRotation(self, angle):
        self.xRot = angle
        self.update()

    def setYRotation(self, angle):
        self.yRot = angle
        self.update()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        #if event.buttons() & Qt.LeftButton:
        self.setXRotation(self.xRot - dx)
        self.setYRotation(self.yRot - dy)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
