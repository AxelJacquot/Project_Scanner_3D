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
                             QStackedWidget, QFormLayout, QDesktopWidget, QFileDialog,)

import OpenGL.GL as gl

from OpenGL.GL import shaders

from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.raw.GL.ARB.vertex_array_object import glGenVertexArrays, \
    glBindVertexArray

from OpenGL import GLU

import pyopencl as cl
import numpy as np
from time import time
from math import pi

import pyrealsense2 as rs
import serial
from serial.tools.list_ports import comports

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
    __kernel void traitement(__global const float *point, __global float *point_prime)
    {
        int test_traitement = 0;
        int i = (get_global_id(0) * 2) + get_global_id(0);
        if(point[i] < 0.5 && point[i] > -0.5){
            if(point[i+1] < 0.5 && point[i+1] > -0.5){
                if(point[i+2] < 0.5 && point[i+2] > -0.5){
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

        self.timer = QTimer(self)       #set timer to execute different action

        # self.rs.init_profile_realsense()

        self.list_view = QComboBox()
        self.list_view.insertItem(0, 'Logo Qt')
        self.list_view.insertItem(1, 'vue Modèle')
        self.list_view.insertItem(2, 'Vue Caméra')

        self.list_view.currentIndexChanged.connect(self.choose_view)

        self.list_view.setMaximumWidth(150)

        self.list_resolution = QComboBox()
        self.list_resolution.insertItem(0, '720p')
        self.list_resolution.insertItem(1, '480p')
        self.list_resolution.insertItem(2, '360p')

        self.list_resolution.setMaximumWidth(150)

        self.glWidget = GLWidget()
        self.glWidget_Model = GLWidget_Model()
        self.glWidget_Camera = GLWidget_Camera()

        self.glWidget.sizeHint()

        self.xyz = QCheckBox("xyz", self)
        self.pcd = QCheckBox("pcd", self)
        self.obj = QCheckBox("obj", self)
        self.stl = QCheckBox("stl", self)
        self.ply = QCheckBox("ply", self)
        self.vtk = QCheckBox("vtk", self)

        self.filename = QLineEdit()
        self.filename.setMaxLength(10)
        self.filename.setMaximumWidth(150)

        self.start_stream = QPushButton("Lancement du stream", self)
        self.start_stream.setMaximumWidth(150)
        self.start_stream.clicked.connect(self.click_stream)

        self.start_scan = QPushButton("Lancement du scan", self)
        self.start_scan.setMaximumWidth(150)
        self.start_scan.clicked.connect(self.click_scan)

        self.quit_button = QPushButton("Quitter", self)
        self.quit_button.setMaximumWidth(150)
        self.quit_button.clicked.connect(self.close)

        self.rs_button = QPushButton("Connecter Caméra", self)
        self.rs_button.setMaximumWidth(150)
        self.rs_button.clicked.connect(self.init_rs)

        self.button_path = QPushButton("Chemin")
        self.button_path.setMaximumWidth(150)
        self.button_path.clicked.connect(self.recover_path)

        self.camera_view_widget = QWidget()
        self.model_view_widget = QWidget()
        self.Logo_Qt_widget = QWidget()

        self.layout_Logo_Qt()
        self.layout_model_view()
        self.layout_camera_view()

        self.stacked = QStackedWidget(self)
        self.stacked.addWidget(self.Logo_Qt_widget)
        self.stacked.addWidget(self.model_view_widget)
        self.stacked.addWidget(self.camera_view_widget)

        fourLayout = QVBoxLayout()
        fourLayout.addWidget(self.xyz)
        fourLayout.addWidget(self.pcd)
        fourLayout.addWidget(self.obj)
        fourLayout.addWidget(self.stl)
        fourLayout.addWidget(self.ply)
        fourLayout.addWidget(self.vtk)

        secondLayout = QFormLayout()
        secondLayout.addRow("Choix de la visualisation", self.list_view)
        secondLayout.addRow("Choix de la résolution", self.list_resolution)
        secondLayout.addRow("Nom des fichiers", self.filename)
        secondLayout.addRow("Choix des formats 3D", fourLayout)
        secondLayout.addRow("Récupération du chemin", self.button_path)
        secondLayout.setAlignment(Qt.AlignRight)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.start_scan)
        buttonLayout.addWidget(self.quit_button)

        thirdLayout = QVBoxLayout()
        thirdLayout.addLayout(secondLayout)
        thirdLayout.addWidget(self.rs_button)
        thirdLayout.addWidget(self.start_stream)
        thirdLayout.addLayout(buttonLayout)
        thirdLayout.setAlignment(Qt.AlignRight)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stacked)
        self.mainLayout.addLayout(thirdLayout)
        self.setLayout(self.mainLayout)

        # self.showFullScreen()
        self.setWindowTitle("Scanner 3D")

    def layout_Logo_Qt(self):
        layout = QHBoxLayout()
        layout.addWidget(self.glWidget)
        self.Logo_Qt_widget.setLayout(layout)

    def layout_camera_view(self):
        layout = QHBoxLayout()
        layout.addWidget(self.glWidget_Camera)
        self.camera_view_widget.setLayout(layout)

    def layout_model_view(self):
        layout = QHBoxLayout()
        layout.addWidget(self.glWidget_Model)
        self.model_view_widget.setLayout(layout)

    def init_rs(self):
        self.rs = RealSense()

    def recover_path(self):
        try:
            dialog = QFileDialog()
            filepath = dialog.getExistingDirectory(self, 'Récupération du chemin')

            if filepath[0]:
                print(filepath)
        except:
            print("error")
            pass

    def click_stream(self):
        self.timer.timeout.connect(self.stream)
        self.timer.start(10)

    def click_scan(self):
        self.timer.timeout.connect(self.scan)
        self.timer.start(10)

    def stream(self):
        self.rs.stream_camera()
        self.rs.signal_camera.connect(self.glWidget_Camera.set_data)

    def scan(self):
        self.rs.recovery_data_model()
        self.rs.signal_model.connect(self.glWidget_Model.set_data)

        """print(self.filename.displayText())
        self.filename.setReadOnly(1)"""

    def closeEvent(self, event):

        reply = QMessageBox.question(self, "Attention Fermeture de l'application",
                                     "Etes vous sur de vouloir quitter ?", QMessageBox.Close |
                                     QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            event.accept()
        else:
            event.ignore()

    def choose_view(self, i):
        self.stacked.setCurrentIndex(i)


class RealSense(QWidget):

    signal_model = pyqtSignal(object)         #signal_camera
    signal_camera = pyqtSignal(object, object)

    def __init__(self, width=1280, height=720):
        super(RealSense, self).__init__()
        self.counterstep = 0

        self.pt = np.array(2)
        #self.portt = self.ports()
        self.init_realsense(width, height)

    def init_realsense(self, width, height):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
        # other_stream, other_format = rs.stream.infrared, rs.format.y8
        other_stream, other_format = rs.stream.color, rs.format.rgb8
        self.config.enable_stream(rs.stream.color, width, height, rs.format.rgb8, 30)
        self.pc = rs.pointcloud()
        # Start streaming
        self.pipeline.start(self.config)
        self.width_rs = width
        self.height_rs = height
        self.init_profile_realsense()

    def init_profile_realsense(self):
        profile = self.pipeline.get_active_profile()
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
        depth_intrinsics = depth_profile.get_intrinsics()
        w, h = depth_intrinsics.width, depth_intrinsics.height
        # Processing blocks

        self.decimate = rs.decimation_filter()
        self.decimate.set_option(rs.option.filter_magnitude, 2 ** 0)
        self.colorizer = rs.colorizer()
        self.filters = [rs.disparity_transform(),
                   rs.spatial_filter(),
                   rs.temporal_filter(),
                   rs.disparity_transform(False)]


    def ask_for_port(self):
        for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
            if desc == "FT232R USB UART":
                self.port = port
                return port
        return 0

    def ports(self):
        port = self.ask_for_port()
        if port == 0:
            reply = QMessageBox.question(self, "Erreur de connexion série",
                                         "Voulez vous ressaye la verification de la connection serie ?",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                port = self.ports()
            else:
                return 0
        else:
            return port

    def stream_camera(self):
        points = rs.points()

        success, frames = self.pipeline.try_wait_for_frames(timeout_ms=0)
        if not success:
            return

        depth_frame = frames.get_depth_frame()
        other_frame = frames.first(rs.stream.color)

        depth_frame = self.decimate.process(depth_frame)

        for f in self.filters:
            depth_frame = f.process(depth_frame)

        # Grab new intrinsics (may be changed by decimation)
        depth_intrinsics = rs.video_stream_profile(
            depth_frame.profile).get_intrinsics()
        w, h = depth_intrinsics.width, depth_intrinsics.height

        color_image = np.asanyarray(other_frame.get_data())

        colorized_depth = self.colorizer.colorize(depth_frame)
        depth_colormap = np.asanyarray(colorized_depth.get_data())

        mapped_frame, color_source = other_frame, color_image

        points = self.pc.calculate(depth_frame)

        self.pc.map_to(mapped_frame)

        vert = np.asarray(points.get_vertices(2))
        texture = np.asarray(points.get_texture_coordinates(2))

        self.signal_camera.emit(vert, texture)

        """
        
        # handle color source or size change
        fmt = '16RGBA'
        global image_data
        if (image_data.format, image_data.pitch) != (fmt, color_source.strides[0]):
            empty = (gl.GLubyte * (w * h * 3))()
            image_data = pyglet.image.ImageData(w, h, fmt, empty)
        # copy image deta to pyglet
        image_data.set_data(fmt, color_source.strides[0], color_source.ctypes.data)

        verts = np.asarray(points.get_vertices(2)).reshape(h, w, 3)
        texcoords = np.asarray(points.get_texture_coordinates(2))

        if len(vertex_list.vertices) != verts.size:
            vertex_list.resize(verts.size // 3)
            # need to reassign after resizing
            vertex_list.vertices = verts.ravel()
            vertex_list.tex_coords = texcoords.ravel()

        copy(vertex_list.vertices, verts)
        copy(vertex_list.tex_coords, texcoords)"""

    def recovery_data_model(self):
        points = rs.points()

        success, frames = self.pipeline.try_wait_for_frames(timeout_ms=0)       #récupération des images
        if not success:
            return

        depth_frame = frames.get_depth_frame()  #récupération de l'image de la profondeur

        depth_frame = self.decimate.process(depth_frame)

        for f in self.filters:          #application des différents filtres
            depth_frame = f.process(depth_frame)

        points = self.pc.calculate(depth_frame)     #calcul des points

        self.pt = np.array(points.get_vertices(2))      #restructuration de la donnée dans des vecteurs n*3

        self.signal_model.emit(self.pt)

    def construct_model(self):
        pass


class GLWidget_Model(QOpenGLWidget):


    def __init__(self):

        super(GLWidget_Model, self).__init__()
        self.zRot = 0
        self.yRot = 0
        self.xRot = 0

        self.lastPos = QPoint()

        self.vert = np.random.rand(999999).astype(np.float32).reshape(333333, 3)

    def set_data(self, vert):
        self.vert = vert
        self.update()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)

        glLoadIdentity()

        gluLookAt(0, 0, 0, 0, 0, 1, 0, -1, 0)

        glPointSize(1)

        #rotate 3D model
        glRotated(self.xRot, 1.0, 0.0, 0.0)
        glRotated(self.yRot, 0.0, 1.0, 0.0)
        glRotated(self.zRot, 0.0, 0.0, 1.0)

        # display 3D model
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vert)
        glDrawArrays(GL_POINTS, 0, self.vert.shape[0])
        glDisableClientState(GL_VERTEX_ARRAY)

        glFlush()

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.update()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot +  dy)
            self.setYRotation(self.yRot +  dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot +  dy)
            self.setZRotation(self.zRot +  dx)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        return angle

class GLWidget_Camera(QOpenGLWidget):


    def __init__(self):

        super(GLWidget_Camera, self).__init__()
        self.zRot = 0
        self.yRot = 0
        self.xRot = 0

        self.lastPos = QPoint()

        self.vert = np.random.rand(99999).astype(np.float32).reshape(33333, 3)
        self.texture = np.random.rand(99999).astype(np.float32).reshape(33333, 3)

    def set_data(self, vert, texture):
        self.vert = vert
        self.texture = texture
        self.update()
    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glPointSize(1)

        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)


        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vert)
        glColorPointer(3, GL_FLOAT, 0, self.texture);
        glDrawArrays(GL_POINTS, 0, self.vert.shape[0])
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        glFlush()

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.update()

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle


class GLWidget(QOpenGLWidget):


    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(1280, 720)

        self.lastPos = QPoint()

        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)

    def getOpenglInfo(self):
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
        """.format(
            gl.glGetString(gl.GL_VENDOR),
            gl.glGetString(gl.GL_RENDERER),
            gl.glGetString(gl.GL_VERSION),
            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        )

        return info

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(1280, 1280)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.update()

    def initializeGL(self):
        print(self.getOpenglInfo())

        self.setClearColor(self.trolltechPurple.darker())
        self.object = self.makeObject()
        gl.glShadeModel(gl.GL_FLAT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

    def paintGL(self):
        gl.glClear(
            gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslated(0.0, 0.0, -10.0)
        gl.glRotated(self.xRot, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot, 0.0, 0.0, 1.0)
        gl.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side,
                      side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)

        gl.glBegin(gl.GL_QUADS)

        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        NumSectors = 400

        for i in range(NumSectors):
            angle1 = (i * 2 * math.pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * math.pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)

        gl.glEnd()
        gl.glEndList()

        return genList

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.setColor(self.trolltechGreen)

        gl.glVertex3d(x1, y1, -0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x3, y3, -0.05)
        gl.glVertex3d(x4, y4, -0.05)

        gl.glVertex3d(x4, y4, +0.05)
        gl.glVertex3d(x3, y3, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.setColor(self.trolltechGreen.darker(250 + int(100 * x1)))

        gl.glVertex3d(x1, y1, +0.05)
        gl.glVertex3d(x2, y2, +0.05)
        gl.glVertex3d(x2, y2, -0.05)
        gl.glVertex3d(x1, y1, -0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        return angle

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
