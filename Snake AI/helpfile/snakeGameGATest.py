import pygame
import random
import collections
from helpfile.snakeGame import SnakeGame
from helpfile.snake import Snake
from helpfile import neuralNetwork as nn

class SnakeGameGATest(SnakeGame):
	def __init__(self, fps, chromosome, bits_per_weight, num_inputs, num_hidden_layer_nodes, num_outputs):

		super().__init__(fps)
		self.frames_since_last_fruit = 0
		self.bits_per_weight = bits_per_weight
		self.num_inputs = num_inputs
		self.num_hidden_layer_nodes = num_hidden_layer_nodes
		self.num_outputs = num_outputs
		if chromosome != "":
			self.weights = nn.mapChrom2Weights(chromosome, self.bits_per_weight, self.num_inputs, self.num_hidden_layer_nodes, self.num_outputs)
	
	
	def move_snake(self):
		
		head = self.snake.body[0]

		dist_left_fruit = self.manhattan_distance(head[0],head[1]-1)
		dist_up_fruit = self.manhattan_distance(head[0]-1,head[1])
		dist_right_fruit = self.manhattan_distance(head[0],head[1]+1)
		dist_down_fruit = self.manhattan_distance(head[0]+1, head[1])

		constant = 20
		open_spaces_left = self.calc_open_spaces((head[0], head[1]-1))/constant
		open_spaces_up = self.calc_open_spaces((head[0]-1, head[1]))/constant
		open_spaces_right = self.calc_open_spaces((head[0], head[1]+1))/constant
		open_spaces_down = self.calc_open_spaces((head[0]+1, head[1]))/constant

		length = self.score + 1
	
		network_inputs = [dist_left_fruit, dist_up_fruit, dist_right_fruit, dist_down_fruit,  open_spaces_left, open_spaces_up, open_spaces_down, open_spaces_right, length]

		outputs = nn.testNetwork(network_inputs, self.weights, self.num_hidden_layer_nodes, self.num_outputs)
		max_output = max(outputs)
		if max_output == outputs[0]:
			direct = "left"
		elif max_output == outputs[1]:
			direct = "up"
		elif max_output == outputs[2]:
			direct = "right"
		else:
			direct = "down"

		self.snake.directions.appendleft(direct)
		if len(self.snake.directions) > len(self.snake.body):
			self.snake.directions.pop()

		self.snake.update_body_positions()

	def manhattan_distance(self, y_head, x_head):
		return abs(self.fruit_pos[0] - y_head) + abs(self.fruit_pos[1] - x_head)

	def calc_open_spaces(self,start_pos):
		open_spaces = 0

		start_y = start_pos[1]
		start_x = start_pos[0]

		if start_pos in self.snake.body or (start_x < 0 or start_x >= self.cols or start_y < 0 or start_y >= self.rows):
				return 0
		visited = set([start_pos])
		queue = collections.deque([start_pos])

		while len(queue) > 0:

			cur = queue.popleft()

			possible_moves = self.get_possible_moves(cur)

			for move in possible_moves:
				if move not in visited:

					visited.add(move)

					if move not in self.snake.body:
						open_spaces +=1
						queue.append(move)

		return open_spaces

	def get_possible_moves(self,cur):

		adjacent_spaces = [(cur[0], cur[1]-1), (cur[0]-1,cur[1]), (cur[0], cur[1]+1), (cur[0]+1, cur[1])]
		possible_moves = []
		for move in adjacent_spaces:
			move_y = move[1]
			move_x = move[0]
			if move_x >= 0 and move_x < self.cols and move_y >= 0 and move_y < self.rows:
					possible_moves.append(move)
		return possible_moves


	def check_fruit_collision(self):
		if self.snake.body[0] == self.fruit_pos:
			self.snake.extend_snake()
			self.generate_fruit()

			self.score += 1
			self.frames_since_last_fruit = 0


	def update_frames_since_last_fruit(self):
		
		self.frames_since_last_fruit += 1
		if (self.frames_since_last_fruit == 50 and self.score < 6) or self.frames_since_last_fruit == 250:
			self.game_over()

	
	def game_over(self):

		self.snake = Snake(self.rows,self.cols)
		self.generate_fruit()
		self.restart = True
		if self.score > self.high_score:
			self.high_score = self.score
		self.score = 0
		self.frames_since_last_fruit = 0




