import math
import random

class Organism:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.body = [[random.randint(0, 1) for x in range(width)] for y in range(height)]
		self.colorsNo = 1

	def ShowBody(self):
		for x in range(self.height):
			print(self.body[x])

	def Adaptation(self):
		return self.MomentOfInertia() / self.ConnectedComponents()

	def MomentOfInertia(self):
		result = 0

		for i in range(self.height):
			for k in range(self.width):
				result += self.body[i][k] * self.Distanse(k, i)

		return result

	def ConnectedComponents(self):
		color = 1
		for row in range(self.width):
			for col in range(self.height):
				if self.body[col][row] == 0:
					continue

				if self.body[col][row] == 1:
					color += 1
					self.ColorConnectedComponents(row, col, color)

		self.colorsNo = color
		return self.colorsNo

	def GetColorsNo(self):
		return self.colorsNo

	def Distanse(self, row, col):
		widthCenter = self.width / 2
		heightCenter = self.height / 2
		return math.floor(math.hypot((row + 0.5) - widthCenter, (col + 0.5) - heightCenter))

	def ColorConnectedComponents(self, row, col, color):
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
		rightBoundary = (col == self.width - 1)
		topBoundary = (row == 0)
		bottomBoundary = (row == self.height - 1)

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
