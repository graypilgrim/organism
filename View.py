import sys
from PyQt4 import QtGui, QtCore
import random

WIDTH = 800
HEIGHT = 600

class View(QtGui.QWidget):

	def __init__(self, organism):
		super(View, self).__init__()
		self.organism = organism
		self.initUI()

	def initUI(self):
		self.setGeometry(200, 200, WIDTH, HEIGHT)
		self.setWindowTitle('Organism')
		self.show()

	def paintEvent(self, e):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawMatrix(qp)
		qp.end()

	def drawMatrix(self, qp):
		rgbColors = self.chooseColors()

		horizBoxSide = WIDTH // self.organism.bodySize
		vertBoxSide = HEIGHT // self.organism.bodySize

		boxSide = min(horizBoxSide, vertBoxSide)

		color = QtGui.QColor(0, 0, 0)
		qp.setPen(color)

		for col in range(self.organism.bodySize):
			for row in range(self.organism.bodySize):
				color = rgbColors[self.organism.body[col][row]]
				qp.setBrush(QtGui.QColor(color[0], color[1], color[2]))
				qp.drawRect(row*boxSide, col*boxSide, boxSide, boxSide)

	def chooseColors(self):
		rgbColors = []
		colorsNo = self.organism.GetConnectedComponentsNo()

		rgbColors.append((255, 255, 255))

		for i in range(1, colorsNo + 1):
			r = random.randint(0, 255)
			g = random.randint(0, 255)
			b = random.randint(0, 255)
			rgbColors.append((r, g, b))

		return rgbColors

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	o = Organism(1, 1)
	ex = View()
	sys.exit(app.exec_())
