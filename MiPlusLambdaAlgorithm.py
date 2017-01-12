import threading
import random
from math import exp
import time

from Chromosome import Chromosome
from Phenotype import Phenotype

class MiPlusLambdaAlgorithm (threading.Thread):
	miValue = 20
	lambdaValue = 30
	population = []
	highestAdaptationValue = 0.0
	mutationFactor = mutationCounter = 17

	def __init__(self, view, cellNo, bodySize):
		threading.Thread.__init__(self)
		self.view = view
		self.cellNo = cellNo
		self.bodySize = bodySize

	def run(self):
		self.SearchForSolution()

	def StrangeFunctionName(self):
		while True:
			chromo = Chromosome(self.cellNo, self.bodySize)
			print("UpdateData")
			self.view.UpdateData(chromo)
			time.sleep(0.1)


	def SearchForSolution(self):
		self.CreateFirstPopulation()
		print("First")
		self.ShowPopulation()

		tempPopulation = self.DrawTemporaryPopulation()
		print("temp")
		self.ShowPopulation(tempPopulation)

		# while not self.StopCondition():
		# 	tempPopulation = self.DrawTemporaryPopulation()
		# 	offspring = self.ReproduceOffspringPopulation(tempPopulation)
		# 	self.ChooseNextPopulation(offspring)
		# 	self.ChooseBestIndividal()

	# def ChooseBestIndividal(self):
	# 	self.view.UpdateData()

	def CreateFirstPopulation(self):
		for i in range(self.miValue):
			chromosome = Chromosome(self.cellNo, self.bodySize)
			self.population.append(chromosome)

	def DrawTemporaryPopulation(self):
		tempPopulation = []
		for i in range(self.lambdaValue):
			index = random.randint(0, self.miValue - 1)
			tempPopulation.append(self.population[index])

		return tempPopulation

	def ReproduceOffspringPopulation(self, tempPopulation):
		offspring = []
		for i in range(self.lambdaValue):
			first = random.randint(0, self.lambdaValue - 1)
			second = random.randint(0, self.lambdaValue - 1)
			newIndividual = self.Interbreed(tempPopulation[first], tempPopulation[second])

			if self.ShouldMutate():
				newIndividual = self.Mutate(newIndividual)

			offspring.append(newIndividual)

		return offspring

	def ChooseNextPopulation(self, offspring):
		sum = 0.0

		offspring.extend(self.population)
		adaptationValue = []

		for i in range(len(offspring)):
			phenotype = Phenotype(self.bodySize)
			phenotype.UpdateBody(offspring[i])
			adaptation = phenotype.GetAdaptation()

			adaptationValue.append(exp(adaptation))
			sum += exp(adaptation)

		probability = []
		for i in range(len(offspring)):
			probability.append(adaptationValue[i] / sum)

		for i in range(1, len(offspring)):
			probability[i] += probability[i - 1]

		result = []
		for i in range(self.miValue):
			val = random.random()

			for i in range(len(probability)):
				if probability[i] >= val >= probability[i]:
					result.append(offspring[i])

		self.population = result

	def ShowPopulation(self, population=None):
		if population == None:
			for i in self.population:
				print(i.genotype)
		else:
			for i in population:
				print(i.genotype)
