import pygame
import random
import collections
from helpfile import neuralNetwork  as nn
from helpfile import geneticAlgorithm as ga 
from helpfile.snake import Snake


class SnakeGame():

	def __init__(self, fps):

		self.width = 500
		self.height = 600
		self.grid_start_y = 50
		self.win = pygame.display.set_mode((self.width, self.height))
		self.play = True
		self.restart = False
		self.clock = pygame.time.Clock()
		self.fps = fps
		self.rows = 10
		self.cols = self.rows
		self.snake = Snake(self.rows,self.cols)
		self.fruit_pos = (0,0)
		self.generate_fruit()
		self.score = 0
		self.high_score = 0
		
	def redraw_window(self):

		self.win.fill(pygame.Color(104, 60, 135))
		self.draw_data_window()
		self.draw_grid()
		self.draw_grid_updates()
		pygame.display.update()

	def draw_data_window(self):

		pygame.draw.rect(self.win, pygame.Color(20, 20, 20), (0,0,self.width, self.grid_start_y))

		font = pygame.font.SysFont('calibri', 20)
		score_text = font.render('Score: ' + str(self.score),1, (255,255,255))
		high_score_text = font.render('High Score: ' + str(self.high_score), 1, (255,255,255))
		self.win.blit(score_text, (30, 10))
		self.win.blit(high_score_text, (self.width - 140, 10))

	def draw_grid(self):

		space_col = self.width//self.cols
		space_row = (self.height - self.grid_start_y)//self.rows

		for i in range(self.rows):
			pygame.draw.line(self.win, pygame.Color(100,100,100), (0, space_row*i + self.grid_start_y),  (self.width, space_row*i + self.grid_start_y))

		for i in range(self.cols):
			pygame.draw.line(self.win, pygame.Color(100,100,100), (space_col*i, self.grid_start_y), (space_col*i, self.height))

		pygame.draw.line(self.win, pygame.Color(100,100,100), (space_col*self.rows-2, self.grid_start_y), (space_col*self.rows-2, self.height))
		pygame.draw.line(self.win, pygame.Color(100,100,100), (0, self.height -2),  (self.width, self.height -2))

	def generate_fruit(self):

		fruit_row = random.randrange(0,self.rows)
		fruit_col = random.randrange(0,self.cols)

		while (fruit_row, fruit_col) in self.snake.body:

			fruit_row = random.randrange(0,self.rows)
			fruit_col = random.randrange(0,self.cols)


		self.fruit_pos = (fruit_row,fruit_col)

	def move_snake(self):
		
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			direct = "left"
		elif keys[pygame.K_UP]:
			direct = "up"
		elif keys[pygame.K_RIGHT]:
			direct = "right"
		elif keys[pygame.K_DOWN]:
			direct = "down"
		else:
			if len(self.snake.directions) == 0:
				direct = "right"
			else:
				direct = self.snake.directions[0]

		self.snake.directions.appendleft(direct)
		if len(self.snake.directions) > len(self.snake.body):
			self.snake.directions.pop()

		self.snake.update_body_positions()


	def draw_grid_updates(self):

		space_col = self.width//self.cols
		space_row = (self.height - self.grid_start_y)//self.rows

		fruit_y = self.fruit_pos[0]
		fruit_x = self.fruit_pos[1]
		pygame.draw.rect(self.win, pygame.Color(250,30,30), (space_col*fruit_x+1, self.grid_start_y + space_row*fruit_y+1, space_col-1, space_row-1))

		for pos in self.snake.body:
			pos_y = pos[0]
			pos_x = pos[1]
			
			pygame.draw.rect(self.win, pygame.Color(255,255,255), (space_col*pos_x+1, self.grid_start_y + space_row*pos_y+1, space_col-1, space_row-1))

		
		head = self.snake.body[0]
		head_y = head[0]
		head_x = head[1]
		head_dir = self.snake.directions[0]


		if head_dir == "left":
			pygame.draw.circle(self.win, pygame.Color(100,100,100), (space_col*head_x+space_col//10, self.grid_start_y + space_row*head_y + (space_row*4)//5), 2)
			pygame.draw.circle(self.win, pygame.Color(100,100,100), (space_col*head_x+space_col//10, self.grid_start_y + space_row*head_y + space_row//5), 2)
		elif head_dir == "up":
			pygame.draw.circle(self.win, pygame.Color(100,100,100), (space_col*head_x+space_col//5, self.grid_start_y + space_row*head_y + space_row//10), 2)
			pygame.draw.circle(self.win, pygame.Color(100,100,100), (space_col*head_x+(space_col*4)//5, self.grid_start_y + space_row*head_y + space_row//10), 2)
		elif head_dir == "right":
			pygame.draw.circle(self.win, pygame.Color(100,100,100), (space_col*head_x+(space_col*9)//10, self.grid_start_y + space_row*head_y + space_row//5), 2)
			pygame.draw.circle(self.win, pygame.Color(100,100,100), (space_col*head_x+(space_col*9)//10, self.grid_start_y + space_row*head_y + (space_row*4)//5), 2)
		else:
			pygame.draw.circle(self.win, pygame.Color(100,100,100), (space_col*head_x+space_col//5, self.grid_start_y + space_row*head_y + (space_row*9)//10), 2)
			pygame.draw.circle(self.win, pygame.Color(100,100,100), (space_col*head_x+(space_col*4)//5, self.grid_start_y + space_row*head_y + (space_row*9)//10), 2)


	def check_collisions(self):

		self.check_fruit_collision()
		self.check_wall_collision()
		self.check_body_collision()

	def check_fruit_collision(self):
		if self.snake.body[0] == self.fruit_pos:
			self.snake.extend_snake()
			self.generate_fruit()

			self.score += 1

	def check_wall_collision(self):

		head = self.snake.body[0]
		head_y = head[0]
		head_x = head[1]

		if head_x == self.cols or head_y == self.rows or head_x < 0 or head_y < 0:
			self.game_over()

	def check_body_collision(self):

		if len(self.snake.body) > 1:
			head = self.snake.body[0]
			body_without_head = self.snake.body[1:]

			if head in body_without_head:
				self.game_over()

	def event_handler(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False
				pygame.quit()
				quit()

	def game_over(self):

		self.snake = Snake(self.rows,self.cols)
		self.generate_fruit()
		self.restart = True
		if self.score > self.high_score:
			self.high_score = self.score
		self.score = 0