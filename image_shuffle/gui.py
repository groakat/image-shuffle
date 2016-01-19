from PySide import QtCore, QtGui
import sys
import image_shuffle as S


class ShuffleGui(QtGui.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ShuffleGui, self).__init__(*args, **kwargs)

        self.folder = ''

        self.setup_layout()
        self.show()

    def connect_signals(self):
        self.btn_open_folder.clicked.connect(self.open_folder)
        self.btn_shuffle.clicked.connect(self.shuffle)
        self.btn_unshuffle.clicked.connect(self.unshuffle)

    def setup_layout(self):
        self.layout = QtGui.QGridLayout(self)
        self.cw = QtGui.QWidget(self)


        self.le_folder = QtGui.QLineEdit(self)
        self.btn_open_folder = QtGui.QPushButton(self)
        self.btn_shuffle = QtGui.QPushButton(self)
        self.btn_unshuffle = QtGui.QPushButton(self)

        self.btn_open_folder.setText("Open Folder")
        self.btn_shuffle.setText("Shuffle")
        self.btn_unshuffle.setText("Un-Shuffle")

        self.layout.addWidget(self.le_folder, 0, 0, 1, 2)
        self.layout.addWidget(self.btn_open_folder, 0, 2)
        self.layout.addWidget(self.btn_shuffle, 1, 0)
        self.layout.addWidget(self.btn_unshuffle, 1, 2)

        self.cw.setLayout(self.layout)

        self.setCentralWidget(self.cw)

        self.connect_signals()

    def open_folder(self):
        fn = QtGui.QFileDialog.getExistingDirectory()

        self.folder = fn
        self.le_folder.setText(self.folder)

    def shuffle(self):
        if self.folder:
            if S.test_if_shuffled(self.folder):
                msg_box = QtGui.QMessageBox()
                msg_box.setText("It looks as images in folder are already shuffled.\n(If you want to shuffle anyway, please remove the 'key.csv' file in the target folder.)")
                msg_box.exec_()
                return
            else:
                S.shuffle(self.folder)
        else:
            msg_box = QtGui.QMessageBox()
            msg_box.setText("Please select a folder first")
            msg_box.exec_()

    def unshuffle(self):
        if self.folder:
            S.unshuffle(self.folder)
            S.remove_keys(self.folder)
        else:
            msg_box = QtGui.QMessageBox()
            msg_box.setText("Please select a folder first")
            msg_box.exec_()




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    w = ShuffleGui()

    # app.connect(app, QtCore.SIGNAL("aboutToQuit()"), w.exit)
    # w.quit.connect(app.quit)

    sys.exit(app.exec_())