import random
import math
import sys

class Chromosome:
	def __init__(self, cellNo, bodySize):
		if (cellNo > bodySize**2):
			print("Invalid data. More cells than available body size")
			sys.exit(1)

		self.cellNo = cellNo
		self.bodySize = bodySize

		seen = set()
		self.genotype = []
		i = 0
		while i < cellNo:
			row = random.randint(0, bodySize - 1)
			col = random.randint(0, bodySize - 1)
			gen = (row, col)
			if gen not in seen:
				self.genotype.append((gen))
				seen.add(gen)
				i += 1
