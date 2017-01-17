import random
import math

class Genotype:
	def __init__(self, chromoSize, bodySize):
		self.chromoSize = chromoSize
		self.bodySize = bodySize
		self.positions = []
		self.RandCells()

	def RandCells(self):
		seen = set()
		i = 0
		while i < self.chromoSize:
			row = random.randint(0, self.bodySize - 1)
			col = random.randint(0, self.bodySize - 1)
			gen = (row, col)
			if gen not in seen:
				self.positions.extend([row, col])
				seen.add(gen)
				i += 2

	def Interbreed(self, second):
		locus = random.randint(0, self.chromoSize - 1)

		for i in range(locus, self.chromoSize):
			self.positions[i], second.positions[i] = second.positions[i], self.positions[i]

		self.CheckInterbreedMutateMaybe()
		second.CheckInterbreedMutateMaybe()

	def CheckInterbreedMutateMaybe(self):
		chromosomeIncorrect = True

		while chromosomeIncorrect:
			seen = set()
			for i in range(0, self.chromoSize, 2):
				cell = (self.positions[i], self.positions[i+1])
				if cell in seen:
					self.Mutate(i)
					break

			chromosomeIncorrect = False

	def Mutate(self, pos=None):
		print("Mutation called")
		if pos == None:
			pos = random.randint(0, self.chromoSize - 1)

		bitNo = math.ceil(math.log(self.bodySize, 2))
		mutationBit = random.randint(0, bitNo - 1)

		mutationMask = 1 << mutationBit

		if self.positions[pos] & mutationMask == 1:
			self.positions[pos] &= not mutationMask
		else:
			self.positions[pos] &= mutationMask
