from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
    QGridLayout,
)
from PyQt5.QtGui import QIcon
from screeninfo import get_monitors




class Inverse(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def interfejs(self):
        for m in get_monitors():
            continue
        ukladT = QGridLayout()
        #Starting Coordinates
        StartLatitude = QLabel("Starting Latitude:", self)
        StartLatitude.setMaximumWidth(100)
        StartLongitude = QLabel("Starting Longitude:", self)
        StartLongitude.setMaximumWidth(100)
        StartLatitudeInput = QLineEdit(self)
        StartLatitudeInput.setMaximumWidth(100)
        StartLongitudeInput = QLineEdit(self)
        StartLongitudeInput.setMaximumWidth(100)
        StartNS = QComboBox(self)
        StartNS.setMaximumWidth(100)
        PlanetSide1 = QLabel("Starting point hemispheres: ")
        StartNS.addItem("North")
        StartNS.addItem("South")
        StartWE = QComboBox(self)
        StartWE.setMaximumWidth(100)
        StartWE.addItem("West")
        StartWE.addItem("East")

        ukladT.addWidget(StartLatitude, 0, 0)
        ukladT.addWidget(StartLongitude, 1, 0)
        ukladT.addWidget(StartLatitudeInput, 0, 1)
        ukladT.addWidget(StartLongitudeInput, 1, 1)
        ukladT.addWidget(PlanetSide1, 2, 0)
        ukladT.addWidget(StartNS, 2, 1)
        ukladT.addWidget(StartWE, 2, 2)

        #Ending Coordinates
        EndLatitude = QLabel("Ending Latitude:", self)
        EndLatitude.setMaximumWidth(100)
        EndLongitude = QLabel("Ending Longitude:", self)
        EndLongitude.setMaximumWidth(100)
        EndLatitudeInput = QLineEdit(self)
        EndLatitudeInput.setMaximumWidth(100)
        EndLongitudeInput = QLineEdit(self)
        EndLongitudeInput.setMaximumWidth(100)
        EndNS = QComboBox(self)
        EndNS.setMaximumWidth(100)
        PlanetSide1 = QLabel("Ending point hemispheres: ")
        EndNS.addItem("North")
        EndNS.addItem("South")
        EndWE = QComboBox(self)
        EndWE.setMaximumWidth(100)
        EndWE.addItem("West")
        EndWE.addItem("East")
        Distance = QLabel()

        ukladT.addWidget(EndLatitude, 0, 3)
        ukladT.addWidget(EndLongitude, 1, 3)
        ukladT.addWidget(EndLatitudeInput, 0, 4)
        ukladT.addWidget(EndLongitudeInput, 1, 4)
        ukladT.addWidget(PlanetSide1, 2, 3)
        ukladT.addWidget(EndNS, 2, 4)
        ukladT.addWidget(EndWE, 2, 5)
        ukladT.addWidget(Distance, 4, 3)






        calculateButton = QPushButton("Calculate", self)
        ukladT.addWidget(calculateButton, 3, 2)




        #Calculations
        import numpy as np
        import pyperclip
        import plotly.graph_objects as go

        def Calculation():

            B1 = float(StartLatitudeInput.text())
            L1 = float(StartLongitudeInput.text())
            #print(B1, L1)
            StartHemiNS = StartNS.currentText()
            StartHemiWE = StartWE.currentText()
            B2 = float(EndLatitudeInput.text())
            L2 = float(EndLongitudeInput.text())
            #print(B2, L2)
            EndHemiNS = EndNS.currentText()
            EndHemiWE = EndWE.currentText()
            print(EndHemiWE)
            #print(StartHemiNS)
            if StartHemiNS == 'North':
                B1 = B1
            if StartHemiNS == 'South':
                B1 = 0-B1
            if StartHemiWE == 'West':
                L1 = 0-L1
            if StartHemiWE == 'East':
                L1 = L1
            if EndHemiNS == 'North':
                B2 = B2
            if EndHemiNS == 'South':
                B2 = 0-B2
            if EndHemiWE == 'West':
                L2 = 0-L2
            if EndHemiWE == 'East':
                L2 = L2

            a = 6378137
            b = 6356752.3141
            e2 = (a**2 - b**2)/a**2
            f = (a - b) / a
            B_p = B1*np.pi/180
            L_p = L1*np.pi/180
            B_k = B2*np.pi/180
            L_k = L2*np.pi/180

            #print('B_p: ', B_p, B_p * 180 / np.pi, 'L_p: ', L_p, L_p * 180 / np.pi)
            #print('B_k: ', B_k, B_k * 180 / np.pi, 'L_k: ', L_k, L_k * 180 / np.pi)

            U1 = np.arctan((1 - f) * np.tan(B_p))
            U2 = np.arctan((1 - f) * np.tan(B_k))

            L = L_k - L_p
            Lambda = L

            for i in range(10):
                Lambda_prev = Lambda
                sinSigma = np.sqrt((np.cos(U2)*np.sin(Lambda))**2+(np.cos(U1)*np.sin(U2)-np.sin(U1)*np.cos(U2)*np.cos(Lambda))**2)
                cosSigma = np.sin(U1) * np.sin(U2) + np.cos(U1) * np.cos(U2) * np.cos(Lambda)
                sigma = np.arctan2(sinSigma, cosSigma)
                sinAlfa = np.cos(U1) * np.cos(U2) * np.sin(Lambda) / sinSigma
                cos2Sigmam = cosSigma - (2 * np.sin(U1) * np.sin(U2) / (1 - sinAlfa ** 2))
                C = f / 16 * (1 - sinAlfa ** 2) * (4 + f * (4 - 3 * (1 - sinAlfa ** 2)))
                Lambda = L + (1 - C) * f * sinAlfa *(sigma+C*sinSigma*(cos2Sigmam+C*cosSigma*(-1+2*cos2Sigmam**2)))
                if abs(Lambda - Lambda_prev) < 1e-12:
                    break
                u2 = (1 - sinAlfa ** 2) * (a ** 2 - b ** 2) / (b ** 2)
                A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
                B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
                deltaSigma = B * sinSigma * (cos2Sigmam + B / 4 * (cosSigma *(-1+2*cos2Sigmam**2)-B/6*cos2Sigmam*(-3+4*sinSigma**2)*(-3+4*cos2Sigmam**2)))
                s = b * A * (sigma - deltaSigma)
                Az_12 = np.arctan2((np.cos(U2) * np.sin(Lambda)),(np.cos(U1)*np.sin(U2)-np.sin(U1)*np.cos(U2)*np.cos(Lambda)))
                Az_21 = np.arctan2((np.cos(U1) * np.sin(Lambda)),((-np.sin(U1)) * np.cos(U2) + np.cos(U1) * np.sin(U2) * np.cos(Lambda)))
                #print('Az_12', (Az_12) * 180 / np.pi)
                #print('Az_21', (np.pi + Az_21) * 180 / np.pi)
                #print('S ', s)

                Distance.setText(f'Distance: {s} meters\nAzimuth from point 1 to point 2: {Az_12*180/np.pi}°\nAzimuth from point 2 to 1: {Az_21*180/np.pi}')




        calculateButton.clicked.connect(Calculation)

        # przypisanie utworzonego układu do okna
        self.setLayout(ukladT)
        width = 1000
        height = 800
        self.setGeometry(int(m.width/2-width/2), int(m.height/2-height/2), width, height)
        self.setWindowIcon(QIcon('kalkulator.png'))
        self.setWindowTitle("Vincent's Inverse Formula")
        self.show()



