import random

class Chromosome:
	def __init__(self, cellNo, bodySize):
		self.cellNo = cellNo
		self.bodySize = bodySize
		self.genotype = []
		self.RandCells()

	def RandCells(self):
		seen = set()
		i = 0
		while i < self.cellNo:
			row = random.randint(0, self.bodySize - 1)
			col = random.randint(0, self.bodySize - 1)
			gen = (row, col)
			if gen not in seen:
				self.genotype.extend([row, col])
				seen.add(gen)
				i += 1
