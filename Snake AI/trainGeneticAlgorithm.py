import pygame
from helpfile.snakeGameGATrain import SnakeGameGATrain
from helpfile import geneticAlgorithm as ga 


def main():
	game_fps = 3000
	chroms_per_gen = 200
	num_inputs = 9
	num_hidden_layer_nodes = 10
	bits_per_weight = 6
	num_outputs =4
	total_bits = ((num_inputs+1)*num_hidden_layer_nodes + num_hidden_layer_nodes*(num_hidden_layer_nodes+1) + num_outputs*(num_hidden_layer_nodes + 1))*bits_per_weight
	population = ga.genPopulation(chroms_per_gen, total_bits)
	game = SnakeGameGATrain(game_fps, population, chroms_per_gen, bits_per_weight, num_inputs, num_hidden_layer_nodes, num_outputs)
	
	pygame.font.init()

	while game.play:

		game.clock.tick(game.fps)
		
		game.move_snake()
		game.check_collisions()
		game.update_frames_since_last_fruit()
		game.frames_alive += 1

		if game.restart == True:
			game.restart = False
			continue
		
		game.redraw_window()
		
		game.event_handler()
		
main()