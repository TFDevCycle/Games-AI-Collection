
import random
import itertools
import statistics

def genPopulation(popSize, numBits):


	chromosomes = []

	for _ in range(popSize):

		chromosome = ""

		for _ in range(numBits):

			bit = random.randrange(2)
			chromosome += str(bit)

		chromosomes.append(chromosome)

	return chromosomes

def createNextGeneration(parentPop, fitnessScores):

	fitnessRouletteCutoffs, bestIndividual, bestFitness, averageFitness = assignFitnessRatios(parentPop, fitnessScores)

	childPop = []

	
	bestParents  = extractBestParents(parentPop, fitnessScores)

	for _ in range(len(parentPop) - len(bestParents)):

		selectedPair = selection(parentPop, fitnessRouletteCutoffs)

		child = crossOver(selectedPair)

		child = mutation(child)

		childPop.append(child)

	childPop = childPop + bestParents

	return childPop, bestIndividual, bestFitness, averageFitness


def assignFitnessRatios(parentPop, fitnessScores):


	bestFitness = max(fitnessScores)
	bestIndividual = parentPop[fitnessScores.index(bestFitness)]
	totalScore = sum(fitnessScores)
	averageFitness = totalScore/len(fitnessScores)

	fitnessRatios = []

	totalScore = sum(fitnessScores)
	for score in fitnessScores:
		ratio = score/totalScore
		fitnessRatios.append(ratio)

	fitnessRouletteCutoffs = list(itertools.accumulate(fitnessRatios))

	return fitnessRouletteCutoffs, bestIndividual, bestFitness, averageFitness


def extractBestParents(parentPop, fitnessScores):

	fitnessScoresCopy = fitnessScores.copy()
	fitnessScoresCopy.sort()

	maxIndex = len(fitnessScores) - 1

	bestScoresCutoffIndex = int(maxIndex*(1/2))

	bestScoresCutoff = fitnessScoresCopy[bestScoresCutoffIndex]

	bestParents = []

	for i in range(len(parentPop)):

		if fitnessScores[i] > bestScoresCutoff:
			bestParents.append(parentPop[i])

	return bestParents




def selection(parentPop, fitnessRouletteCutoffs):

	pair = []
	
	for _ in range(2):

		randVal = random.random()

		for i, cutoff in enumerate(fitnessRouletteCutoffs):
			if randVal < cutoff:
				pair.append(parentPop[i])
				break

	return pair

def crossOver(pair):


	randVal = random.randrange(2)
	startWithFirst = True
	if randVal == 0:
		startWithFirst = False

	numBits = len(pair[0])
	crossOverPoint = random.randrange(numBits)

	child = ""
	if startWithFirst:
		if crossOverPoint == numBits - 1:
			child = pair[1]
		else:
			child = pair[0][:crossOverPoint] + pair[1][crossOverPoint:]
	else:
		if crossOverPoint == numBits - 1:
			child = pair[0]
		else:
			child = pair[1][:crossOverPoint] + pair[0][crossOverPoint:]

	return child

def mutation(chrom):

	MUTATION_RATE = .008
	bitList = list(chrom)
	for i,bit in enumerate(bitList):

		randVal = random.random()

		if randVal < MUTATION_RATE:
			if bitList[i] == "0":
				bitList[i] = "1"
			else:
				bitList[i] = "0"

	newString = "".join(bitList)

	return newString



