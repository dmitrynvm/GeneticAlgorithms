def FitnessFunction1(self, totalFitness, maxFitness, k):
    denominator = k * (maxFitness + 1) - totalFitness
    numerator = maxFitness - self.OptFunction() + 1
    self.fitness = numerator / denominator
    return self.fitness
