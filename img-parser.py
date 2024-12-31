#!/usr/bin/env python3

from imageview import ImageView

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QTextCursor, QIntValidator
from PyQt5.QtWidgets import (
	QApplication, QDialog, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget,
	QLabel, QTextEdit, QLineEdit, QPushButton, QFrame, QFormLayout,
	QCheckBox, QScrollArea, QSizePolicy, QMessageBox, QSplitter, QSlider,
)
import sys
import json


class App(QDialog):
	# on_stop_signal = pyqtSignal(object)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setMinimumSize(800, 800)
		self.hbox = QHBoxLayout(self)
		self.imgView = ImageView(self, data)
		self.control = self.createControlPanel()
		splitter = QSplitter(self)
		splitter.addWidget(self.control)
		splitter.addWidget(self.imgView)
		self.hbox.addWidget(splitter)

		self.imgView.updateImage()

	def createControlPanel(self):
		ctrl = QWidget(self)
		ctrl.setMinimumSize(200, 100)

		topLevel = QFormLayout(ctrl)
		topLevel.setRowWrapPolicy(QFormLayout.WrapAllRows)

		scaleSlider = QSlider(Qt.Horizontal)
		scaleSlider.setRange(1, 50)
		scaleSlider.setValue(self.imgView.imgScale)

		def setImgScale(val):
			self.imgView.setScale(val)
		scaleSlider.valueChanged.connect(setImgScale)
		topLevel.addRow('Image scale', scaleSlider)
		self.scaleSlider = scaleSlider

		widthSlider = QSlider(Qt.Horizontal)
		widthSlider.setRange(1, 2048)
		widthSlider.setValue(self.imgView.imgWidth)

		def setImgWidth(val):
			self.imgView.setWidth(val)
		widthSlider.valueChanged.connect(setImgWidth)
		topLevel.addRow('Image width', widthSlider)
		self.widthSlider = widthSlider

		heightSlider = QSlider(Qt.Horizontal)
		heightSlider.setRange(1, 2048)
		heightSlider.setValue(self.imgView.imgHeight)

		def setImgHeight(val):
			self.imgView.setHeight(val)
		heightSlider.valueChanged.connect(setImgHeight)
		topLevel.addRow('Image height', heightSlider)
		self.heightSlider = heightSlider

		return ctrl

	def updateScaleSlider(self):
		self.scaleSlider.setValue(int(self.imgView.imgScale))

	def updateWidthSlider(self):
		self.widthSlider.setValue(int(self.imgView.imgWidth))

	def updateHeightSlider(self):
		self.heightSlider.setValue(int(self.imgView.imgHeight))

path = "./Textures/T_CNS1154_SaveFairy_C.ubulk"
with open(path, "rb") as file:
	data = file.read()

if __name__ == '__main__':
	exitCode = -1
	try:
		app = QApplication(sys.argv)

		window = App()
		window.show()
		exitCode = app.exec()
	except Exception as e:
		print(e)

	sys.exit(exitCode)
