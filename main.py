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
from PyQt5.uic.properties import QtCore
from PyQt5.QtCore import Qt

from Inverse import Inverse
from Direct import Direct

from screeninfo import get_monitors
class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.interface()

    def inverseFormula(self, checked):
        self.w = Inverse()
        self.w.show()

    def directFormula(self, checked):
        self.w = Direct()
        self.w.show()

    def interface(self):

        for m in get_monitors():
            continue

        grid = QGridLayout()

        choose = QLabel('Choose a method')
        choose.setAlignment(Qt.AlignCenter)
        grid.addWidget(choose, 0, 1)

        directButton = QPushButton("Vincenty's direct")
        directButton.clicked.connect(self.directFormula)

        grid.addWidget(directButton, 1, 0)




        inverseButton = QPushButton("Vincenty's inverse")
        grid.addWidget(inverseButton, 1, 2)
        inverseButton.clicked.connect(self.inverseFormula)





        self.setLayout(grid)
        width = 400
        height = 200
        self.setGeometry(int(m.width / 2 - width / 2), int(m.height / 2 - height / 2), width, height)
        self.setWindowTitle("Geodetic Calculators")
        self.show()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = MainWindow()
    sys.exit(app.exec_())