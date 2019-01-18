import random

class Gene():
	def __init__(self, char=None):
		self.possible_chars = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

		if char is None:
			self.set_random_char()
		else:
			self.char = char

	def set_random_char(self):
		self.char = self.possible_chars[random.randint(0, len(self.possible_chars)-1)]

class Chromosome():
	def __init__(self, target, string=None):
		self.genes = []

		if string is None:
			self.fill_genes_randomly(len(target))
		else:
			self.fill_genes_with_string(string)

		self.target = target

		self.fitness = -1

	def fill_genes_randomly(self, length):
		for i in range(length):
			self.genes.append(Gene())

	def fill_genes_with_string(self, string):
		for letter in string:
			self.genes.append(Gene(letter))

	def to_string(self):
		s = ''
		for g in self.genes:
			s += g.char

		return s

	def get_fitness(self):
		if (self.fitness != -1):
			return self.fitness

		self.fitness = 0

		for i in range(len(self.genes)):
			if self.genes[i].char == self.target[i]:
				self.fitness += 1

		return self.fitness

	def mutate(self, mutation_rate):
		self.fitness = -1

		for gene in self.genes:
			if random.uniform(0, 1) <= mutation_rate:
				gene.set_random_char()

class Evolution():
	def __init__(self, target, population_size, num_generations, crossover_rate, mutation_rate):
		self.target = target
		self.population_size = population_size
		self.num_generations = num_generations

		self.crossover_rate = crossover_rate
		self.mutation_rate = mutation_rate

		self.current_generation = []
		################################

	def create_first_generation(self):
		for i in range(self.population_size):
			self.current_generation.append(Chromosome(self.target))

	def start_evolution(self):
		generation_count = 0
		
		for i in range(self.num_generations):
			last_generation = self.current_generation
			next_generation = []

			fittest = self.find_fittest(last_generation)
			if fittest.to_string() == self.target:
				print("\"" + self.target + "\" found after " + str(generation_count) + " generations")
				break

			self.survive(fittest, next_generation)

			crossover_pool = self.create_crossover_pool(last_generation)

			for j in range(len(last_generation)/2 -1):
				if random.uniform(0, 1) <= self.crossover_rate:
					first_parent = self.choose_random_from(crossover_pool)
					second_parent = self.choose_random_from(crossover_pool)

					first_child, second_child = self.perform_crossover(first_parent, second_parent)
					self.survive(first_child, next_generation)
					self.survive(second_child, next_generation)

			while len(next_generation) < len(last_generation):
				self.survive(self.choose_random_from(crossover_pool), next_generation)

			self.current_generation = next_generation

			generation_count += 1

			if i % 50 == 0: print(fittest.to_string() + " " + str( float(100/len(self.target)) * fittest.get_fitness()/100 ))

	def survive(self, chromosome, next_generation):
		chromosome.mutate(self.mutation_rate)
		next_generation.append(chromosome)

	def find_fittest(self, generation):
		fittest = 0
		for chromosome in generation:
			if chromosome.get_fitness() > fittest:
				fittest = chromosome.get_fitness()

		for chromosome in generation:
			if chromosome.get_fitness() == fittest:
				return chromosome

	def choose_random_from(self, generation):
		return generation[random.randint(0, len(generation)-1)]

	def perform_crossover(self, first_parent, second_parent):
		first_parent = first_parent.to_string()
		second_parent = second_parent.to_string()

		split_index = random.randint(1, len(first_parent)-1)

		first_child = first_parent[:split_index] + second_parent[split_index:]
		second_child = second_parent[:split_index] + first_parent[split_index:]

		first_child = Chromosome(self.target, first_child)
		second_child = Chromosome(self.target, second_child)

		return first_child, second_child

	def create_crossover_pool(self, generation):
		pool = generation[:]

		for chromosome in generation:
			for i in range(chromosome.get_fitness()):
				pool.append(chromosome)

		return pool

#args: target, generation size, number of generations, crossover rate, mutation rate
e = Evolution("hello world", 50, 3000, .5, .003)
e.create_first_generation()
e.start_evolution()