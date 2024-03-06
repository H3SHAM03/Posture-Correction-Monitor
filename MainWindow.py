from PyQt5 import QtWidgets, uic, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QVBoxLayout,QMessageBox
import sys
import serial
import threading
from Stopwatch import *

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("GUI.ui", self)
        self.ui.full_menu.setHidden(True)
        self.GraphWidget1 = PlotWidget()
        self.GraphWidget2 = PlotWidget()
        self.GraphWidget3 = PlotWidget()
        self.GraphWidget1.setXRange(0,10,padding=0)
        self.GraphWidget2.setXRange(0,10,padding=0)
        self.GraphWidget3.setXRange(0,10,padding=0)
        self.GraphWidget3.setYRange(-1,2,padding=0)
        self.GraphWidget3.setLimits(xMin=0,yMin=-1,yMax=2)
        self.ser = serial.Serial('COM5',timeout=1)
        self.FlexData = []
        self.FsrData = []
        self.WornData = []
        self.CorrectData = []
        self.FlexTimes = []
        self.FsrTimes = []
        self.GlobalTimes = []
        self.FlexSW = Stopwatch()
        self.FsrSW = Stopwatch()
        self.GlobalSW = Stopwatch()
        self.second = 0
        self.ispaused = False
        self.minFlex = float('inf')
        self.minFsr = float('inf')
        self.maxFlex = float('-inf')
        self.maxFsr = float('-inf')
        self.data_line_flex = self.GraphWidget1.plot(pen='r',name='Flex')
        self.data_line_fsr = self.GraphWidget2.plot(pen='g',name='FSR')
        self.data_line_stats = self.GraphWidget3.plot(pen='y',name='Stats')

        layout1=QVBoxLayout()
        layout1.addWidget(self.GraphWidget1)
        self.ui.widget_11.setLayout(layout1)
        layout2=QVBoxLayout()
        layout2.addWidget(self.GraphWidget2)
        self.ui.widget_9.setLayout(layout2)
        layout3=QVBoxLayout()
        layout3.addWidget(self.GraphWidget3)
        self.ui.widget_12.setLayout(layout3)


        self.ui.Monitor.clicked.connect(self.MonitoringMode)
        self.ui.Monitor2.clicked.connect(self.MonitoringMode)
        self.ui.Statistics.clicked.connect(self.StatisticsMode)
        self.ui.Statistics2.clicked.connect(self.StatisticsMode)
        self.ui.pushButton_9.clicked.connect(self.UpdateSidebar)
        self.ui.exit.clicked.connect(self.Exiting)
        self.ui.exit2.clicked.connect(self.Exiting)
        self.ui.clear.clicked.connect(lambda: self.ClearGraph(1))
        self.ui.clear2.clicked.connect(lambda: self.ClearGraph(2))
        self.ui.pushButton.clicked.connect(self.Pause)

        self.ReadThread = threading.Thread(target=self.ReadData)
        self.ReadThread.start()


    def ReadData(self):
        self.FlexSW.start()
        self.FsrSW.start()
        self.GlobalSW.start()
        while True:
            data = str(self.ser.readline().decode('ascii'))
            data = data.replace('\r\n','')
            if data != '':
                data = data.split('/')
                FlexData = data[0]
                FsrData = data[1]
            else:
                FlexData = FsrData = ''

            if FlexData != '' and FsrData != '':
                self.ui.label_2.setText(str(FlexData))
                self.ui.label_6.setText(str(FsrData))
                self.FlexData.append(float(FlexData))
                self.FsrData.append(float(FsrData))
                FlexSec = self.FlexSW.secondsPassed()
                FsrSec = self.FsrSW.secondsPassed()
                self.FlexTimes.append(FlexSec)
                self.FsrTimes.append(FsrSec)
                self.data_line_flex.setData(self.FlexTimes, self.FlexData)
                self.data_line_fsr.setData(self.FsrTimes, self.FsrData)
                self.GlobalTimes.append(self.GlobalSW.secondsPassed())
                self.UpdateViewBox()
                if float(FlexData)>49:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    warn = '[' + str(current_time) + ']: ' + 'Abnormal temperature(%.2f °C)' %float(FlexData)
                    self.CorrectData.append(0)
                else:
                    self.CorrectData.append(1)

                if  float(FsrData)>0:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    warn = '[' + str(current_time) + ']: ' + 'Humidity(%.2f °C)' %float(FsrData)
                    self.WornData.append(1)
                else:
                    self.WornData.append(0)
                self.data_line_stats.setData(self.GlobalTimes,self.WornData)
                threading.Thread(target=self.GetStatistics).start()

    def GetStatistics(self):
        if min(self.FlexData) < self.minFlex:
            self.minFlex = min(self.FlexData)
            self.ui.label_18.setText(str(int(self.minFlex)))
        if min(self.FsrData) < self.minFsr:
            self.minFsr = min(self.FsrData)
            self.ui.label_20.setText(str(int(self.minFsr)))   
        if max(self.FlexData) > self.maxFlex:
            self.maxFlex = max(self.FlexData)
            self.ui.label_19.setText(str(int(self.maxFlex)))
        if max(self.FsrData) > self.maxFsr:
            self.maxFsr = max(self.FsrData)
            self.ui.label_21.setText(str(int(self.maxFsr)))
        WornPercent = (self.WornData.count(1) / len(self.WornData))*100
        self.ui.label_23.setText(str(int(WornPercent))+'%')
        CorrectPercent = (self.CorrectData.count(1) / len(self.CorrectData))*100
        self.ui.label_25.setText(str(int(CorrectPercent))+'%')

    def UpdateViewBox(self):
        if self.FlexTimes[-1] > 10:
            self.GraphWidget1.setXRange(self.FlexTimes[-1]-10,self.FlexTimes[-1])
        if self.FsrTimes[-1] > 10:
            self.GraphWidget2.setXRange(self.FsrTimes[-1]-10,self.FsrTimes[-1])
        if self.GlobalTimes[-1] > 10 and self.ispaused == False:
            self.GraphWidget3.setXRange(self.GlobalTimes[-1]-10,self.GlobalTimes[-1])

    def Pause(self):
        if self.ispaused == False:
            self.ui.pushButton.setText('Back to Real-Time')
            self.ispaused = True
        else:
            self.ui.pushButton.setText('Free Scroll')
            self.ispaused = False

    def ErrorMsg(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def ClearGraph(self,index):
        if index == 1:
            self.FlexTimes = []
            self.FlexData = []
            self.data_line_flex.clear()
            self.GraphWidget1.setXRange(0,10,padding=0)
            self.FlexSW.reset()
            self.FlexSW.start()
        elif index == 2:
            self.FsrTimes = []  
            self.FsrData = []
            self.data_line_fsr.clear()
            self.GraphWidget2.setXRange(0,10,padding=0)
            self.FsrSW.reset()
            self.FsrSW.start()

    def UpdateSidebar(self):
        if self.ui.pushButton_9.isChecked() == True:
            self.ui.Monitor2.setHidden(True)
            self.ui.Statistics2.setHidden(True)
            self.ui.exit2.setHidden(True)
        else:
            self.ui.Monitor2.setHidden(False)
            self.ui.Statistics2.setHidden(False)
            self.ui.exit2.setHidden(False)

    def StatisticsMode(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.stackedWidget_2.setCurrentIndex(1)

    def MonitoringMode(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_2.setCurrentIndex(0)

    def Exiting(self):
        self.ser.close()
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.ser.close()
        return super().closeEvent(a0)