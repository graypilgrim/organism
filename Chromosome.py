import random
import math
import sys

class Chromosome:
	def __init__(self, cellNo, bodySize):
		self.cellNo = cellNo
		self.bodySize = bodySize
		self.genotype = []

	def RandCells(self):
		seen = set()
		i = 0
		while i < self.cellNo:
			row = random.randint(0, self.bodySize - 1)
			col = random.randint(0, self.bodySize - 1)
			gen = (row, col)
			if gen not in seen:
				self.genotype.append((gen))
				seen.add(gen)
				i += 1
