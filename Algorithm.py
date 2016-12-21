from Organism import Organism
from Chromosome import Chromosome

class Algorithm:
	def __init__(self, organism, chromosome):
		self.organism = organism
		self.chromosome = chromosome

	def StrangeFunctionName(self):
		chromo = Chromosome(self.chromosome.cellNo, self.chromosome.bodySize)
		chromo.RandCells()
		self.organism.UpdateBody(chromo)
