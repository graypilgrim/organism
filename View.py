import sys
from PyQt4 import QtGui, QtCore

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
		colorsNo = self.organism.GetColorsNo()

		color = QtGui.QColor(0, 0, 0)
		qp.setPen(color)

		qp.setBrush(QtGui.QColor(200, 0, 0))
		qp.drawRect(10, 15, 90, 60)

		qp.setBrush(QtGui.QColor(255, 80, 0, 160))
		qp.drawRect(100, 15, 90, 60)

		qp.setBrush(QtGui.QColor(25, 0, 90, 200))
		qp.drawRect(190, 15, 90, 60)

	def drawRect(self, color)


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	o = Organism(1, 1)
	ex = View()
	sys.exit(app.exec_())
