import math
import random

class Organism:
	def __init__(self, chromosome):
		self.chromosome = chromosome
		self.bodySize = chromosome.bodySize
		self.body = [[0 for x in range(self.bodySize)] for y in range(self.bodySize)]

		for i in chromosome.genotype:
			col = i[1]
			row = i[0]
			self.body[col][row] = 1
		self.colorsNo = 1

	def ShowBody(self):
		for x in range(self.bodySize):
			print(self.body[x])

	def Adaptation(self):
		return self.MomentOfInertia() / self.GetConnectedComponentsNo()

	def MomentOfInertia(self):
		result = 0

		for i in range(self.bodySize):
			for k in range(self.bodySize):

				result += self.body[i][k] * self.Distanse(k, i)

		return result

	def ColorConnectedComponents(self):
		color = 1
		for row in range(self.bodySize):
			for col in range(self.bodySize):

				if self.body[col][row] == 0:
					continue

				if self.body[col][row] == 1:
					color += 1
					self.ColorNeighborhood(row, col, color)

		self.colorsNo = color

	def GetConnectedComponentsNo(self):
		return self.colorsNo

	def Distanse(self, row, col):
		bodyCenter = self.bodySize / 2
		return math.floor(math.hypot((row + 0.5) - bodyCenter, (col + 0.5) - bodyCenter))

	def ColorNeighborhood(self, row, col, color):
		self.body[col][row] = color

		neighbors = self.FindNeighbors(col, row)

		while neighbors:
			coordinates = neighbors.pop()
			x = int(coordinates[0])
			y = int(coordinates[1])
			self.body[y][x] = color
			neighbors.extend(self.FindNeighbors(y, x))

	def FindNeighbors(self, col, row):
		leftBoundary = (col == 0)
		rightBoundary = (col == self.bodySize - 1)
		topBoundary = (row == 0)
		bottomBoundary = (row == self.bodySize - 1)

		neighbors = []

		if not topBoundary:
			if not leftBoundary and self.body[col-1][row-1] == 1:
				neighbors.append((row-1, col-1))

			if self.body[col][row-1] == 1:
				neighbors.append((row-1, col))

			if not rightBoundary and self.body[col+1][row-1] == 1:
				neighbors.append((row-1, col+1))

		if not leftBoundary:
			if self.body[col-1][row] == 1:
				neighbors.append((row, col-1))

		if not rightBoundary:
			if self.body[col+1][row] == 1:
				neighbors.append((row, col+1))

		if not bottomBoundary:
			if not leftBoundary and self.body[col-1][row+1] == 1:
				neighbors.append((row+1, col-1))

			if self.body[col][row+1] == 1:
				neighbors.append((row+1, col))

			if not rightBoundary and self.body[col+1][row+1] == 1:
				neighbors.append((row+1, col+1))

		return neighbors
