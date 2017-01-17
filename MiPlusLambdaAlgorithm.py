import threading
import random
import math
import time
import copy

from Genotype import Genotype
from Phenotype import Phenotype

class MiPlusLambdaAlgorithm (threading.Thread):
	miValue = 10
	lambdaValue = 20
	population = []
	offspring = []
	mutationFactor = mutationCounter = 2

	currentAdaptationValue = 0.0
	lastAdaptationValue = 0.0
	adaptationDelta = 0.00004
	lastAdaptationValuesBelowDelta = 0
	maxValuesBelowDelta = 300


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

	def SearchForSolutionOneIteration(self):
		self.CreateFirstPopulation()
		print("First")
		self.ShowPopulation()

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

		print("Solution found: " + str(self.currentAdaptationValue))


	def SearchForSolution(self):
		self.CreateFirstPopulation()

		while not self.StopCondition():
			tempPopulation = self.DrawTemporaryPopulation()
			self.ReproduceOffspringPopulation(tempPopulation)
			self.ChooseNextPopulation()
			self.ChooseBestIndividal()
			time.sleep(0.1)

		print("Solution found: " + str(self.currentAdaptationValue))

	def CreateFirstPopulation(self):
		for i in range(self.miValue):
			genotype = Genotype(self.chromoSize, self.bodySize)
			self.population.append(genotype)

	def DrawTemporaryPopulation(self):
		tempPopulation = []
		for i in range(self.lambdaValue):
			index = random.randint(0, self.miValue - 1)
			tempPopulation.append(copy.deepcopy(self.population[index]))

		return tempPopulation

	def ReproduceOffspringPopulation(self, tempPopulation):
		self.offspring = []
		for i in range(0, self.lambdaValue, 2):
			tempPopulation[i].Interbreed(tempPopulation[i+1])

			if self.ShouldMutate():
				tempPopulation[i].Mutate()
				self.mutationCounter = self.mutationFactor

			self.offspring.append(tempPopulation[i])
			self.offspring.append(tempPopulation[i+1])

	def ShouldMutate(self):
		self.mutationCounter -= 1
		return self.mutationCounter == 0

	def CreateRouletteWheel(self, individualsToChoose):
		sum = 0.0

		adaptationValue = []

		for i in range(len(individualsToChoose)):
			phenotype = Phenotype(self.bodySize)
			phenotype.UseGenotype(individualsToChoose[i])
			adaptation = phenotype.GetAdaptation()

			adaptationValue.append(math.exp(adaptation))
			sum += math.exp(adaptation)

		rouletteWheel = []
		for i in range(len(individualsToChoose)):
			rouletteWheel.append(adaptationValue[i] / sum)

		for i in range(1, len(individualsToChoose)):
			rouletteWheel[i] += rouletteWheel[i - 1]

		return rouletteWheel

	def ChooseNextPopulation(self):
		individualsToChoose = self.SumPopulations()

		rouletteWheel = self.CreateRouletteWheel(individualsToChoose)

		result = []
		seen = set()
		added = 0
		while added < self.miValue:
			val = random.random()
			prev = 0.0
			for i in range(len(rouletteWheel)):
				if prev <= val <= rouletteWheel[i] and i not in seen:
					result.append(individualsToChoose[i])
					seen.add(i)
					added += 1
				prev = rouletteWheel[i]

		self.population = result

	def ChooseBestIndividal(self):
		phenotype = Phenotype(self.bodySize)
		indexBest = -1
		adaptationBest = 0.0

		for i in range(self.miValue):
			phenotype.UseGenotype(self.population[i])
			if phenotype.GetAdaptation() > adaptationBest:
				indexBest = i
				adaptationBest = phenotype.GetAdaptation()

		self.lastAdaptationValue = self.currentAdaptationValue
		self.currentAdaptationValue = adaptationBest
		print("Current best: " + str(adaptationBest))

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
				if self.offspring[i].positions == self.population[j].positions:
					absent = False
					break

			if absent:
				result.append(self.offspring[i])

		return result

	def ShowPopulation(self, population=None):
		if population == None:
			for i in self.population:
				print(i.positions)
		else:
			for i in population:
				print(i.positions)
