import sys
import argparse

from PyQt4 import QtGui

from View import View
from Algorithm import Algorithm

parser = argparse.ArgumentParser(description="Program using genetic algorithms")
parser.add_argument("bodySize", type=int, help="number of cells in one row of square matrix")
parser.add_argument("cellsNo", type=int, help="number of cells occupied by the organism")
parser.add_argument("algorithm", type=int, choices=[0, 1], help="use on of the provided algorithms, 0 for (mi+lambda), 1 for (mi, lambda)")

args = parser.parse_args()
bodySize = args.bodySize
cellsNo = args.cellsNo
miPlusLambda = args.algorithm == 0

app = QtGui.QApplication(sys.argv)
view = View(bodySize)

algorithm = Algorithm(view, bodySize, cellsNo, miPlusLambda)
algorithm.deamon = True
algorithm.start()

sys.exit(app.exec_())
