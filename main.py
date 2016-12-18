from Chromosome import Chromosome
from Organism import Organism
from View import View
import sys
from PyQt4 import QtGui, QtCore

if len(sys.argv) < 2:
	print("Error. Body cells and body size required")
	sys.exit(1)

chromo = Chromosome(int(sys.argv[1]), int(sys.argv[2]))
org = Organism(chromo)
org.ColorConnectedComponents()

app = QtGui.QApplication(sys.argv)
ex = View(org)
sys.exit(app.exec_())
