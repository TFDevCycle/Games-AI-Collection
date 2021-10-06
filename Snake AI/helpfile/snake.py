import collections

class Snake():

	def __init__(self,rows,cols):

		self.rows = rows
		self.cols = cols
		self.body = []
		self.body.append(self.initialize_snake())
		self.directions = collections.deque()

	def initialize_snake(self):
		snake_row = self.rows//2
		snake_col = 1

		return (snake_row,snake_col)

	def update_body_positions(self):
	
		for i,pos in enumerate(self.body):

			direct = self.directions[i]

			if direct == "left":

				self.body[i] = (pos[0],pos[1]-1)		
			elif direct == "up":

				self.body[i] = (pos[0]-1,pos[1])
			
			elif direct == "right":

				self.body[i] = (pos[0],pos[1]+1)		
			else:

				self.body[i] = (pos[0]+1, pos[1])


	def extend_snake(self):


		snake_tail = self.body[-1]

		tail_dir = self.directions[-1]

		if tail_dir == "left":

			self.body.append((snake_tail[0], snake_tail[1]+1))
		elif tail_dir == "up":

			self.body.append((snake_tail[0]+1, snake_tail[1]))
		elif tail_dir == "right":

			self.body.append((snake_tail[0], snake_tail[1]-1))
		else:

			self.body.append((snake_tail[0]-1, snake_tail[1]))
