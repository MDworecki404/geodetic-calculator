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
    QGridLayout, QMessageBox,
)
from PyQt5.QtGui import QIcon
from screeninfo import get_monitors
import pandas as pd
import time
from alive_progress import alive_bar
class Direct(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interfejs()

    def interfejs(self):
        global m
        for m in get_monitors():
            continue

        grid = QGridLayout()


        Latitude = QLabel("Latitude: ")
        Latitude.setMaximumWidth(100)
        LatitudeInput = QLineEdit()
        LatitudeInput.setMaximumWidth(100)
        grid.addWidget(Latitude, 0, 0)
        grid.addWidget(LatitudeInput, 0, 1)

        Longitude = QLabel("Longitude: ")
        Longitude.setMaximumWidth(100)
        LongitudeInput = QLineEdit()
        LongitudeInput.setMaximumWidth(100)
        grid.addWidget(LongitudeInput, 1, 1)
        grid.addWidget(Longitude, 1, 0)

        HemiNS = QComboBox()
        HemiNS.setMaximumWidth(100)
        HemiNS.addItem('North')
        HemiNS.addItem('South')
        grid.addWidget(HemiNS, 0, 2)

        HemiWE = QComboBox()
        HemiWE.setMaximumWidth(100)
        HemiWE.addItem('West')
        HemiWE.addItem('East')
        grid.addWidget(HemiWE, 1, 2)

        Azimuth1_2 = QLabel('Azimuth from point 1 to 2: ')
        Azimuth1_2Input = QLineEdit()
        Azimuth1_2.setMaximumWidth(100)
        Azimuth1_2Input.setMaximumWidth(100)
        grid.addWidget(Azimuth1_2, 2,0)
        grid.addWidget(Azimuth1_2Input, 2, 1)

        jump = QLabel('Jump: ')
        jumpInput = QLineEdit()
        jump.setMaximumWidth(100)
        jumpInput.setMaximumWidth(100)
        grid.addWidget(jump,3,0)
        grid.addWidget(jumpInput,3,1)

        ElipsoidalDistance = QLabel("Ellispoidal Distance(in metres): ")
        ElipsoidalDistanceInput = QLineEdit()
        ElipsoidalDistance.setMaximumWidth(200)
        ElipsoidalDistanceInput.setMaximumWidth(100)
        grid.addWidget(ElipsoidalDistance, 2, 2)
        grid.addWidget(ElipsoidalDistanceInput, 2, 3)

        Calculate = QPushButton('Calculate')
        grid.addWidget(Calculate, 4, 1)
        import numpy as np
        def Calculation():

            B = float(LatitudeInput.text())
            L = float(LongitudeInput.text())
            Az1_2 = float(Azimuth1_2Input.text())
            NS = HemiNS.currentText()
            WE = HemiWE.currentText()
            if NS == 'North':
                B = B
            if NS == 'South':
                B = 0-B
            if WE == 'West':
                L = 0-L
            if WE == 'East':
                L = L

            a_GRS80 = 6378137
            b_GRS80 = 6356752.3141
            e2_GRS80 = (a_GRS80 ** 2 - b_GRS80 ** 2) / a_GRS80 ** 2
            B = B * np.pi / 180
            L = L * np.pi / 180
            Az = Az1_2*np.pi/180

            s = float(ElipsoidalDistanceInput.text())
            N = a_GRS80 / np.sqrt(1 - e2_GRS80 * np.sin(B) ** 2)
            M = (1 - e2_GRS80) * a_GRS80 / (np.sqrt(1 - e2_GRS80 * np.sin(B) ** 2)) ** 3

            ds = float(jumpInput.text())
            s1 = 0
            PB = [B * 180/np.pi]
            PL = [L * 180/np.pi]
            df = pd.DataFrame([])
            points = []
            cols = ['B', 'L']
            while s1<s:
                Np = N
                Mp = M
                Bp = B
                dL = ds * np.sin(Az) / (Np * np.cos(Bp))
                L = L + dL
                dB = ds * np.cos(Az) / Mp
                B = B + dB
                N = a_GRS80 / np.sqrt(1 - e2_GRS80 * np.sin(B) ** 2)
                M = (1 - e2_GRS80) * a_GRS80 / (np.sqrt(1 - e2_GRS80 * np.sin(B) ** 2)) ** 3
                Az = Az + ds / Np * np.sin(Az) * np.tan(Bp)
                s1 = s1 + ds
                PB.extend([B * 180 / np.pi])
                PL.extend([L * 180 / np.pi])
                points.append([B, L])


            df = pd.DataFrame(points, columns=cols)

            B_b = B
            L_b = L
            Az_b = Az

            saveRaport = QMessageBox()
            saveRaport.setIcon(QMessageBox.Question)
            saveRaport.setText('Do you want to save the raport?')
            saveRaport.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            retval = saveRaport.exec_()
            if retval == QMessageBox.Yes:
                f = open('raport.txt', 'w')
                f.write(str(df))

            import plotly.graph_objects as go
            fig = go.Figure(go.Scattergeo(mode="lines", lat=PB, lon=PL, marker={'size': 10}))
            fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True, projection_type="orthographic", showocean=True, lakecolor="Blue", showrivers=True, rivercolor="Blue", showcountries=True, countrycolor="RebeccaPurple")
            fig.data[0].line.color = 'rgb(204, 20, 204)'
            fig.update_layout(margin={'l': 0, 't': 0, 'b': 0, 'r': 0},mapbox={"center": {'lon': 150, 'lat': 150}, "style": "stamen-terrain","center": {'lon': 50, 'lat': 50}, "zoom": 1})
            fig.show()

            fig = go.Figure(go.Scattermapbox(mode="lines", lat=PB, lon=PL, marker={'size': 10}))
            fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True, projection_type="orthographic",
                            showocean=True, lakecolor="Blue", showrivers=True, rivercolor="Blue", showcountries=True,
                            countrycolor="RebeccaPurple")
            fig.data[0].line.color = 'rgb(204, 20, 204)'
            fig.update_layout(margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
                              mapbox={"center": {'lon': 150, 'lat': 150}, "style": "stamen-terrain",
                                      "center": {'lon': 50, 'lat': 50}, "zoom": 1})
            fig.show()





        Calculate.clicked.connect(Calculation)
        self.setLayout(grid)
        width = 1000
        height = 800
        self.setGeometry(int(m.width / 2 - width / 2), int(m.height / 2 - height / 2), width, height)
        self.setWindowIcon(QIcon('kalkulator.png'))
        self.setWindowTitle("Vincent's Inverse Formula")
        self.show()