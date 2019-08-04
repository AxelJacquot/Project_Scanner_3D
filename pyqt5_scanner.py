from PyQt5.QtWidgets import QApplication, QPushButton, QLabel,QMessageBox,QBoxLayout,QComboBox,QCheckBox,QMenuBar,\
    QMenu,QMainWindow
import sys

class Test(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        Button = QPushButton("Lancement",self)
        Button.move(30, 50)

        self.label = QLabel(self)
        self.label.move(200, 110)

        checkbox = QCheckBox('xyz',self)

        Button.clicked.connect(self.lancement_click)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Scanner 3D')
        self.show()

    def lancement_click(self):
        self.label.setText("Bouton cliqué")
        self.label.adjustSize()
        print('ici')

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Test()
    sys.exit(app.exec_())