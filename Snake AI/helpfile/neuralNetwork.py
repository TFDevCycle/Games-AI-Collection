
import random
import itertools
import math

def mapChrom2Weights(chrom, bitsPerWeight, numInputs, numHiddenLayerNodes, numOutputs):

	weightList = initializeWeightList(numInputs, numHiddenLayerNodes, numOutputs)

	chrom  =  " " + chrom
	
	hiddenLayer1BitsEnd = bitsPerWeight*(numInputs+1)*numHiddenLayerNodes
	index = 1
	node_num = 0
	numWeightsPerCurNode = 0

	while index < hiddenLayer1BitsEnd:
		weightBitString = chrom[index:index+bitsPerWeight]

		weightList[0][node_num][numWeightsPerCurNode] = bin2Weight(weightBitString)
		numWeightsPerCurNode +=1

		if numWeightsPerCurNode == numInputs + 1:
			node_num += 1
			numWeightsPerCurNode = 0
		index += bitsPerWeight


	hiddenLayer2BitsEnd = hiddenLayer1BitsEnd + numHiddenLayerNodes*(numHiddenLayerNodes + 1)*bitsPerWeight
	node_num = 0
	numWeightsPerCurNode = 0

	while index < hiddenLayer2BitsEnd:
		weightBitString = chrom[index:index+bitsPerWeight]

		weightList[1][node_num][numWeightsPerCurNode] = bin2Weight(weightBitString)
		numWeightsPerCurNode +=1

		if numWeightsPerCurNode == numHiddenLayerNodes + 1:
			node_num += 1
			numWeightsPerCurNode = 0
		index += bitsPerWeight

	outputBitsEnd = hiddenLayer2BitsEnd + numOutputs*(numHiddenLayerNodes + 1)*bitsPerWeight
	node_num = 0
	numWeightsPerCurNode = 0

	while index < outputBitsEnd:
		weightBitString = chrom[index:index+bitsPerWeight]
		weightList[2][node_num][numWeightsPerCurNode] = bin2Weight(weightBitString)
		numWeightsPerCurNode +=1
		if numWeightsPerCurNode == numHiddenLayerNodes + 1:
			node_num += 1
			numWeightsPerCurNode = 0

		index += bitsPerWeight

	return weightList


def initializeWeightList(numInputs, numHiddenNodes, numOutputs):

	inputToHidden1Ws = []
	hidden1ToHidden2Ws = []
	hidden2ToOutputWs = []

	for i in range(numHiddenNodes): 
		curInputWs = []
		for j in range(numInputs + 1):
			curInputWs.append(0)
		inputToHidden1Ws.append(curInputWs)


	for i in range(numHiddenNodes): 
		curInputWs = []
		for j in range(numHiddenNodes + 1): 
			curInputWs.append(0)
		hidden1ToHidden2Ws.append(curInputWs)

	for i in range(numOutputs):
		curInputWs = []
		for j in range(numHiddenNodes + 1): 
			curInputWs.append(0)
		hidden2ToOutputWs.append(curInputWs)

	weightStructure = [inputToHidden1Ws] + [hidden1ToHidden2Ws] + [hidden2ToOutputWs]


	return weightStructure



def bin2Weight(binString):

	bitsPerWeight = len(binString)

	integer = int(binString, 2)

	product = 3/(2**(bitsPerWeight-1))

	normalized_weight = integer*product - 3

	return normalized_weight


def testNetwork(inputList, weightList, numHiddenLayerNodes, numOutputs):

	inputList.append(-1)

	hiddenLayer1Outputs = calcHiddenLayerOutputs(inputList, weightList[0], numHiddenLayerNodes)

	hiddenLayer1Outputs.append(-1)

	hiddenLayer2Outputs = calcHiddenLayerOutputs(hiddenLayer1Outputs, weightList[1], numHiddenLayerNodes)
	hiddenLayer2Outputs.append(-1)

	finalOutputs = []
	for outputWeightList in weightList[2]:

		finalOutput = calcOutputForNeuron(hiddenLayer2Outputs, outputWeightList) 
		finalOutputs.append(finalOutput)

	return finalOutputs

def calcHiddenLayerOutputs(inputList, weightList, numHiddenLayerNodes):

	hiddenLayerOutputs = []

	for i in range(numHiddenLayerNodes):
		output = calcOutputForNeuron(inputList, weightList[i])
		hiddenLayerOutputs.append(output)

	return hiddenLayerOutputs


def calcOutputForNeuron(inputList, weights):

	weightedSum = 0
	for j in range(len(weights)):
		inputVal = inputList[j]
		weightedSum += inputVal*weights[j]

	output = sigmoid(weightedSum)
	
	return output

def sigmoid(s):

	return 1 / (1 + math.exp(-s))
	








