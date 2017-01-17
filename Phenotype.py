import math

class Phenotype:
	def __init__(self, size):
		self.size = size
		self.body = [[0 for x in range(self.size)] for y in range(self.size)]
		self.colorsNo = -1

	def UseGenotype(self, genotype):
		self.body = [[0 for x in range(self.size)] for y in range(self.size)]
		for i in range(0, len(genotype.positions), 2):
			col = genotype.positions[i]
			row = genotype.positions[i + 1]
			self.body[col][row] = 1

		self.ColorConnectedComponents()

	def ShowBody(self):
		for x in range(self.size):
			print(self.body[x])

	def GetAdaptation(self):
		return self.MomentOfInertia() / self.GetConnectedComponentsNo()

	def MomentOfInertia(self):
		result = 0
		for i in range(self.size):
			for k in range(self.size):
				result += self.body[i][k] * self.Distanse(k, i)

		return result

	def ColorConnectedComponents(self):
		color = 1
		for row in range(self.size):
			for col in range(self.size):

				if self.body[col][row] == 0:
					continue

				if self.body[col][row] == 1:
					color += 1
					self.ColorNeighborhood(row, col, color)

		self.colorsNo = color

	def GetConnectedComponentsNo(self):
		return self.colorsNo

	def Distanse(self, row, col):
		bodyCenter = self.size / 2
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
		rightBoundary = (col == self.size - 1)
		topBoundary = (row == 0)
		bottomBoundary = (row == self.size - 1)

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
