import sys
import os
import serial
import time

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
# from PyQt5.QtCore import QString
from PyQt5.uic import loadUi


class Window(QMainWindow):
    """Main window."""

    ser = serial.Serial()
    ser.baudrate = 2400
    ser.timeout = 1
    ser.port = "/dev/ttyUSB0"

    def __del__(self):
        print ("Exiting")
        if self.ser.isOpen():
            self.ser.close()
            print ("Closing port: ", self.ser.port)


    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)


        loadUi("rfid.ui", self)
        self.label.setText("Open port to use scanner")
        self.progressBar.reset()
        self.portButton.setDefault(False)

        if os.name in ('nt', 'dos'):
            for i in range (0, 10):
                self.comboBox.addItem("COM{}".format(i))
        else:
            for i in range (0, 5):
                self.comboBox.addItem("/dev/ttyUSB{}".format(i))

        self.portButton.clicked.connect(self.portButtonClicked)
        self.scanButton.clicked.connect(self.scanCard)

    def portButtonClicked(self, checked):
        if checked:
            try:
                self.ser.port = str(self.comboBox.currentText())  # open serial port
                if not self.ser.isOpen():
                    self.ser.open()

                self.label.setText("Press scan to start")
                self.portButton.setText("Close port")
            except:
                self.label.setText("Failed to open serial port")
                self.portButton.setChecked(False)
        else:
            try:
                if self.ser.isOpen():
                    self.ser.close()

                self.portButton.setText("Open port")
                self.label.setText("Open port to use scanner")

            except:
                self.label.setText("Failed to close port")

    def scanCard(self):
        try:
            self.label.setText("Scanning, place card on scanner")
            self.ser.setDTR(True)
            self.progressBar.reset()
            data='0'
            for i in range(0,4):
                data = self.ser.read(12)
                self.progressBar.setValue((i+1) * 25)
                if len(data)==12:
                    self.progressBar.setValue(100)
                    self.label.setText(format(data[1:10].decode('utf-8')))
                    break
            self.ser.setDTR(False)
            self.ser.flushInput()
            if len(data) != 12:
                self.label.setText("No card was detected")
        except:
            self.label.setText("Failed to scan, check serial port")


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)
    # Create and show the application's main window
    win = Window()
    win.show()
    # Run the application's main loop
    sys.exit(app.exec())