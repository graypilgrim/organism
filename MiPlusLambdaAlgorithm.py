import threading
import random
import math
import time

from Chromosome import Chromosome
from Phenotype import Phenotype

class MiPlusLambdaAlgorithm (threading.Thread):
	miValue = 15
	lambdaValue = 20
	population = []
	offspring = []
	mutationFactor = mutationCounter = 7

	currentAdaptationValue = 0.0
	lastAdaptationValue = 0.0
	adaptationDelta = 0.00004
	lastAdaptationValuesBelowDelta = 0
	maxValuesBelowDelta = 10


	def __init__(self, view, cellNo, bodySize):
		threading.Thread.__init__(self)
		self.view = view
		self.chromoSize = cellNo * 2
		self.bodySize = bodySize

	def run(self):
		self.SearchForSolution()

	def StrangeFunctionName(self):
		print("TEST: ")
		tempGeno = [0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7,
					1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0,
					7, 1, 7, 2, 7, 3, 7, 4, 7, 5]


		self.view.UpdateData(tempGeno)


	def SearchForSolution(self):
		self.CreateFirstPopulation()
		print("First")
		self.ShowPopulation()

		while not self.StopCondition():
			tempPopulation = self.DrawTemporaryPopulation()
			print("temp")
			self.ShowPopulation(tempPopulation)

			self.ReproduceOffspringPopulation(tempPopulation)
			print("offspring")
			self.ShowPopulation(self.offspring)

			self.ChooseNextPopulation()
			print("nextPopulation")
			self.ShowPopulation()

			self.ChooseBestIndividal()
			time.sleep(0.1)

		print("Solution found: " + str(self.currentAdaptationValue))

	def CreateFirstPopulation(self):
		for i in range(self.miValue):
			chromosome = Chromosome(self.chromoSize // 2, self.bodySize)
			self.population.append(chromosome.genotype)

	def DrawTemporaryPopulation(self):
		tempPopulation = []
		for i in range(self.lambdaValue):
			index = random.randint(0, self.miValue - 1)
			tempPopulation.append(list(self.population[index]))

		return tempPopulation

	def ReproduceOffspringPopulation(self, tempPopulation):
		self.offspring = []
		for i in range(0, self.lambdaValue, 2):
			self.Interbreed(tempPopulation[i], tempPopulation[i+1])

			if self.ShouldMutate():
				self.Mutate(tempPopulation[i])

			self.offspring.append(tempPopulation[i])
			self.offspring.append(tempPopulation[i+1])

	def Interbreed(self, first, second):
		locus = random.randint(0, self.chromoSize - 1)

		for i in range(locus, self.chromoSize):
			first[i], second[i] = second[i], first[i]

		while not self.CheckInterbreedMutateMaybe(first):
			pass

		while not self.CheckInterbreedMutateMaybe(second):
			pass

	def CheckInterbreedMutateMaybe(self, genotype):
		seen = set()
		for i in range(0, self.chromoSize, 2):
			cell = (genotype[i], genotype[i+1])
			if cell in seen:
				self.Mutate(genotype, i)
				return False

		return True

	def ShouldMutate(self):
		self.mutationCounter -= 1
		return self.mutationCounter == 0

	def Mutate(self, genotype, pos=None):
		print("Mutation called")
		if pos == None:
			pos = random.randint(0, self.chromoSize - 1)

		bitNo = math.ceil(math.log(self.bodySize, 2))
		mutationBit = random.randint(0, bitNo - 1)

		mutationMask = 1 << mutationBit

		if genotype[pos] & mutationMask == 1:
			genotype[pos] &= not mutationMask
		else:
			genotype[pos] &= mutationMask

		self.mutationCounter = self.mutationFactor

	def ChooseNextPopulation(self):
		sum = 0.0

		individualsToChoose = self.SumPopulations()

		print("sum:")
		self.ShowPopulation(individualsToChoose)

		adaptationValue = []

		for i in range(len(individualsToChoose)):
			phenotype = Phenotype(self.bodySize)
			phenotype.UpdateBody(individualsToChoose[i])
			adaptation = phenotype.GetAdaptation()

			print(str(i) + ": " + str(adaptation))

			adaptationValue.append(math.exp(adaptation))
			sum += math.exp(adaptation)

		probability = []
		for i in range(len(individualsToChoose)):
			probability.append(adaptationValue[i] / sum)

		for i in range(1, len(individualsToChoose)):
			probability[i] += probability[i - 1]

		print("probability:")
		print(probability)

		print("crating")
		result = []
		seen = set()
		added = 0
		while added < self.miValue:
			val = random.random()
			prev = 0.0
			for i in range(len(probability)):
				if prev <= val <= probability[i] and i not in seen:
					result.append(individualsToChoose[i])
					seen.add(i)
					added += 1
				prev = probability[i]

		self.population = result

	def ChooseBestIndividal(self):
		phenotype = Phenotype(self.bodySize)
		indexBest = -1
		adaptationBest = 0.0

		for i in range(self.miValue):
			phenotype.UpdateBody(self.population[i])
			if phenotype.GetAdaptation() > adaptationBest:
				indexBest = i
				adaptationBest = phenotype.GetAdaptation()

		self.lastAdaptationValue = self.currentAdaptationValue
		self.currentAdaptationValue = adaptationBest

		self.view.UpdateData(self.population[indexBest])

	def StopCondition(self):
		if self.currentAdaptationValue - self.lastAdaptationValue < self.adaptationDelta:
			self.lastAdaptationValuesBelowDelta += 1
			if self.lastAdaptationValuesBelowDelta == self.maxValuesBelowDelta:
				return True
		else:
			self.lastAdaptationValuesBelowDelta = 0
		return False

	def SumPopulations(self):
		result = []

		for i in range(self.miValue):
			result.append(self.population[i])

		for i in range(self.lambdaValue):
			absent = True
			for j in range(self.miValue):
				if self.offspring[i] == self.population[j]:
					absent = False
					break

			if absent:
				result.append(self.offspring[i])

		return result

	def ShowPopulation(self, population=None):
		if population == None:
			for i in self.population:
				print(i)
		else:
			for i in population:
				print(i)
