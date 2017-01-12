from PyQt4 import QtGui
import random

from Phenotype import Phenotype

WIDTH = 800
HEIGHT = 600

class View(QtGui.QWidget):

	def __init__(self, bodySize):
		super(View, self).__init__()
		self.phenotype = Phenotype(bodySize)
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

		horizBoxSide = WIDTH // self.phenotype.size
		vertBoxSide = HEIGHT // self.phenotype.size

		boxSide = min(horizBoxSide, vertBoxSide)

		color = QtGui.QColor(0, 0, 0)
		qp.setPen(color)

		for col in range(self.phenotype.size):
			for row in range(self.phenotype.size):
				color = rgbColors[self.phenotype.body[col][row]]
				qp.setBrush(QtGui.QColor(color[0], color[1], color[2]))
				qp.drawRect(row*boxSide, col*boxSide, boxSide, boxSide)

	def chooseColors(self):
		rgbColors = []
		colorsNo = self.phenotype.GetConnectedComponentsNo()

		rgbColors.append((255, 255, 255))

		for i in range(1, colorsNo + 1):
			r = random.randint(0, 255)
			g = random.randint(0, 255)
			b = random.randint(0, 255)
			rgbColors.append((r, g, b))

		return rgbColors

	def UpdateData(self, chromosome):
		self.phenotype.UpdateBody(chromosome)
		self.update()
