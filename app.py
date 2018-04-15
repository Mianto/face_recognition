from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QFormLayout, QDialog
import reco
from shutil import copyfile


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(QDialog):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(655, 341)

        # initialising the MainWindow
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # adding veritical lines for separation
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(320, 0, 20, 381))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))

        # Label for Image Name
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 131, 21))
        self.label.setObjectName(_fromUtf8("label"))

        # Input bar for taking Image names
        self.image_name = QtGui.QLineEdit(self.centralwidget)
        self.image_name.setGeometry(QtCore.QRect(20, 60, 251, 41))
        self.image_name.setObjectName(_fromUtf8("image_name"))

        # Label for Image Path
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 110, 111, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        # Input bar for taking Image Path
        self.image_folder = QtGui.QLineEdit(self.centralwidget)
        self.image_folder.setGeometry(QtCore.QRect(20, 150, 256, 41))
        self.image_folder.setObjectName(_fromUtf8("image_folder"))

        # PushButton for copying Image to the folder
        self.pb = QtGui.QPushButton(self.centralwidget)
        self.pb.setGeometry(QtCore.QRect(90, 230, 93, 33))
        self.pb.setObjectName(_fromUtf8("pushButton"))

        # PushButton for starting the recognition window
        self.start_reco = QtGui.QPushButton(self.centralwidget)
        self.start_reco.setGeometry(QtCore.QRect(390, 120, 181, 51))
        self.start_reco.setObjectName(_fromUtf8("start_reco"))

        layout_image = QFormLayout()
        layout_image.addWidget(self.image_name)
        layout_image.addWidget(self.image_folder)
        layout_image.addWidget(self.pb)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 655, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # adding eventlistener to the pushbutton
        self.connect(self.pb, SIGNAL("clicked()"), self.button_click_1)
        self.start_reco.clicked.connect(lambda: self.recog())
        self.setWindowTitle("Facial Recognistion")

    def retranslateUi(self, MainWindow):
        '''
        Function for labeling the element in the GUI
        '''
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Image Name", None))
        self.label_2.setText(_translate("MainWindow", "Image Location", None))
        self.pb.setText(_translate("MainWindow", "Submit", None))
        self.start_reco.setText(_translate(
            "MainWindow", "Start Recognising", None))

    def button_click_1(self):
        '''
        Function for adding more images to the folder
        for facial recognition
        '''
        image_name = self.image_name.text()
        image_folder = self.image_folder.text()
        src_file = str(image_folder) + str(image_name)
        dest_file = '/home/prashant/Documents/Face_reco/face_recognition/' + str(image_name)
        copyfile(src_file, dest_file)

    def recog(self):
        '''
        Function for adding eventListener to buttons
        for starting recognition
        '''
        known_face_encodings = []
        known_face_names = []
        path = '//home//prashant//Documents//Face_reco//face_recognition//Images//*.jpg'
        known_face_encodings, known_face_names = reco.load_images(
            path, known_face_encodings, known_face_names)
        reco.recognise(known_face_encodings, known_face_names)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
