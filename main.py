from MainWindow import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('Posture Correction Monitor')
    window.setWindowIcon(QtGui.QIcon('icon.png'))
    window.show()
    sys.exit(app.exec_())