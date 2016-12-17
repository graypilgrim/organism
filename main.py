from Organism import Organism
from View import View
import sys
from PyQt4 import QtGui, QtCore

org = Organism(30, 30)
app = QtGui.QApplication(sys.argv)
o = Organism(1, 1)
ex = View(o)
sys.exit(app.exec_())
