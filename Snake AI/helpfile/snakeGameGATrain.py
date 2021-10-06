import pygame
import random
import collections
from helpfile.snakeGameGATest import SnakeGameGATest
from helpfile.snake import Snake
from helpfile.snakeGame import *
from helpfile import neuralNetwork as nn
from helpfile import geneticAlgorithm as ga 
import os


class SnakeGameGATrain(SnakeGameGATest):

	def __init__(self, fps, population, chroms_per_gen, bits_per_weight, num_inputs, num_hidden_layer_nodes, num_outputs):
		
		super().__init__(fps, "", bits_per_weight, num_inputs, num_hidden_layer_nodes, num_outputs)
		self.cur_chrom = 0
		self.frames_alive = 0
		self.chroms_per_gen = chroms_per_gen
		self.population = population
		self.weights = nn.mapChrom2Weights(self.population[self.cur_chrom], self.bits_per_weight, self.num_inputs, self.num_hidden_layer_nodes, self.num_outputs)
		self.fitness_scores = []
		self.game_scores = []
		self.num_generations = 0

	def game_over(self):
		self.fitness_scores.append(self.calc_fitness())
		self.cur_chrom +=1
		self.game_scores.append(self.score)
		if self.cur_chrom == self.chroms_per_gen:
			self.num_generations +=1
			next_generation, best_individual, best_fitness, average_fitness = ga.createNextGeneration(self.population, self.fitness_scores)
			
			self.population = next_generation
			self.cur_chrom  = 0
			self.fitness_scores = []

			average_game_score = sum(self.game_scores)/len(self.game_scores)

			high_score_per_cur_gen = max(self.game_scores)

			print(self.num_generations, self.high_score, average_game_score, high_score_per_cur_gen, average_fitness)

			self.game_scores = []

			file = open("Snake AI\_traininfo\Generations\GAdata.txt", "a+")
			file.write("Generation " + str(self.num_generations) + "\n")
			file.write("Highscore: " + str(high_score_per_cur_gen) + "\n")
			file.write("Best Individual: " + str(best_individual) + "\n")
			file.write("Best Fitness: " + str(best_fitness) + "\n")
			file.write("Average Fitness:" + str(average_fitness) + "\n")
			file.write("Average Game Score:" + str(average_game_score))
			file.write("\n------------------------------------------------------------------------------------------------------\n")
			file.close()

			if self.num_generations%10 == 0:
				abs_file_path = os.path.join(os.getcwd(), "Snake AI\traininfo\Populations\population_" + str(self.num_generations) + ".txt")
				file = open(abs_file_path, "a+")
				file.write(str(self.population))
				file.write("\n")
				file.close()

		self.weights = nn.mapChrom2Weights(self.population[self.cur_chrom], self.bits_per_weight, self.num_inputs, self.num_hidden_layer_nodes, self.num_outputs)

		self.snake = Snake(self.rows,self.cols)
		self.generate_fruit()
		self.restart = True
		if self.score > self.high_score:
			self.high_score = self.score
		self.score = 0
		self.frames_alive = 0
		self.frames_since_last_fruit = 0

	def calc_fitness(self):

		frame_score = self.frames_alive
		if self.frames_since_last_fruit >= 50:
			frame_score = self.frames_alive - self.frames_since_last_fruit
			if frame_score <= 0:
					frame_score = 1

		return ((self.score*2)**2)*(frame_score**1.5)