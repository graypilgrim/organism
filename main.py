import sys

from PyQt4 import QtGui

from View import View
from MiPlusLambdaAlgorithm import MiPlusLambdaAlgorithm

TIMER_INTERVAL = 600

if len(sys.argv) < 3:
	cellNo = 20
	bodySize = 8
else:
	cellNo = int(sys.argv[1])
	bodySize = int(sys.argv[2])

app = QtGui.QApplication(sys.argv)
view = View(bodySize)

miPlusLambda = MiPlusLambdaAlgorithm(view, cellNo, bodySize)
miPlusLambda.deamon = True
miPlusLambda.start()

# timerPaint = QTimer()
# timerPaint.timeout.connect(view.update)
# timerPaint.start(TIMER_INTERVAL)

sys.exit(app.exec_())
