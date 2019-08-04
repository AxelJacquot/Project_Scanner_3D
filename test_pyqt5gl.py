
import sys
import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt, QCoreApplication
from PyQt5.QtGui import QColor, QValidator
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QPushButton, QCheckBox, QLabel,
                             QMenu, QMenuBar, QComboBox, QVBoxLayout, QMessageBox, QWidget, QSpinBox, QLineEdit,
                             QStackedWidget, QFormLayout, QDesktopWidget, QFileDialog)

import OpenGL.GL as gl

from OpenGL import GLU

import numpy as np

import pyrealsense2 as rs

"""

        #Récupération de la résolution de l'écran pour pouvoir modifier 
        #la taille de l'affichage ultérieurement

        self.screen_size = QDesktopWidget().screenGeometry()
        print(" Screen size : " + str(self.screen_size.height()) + "x" + str(self.screen_size.width()))

"""

class RealSense():

    def __init__(self):

        super(RealSense, self).__init__()

    def recovery_data(self):
        pass

    def config_resolution(self):
        pass


class Window(QWidget):


    def __init__(self):
        super(Window, self).__init__()

        self.list_view = QComboBox()
        self.list_view.insertItem(0, 'Vue Caméra')
        self.list_view.insertItem(1, 'vue Modèle')
        self.list_view.insertItem(2, 'vue vide')

        self.list_view.currentIndexChanged.connect(self.choose_view)

        self.list_view.setMaximumWidth(150)

        self.list_resolution = QComboBox()
        self.list_resolution.insertItem(0, '720p')
        self.list_resolution.insertItem(1, '480p')
        self.list_resolution.insertItem(2, '360p')

        self.list_resolution.setMaximumWidth(150)

        self.glWidget = GLWidget()
        self.glWidget2 = GLWidget2()

        self.xyz = QCheckBox("xyz", self)
        self.pcd = QCheckBox("pcd", self)
        self.obj = QCheckBox("obj", self)
        self.stl = QCheckBox("stl", self)
        self.ply = QCheckBox("ply", self)
        self.vtk = QCheckBox("vtk", self)

        self.filename = QLineEdit()
        self.filename.setMaxLength(10)
        self.filename.setMaximumWidth(150)

        self.start_scan = QPushButton("Lancement du scan", self)
        self.start_scan.setMaximumWidth(150)
        self.start_scan.clicked.connect(self.click_scan)

        self.quit_button = QPushButton("Quitter", self)
        self.quit_button.setMaximumWidth(150)
        self.quit_button.clicked.connect(self.close)

        self.button_path = QPushButton("Chemin")
        self.button_path.setMaximumWidth(150)
        self.button_path.clicked.connect(self.recover_path)

        self.camera_view_widget = QWidget()
        self.model_view_widget = QWidget()
        self.void_view_widget = QWidget()

        self.layout_camera_view()
        self.layout_model_view()
        self.layout_void_view()


        self.stacked = QStackedWidget(self)
        self.stacked.addWidget(self.camera_view_widget)
        self.stacked.addWidget(self.model_view_widget)
        self.stacked.addWidget(self.void_view_widget)

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
        thirdLayout.addLayout(buttonLayout)
        thirdLayout.setAlignment(Qt.AlignRight)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stacked)
        self.mainLayout.addLayout(thirdLayout)
        self.setLayout(self.mainLayout)

        self.showFullScreen()
        self.setWindowTitle("Scanner 3D")

    def layout_void_view(self):
        layout = QHBoxLayout()
        self.void_view_widget.setLayout(layout)

    def layout_camera_view(self):
        layout = QHBoxLayout()
        layout.addWidget(self.glWidget)
        self.camera_view_widget.setLayout(layout)


    def layout_model_view(self):
        layout = QHBoxLayout()
        layout.addWidget(self.glWidget2)
        self.model_view_widget.setLayout(layout)


    def recover_path(self):
        print("ici")
        try:
            dialog = QFileDialog()
            filepath = dialog.getExistingDirectory(self, 'Récupération du chemin')

            if filepath[0]:
                print(filepath)
        except:
            print("error")
            pass

    def click_scan(self):
        print(self.filename.displayText())
        self.filename.setReadOnly(1)


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

class GLWidget2(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        self.parent = parent
        QOpenGLWidget.__init__(self, parent)
        self.yRotDeg = 0.0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

    def initializeGL(self):
        #self.qglClearColor(QtGui.QColor(0, 0,  150))
        self.initGeometry()

        gl.glEnable(gl.GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        if height == 0: height = 1

        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glLoadIdentity()
        gl.glTranslate(0.0, 0.0, -50.0)
        gl.glScale(20.0, 20.0, 20.0)
        gl.glRotate(self.yRotDeg, 0.2, 1.0, 0.3)
        gl.glTranslate(-0.5, -0.5, -0.5)

        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glVertexPointerf(self.cubeVtxArray)
        gl.glColorPointerf(self.cubeVtxArray)
        gl.glDrawElementsui(gl.GL_QUADS, self.cubeIdxArray)

    def initGeometry(self):
        self.cubeVtxArray = np.array(
                [[0.0, 0.0, 0.0],
                 [1.0, 0.0, 0.0],
                 [1.0, 1.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [0.0, 0.0, 1.0],
                 [1.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0],
                 [0.0, 1.0, 2.0],
                 [0.8, 1.2, 2.5]])
        self.cubeIdxArray = [
                0, 1, 2, 3,
                3, 2, 6, 7,
                1, 0, 4, 5,
                2, 1, 5, 6,
                0, 3, 7, 4,
                7, 6, 5, 4 ]
        """self.cubeClrArray = [
                [0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 1.0],
                [0.0, 1.0, 1.0 ]]"""

    def spin(self):
        self.yRotDeg = (self.yRotDeg  + 1) % 360.0
        self.parent.statusBar().showMessage('rotation %f' % self.yRotDeg)
        self.updateGL()

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

        self.lastPos = event.pos()

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle


class GLWidget(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

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
        return QSize(800, 800)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
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
        gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
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
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
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
