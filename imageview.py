from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QPointF, QRectF, QThreadPool, QRunnable
from PyQt5.QtGui import QImage, QPaintEvent, QPainter, QBrush, QColor
from PyQt5.QtWidgets import (
	QApplication, QDialog, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget,
	QLabel, QTextEdit, QLineEdit, QPushButton, QFrame, QFormLayout,
	QCheckBox, QScrollArea, QSizePolicy, QMessageBox,
)
from vector import Vector

class ImageView(QWidget):

	def __init__(self, app, data: bytes, parent=None):
		self.app = app
		self.img = QImage('/tmp/mouse.jpg')
		self.backup = QImage('/tmp/mouse.jpg')

		self.imgWidth = 256
		self.imgHeight = 256
		self.imgScale = 25

		self.data = data
		self.dataOffset = 0
		self.dataXStride = 4
		self.dataYStrideFixed = 256
		self.dataYStrideRel = 4

		self.dataROffs = 0
		self.dataGOffs = 1
		self.dataBOffs = 2
		# self.dataAOffs = 0

		self.dataProc = DataProcessor(self)

		super().__init__(parent)

	def setScale(self, scale):
		self.imgScale = scale
		self.app.updateScaleSlider()
		self.repaint()

	def setWidth(self, w):
		self.imgWidth = w
		self.app.updateWidthSlider()
		self.updateImage()

	def setHeight(self, h):
		self.imgHeight = h
		self.app.updateHeightSlider()
		self.updateImage()

	def wheelEvent(self, wheee):
		modifiers = QApplication.keyboardModifiers()
		if modifiers == Qt.ControlModifier:
			self.setScale(self.imgScale + wheee.angleDelta().y() / 120)
		else:
			wheee.ignore()

	def paintEvent(self, paintEvent: QPaintEvent):
		painter = QPainter(self)
		img = self.img
		if self.img is None:
			img = self.backup

		view = Vector(self.size().width(), self.size().height())

		scale = 2 ** (5 * (self.imgScale - 25) / 25)
		imgSize = Vector(img.width(), img.height()) * scale
		pos = view / 2 - imgSize / 2
		br = view / 2 + imgSize / 2
		painter.drawImage(
			QRectF(
				QPointF(pos.values[0], pos.values[1]),
				QPointF(br.values[0], br.values[1]),
			),
			self.img
		)

	def updateImage(self):
		self.dataProc.updateImage()
		self.repaint()

class DataProcessor(QThreadPool):
	def __init__(self, imgView):
		super().__init__()
		self.setMaxThreadCount(1)
		self.imgView = imgView

	def updateImage(self):
		self.clear()
		return self.start(ImageRunnable(self.imgView))

class ImageRunnable(QRunnable):
	def __init__(self, imgView):
		self.imgView = imgView
		super().__init__()

	def run(self):
		imgView = self.imgView
		w, h = imgView.imgWidth, imgView.imgHeight
		img = QImage(w, h, QImage.Format_ARGB32)
		img.fill(QColor(255, 255, 255))

		for y in range(0, h):
			for x in range(0, w):
				pixOffs = imgView.dataOffset \
					+ imgView.dataYStrideFixed * y \
					+ imgView.dataYStrideRel * x * y \
					+ imgView.dataXStride * x
				c = QColor(0, 0, 0)
				c.setRed(imgView.data[pixOffs + imgView.dataROffs])
				c.setGreen(imgView.data[pixOffs + imgView.dataGOffs])
				c.setBlue(imgView.data[pixOffs + imgView.dataBOffs])
				img.setPixelColor(x, y, c)

		self.imgView.img = img
