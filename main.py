import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QTimer

from Chromosome import Chromosome
from Organism import Organism
from View import View
from Algorithm import Algorithm

TIMER_INTERVAL = 100

if len(sys.argv) < 3:
	print("Error. Body cells and body size required")
	sys.exit(1)

cellNo = int(sys.argv[1])
bodySize = int(sys.argv[2])

chromo = Chromosome(cellNo, bodySize)
org = Organism(bodySize)
algo = Algorithm(org, chromo)

app = QtGui.QApplication(sys.argv)
ex = View(org)

timerCalc = QTimer()
timerCalc.timeout.connect(algo.StrangeFunctionName)

timerPaint = QTimer()
timerPaint.timeout.connect(ex.update)

timerCalc.start(TIMER_INTERVAL)
timerPaint.start(TIMER_INTERVAL)

sys.exit(app.exec_())
