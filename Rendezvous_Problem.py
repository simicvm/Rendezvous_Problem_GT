'Rendezvous Problem Through The Game Theoretic Lens'

import random
import math
import matplotlib.pyplot as plt


def global_function():
	"""Calculates the global utility function (potential function)"""
	temp_glob = 0.0
	for player in players:
		temp_glob += player.utility_function()
	global_util = temp_glob/2
	return global_util

def generte_map(grid_size):
	"""
	Function creates a grid of size grid_size x grid_size. Default size is 11x11.
	0 denotes free space, 1 denotes obstacle. They have to be added manualy.
	"""
	world_grid = {}
	for i in range(grid_size+1):
		for j in range (grid_size+1):
			world_grid[(i,j)] = 0
	
	"Adding obstacle in a lousy way!"
	for i in range(3,9):
		world_grid[(6,i)] = 1
	
	world_grid[(4,3)] = 1
	world_grid[(5,3)] = 1
	world_grid[(6,3)] = 1
	world_grid[(4,8)] = 1
	world_grid[(5,8)] = 1
	world_grid[(6,8)] = 1
	return world_grid
	

class Player(object):
	"""Defines Player class used to create Player objects"""
	
	def __init__(self, x, y):
		"""Initialize the player position"""
		self.x_position = x
		self.y_position = y
		self.neighbors = []

	def add_neighbors(self, nbors):
		"""
		Adds neighboring players. 
		nbors has to be in a list format
		"""
		for i in nbors:
			self.neighbors.append(i)
		return self.neighbors

	def update_position(self, x_new, y_new):
		"""Updates player's position"""
		self.x_position = x_new
		self.y_position = y_new

	def current_position(self):
		"""Returns player position""" 
		return self.x_position, self.y_position

	def r_action_set(self):
		"""Determines the restricted area set based on current position and obstacles"""
		curr_pos = self.current_position()
		self.r_a_set = []
		x, y = curr_pos
		for i in [x-1, x, x+1]: 
			if i >= 0 and i <= 10:
				for j in [y-1, y, y+1]:
					if j >= 0 and j <= 10 and world_grid[(i,j)] == 0:
						self.r_a_set.append((i,j))
		return self.r_a_set

	def utility_function(self): 
		"""
		Calculates player's utility
		Neighbors is a set of player's neighbors
		"""
		temp_neighbor = 0.0
		util_temp = 0.0
		self.util_func = 0.0
		for neighbor in self.neighbors:
			for i in range(2):
				temp = (self.current_position()[i] - 
						neighbor.current_position()[i])**2.0
				temp_neighbor += temp
			util_temp += temp_neighbor**0.5	
			temp_neighbor = 0.0
		self.util_func = - util_temp
		return self.util_func

	def trial_utility(self, t_act):
		"""
		Calculates player's utility based on trial action
		Neighbors is a set of player's neighbors
		t_act is a trial action choosen for that step
		"""
		temp_neighbor = 0.0
		util_temp = 0.0
		self.trial_util = 0.0
		for neighbor in self.neighbors:
			for i in range(2):
				temp = (t_act[i] - 
						neighbor.current_position()[i])**2.0
				temp_neighbor += temp
			util_temp += temp_neighbor**0.5	
			temp_neighbor = 0.0
		self.trial_util = - util_temp
		return self.trial_util

"Define and create world with appropriate size "
world_grid = generte_map(10)

"Create players and defines their positions"
player1 = Player(1,5)
player2 = Player(5,1)
player3 = Player(9,5)
player4 = Player(5,9)

"Add neighbor connectios"
player1.add_neighbors([player2, player3])
player2.add_neighbors([player1, player4])
player3.add_neighbors([player1])
player4.add_neighbors([player2])

"Makes player set"
players = [player1, player2, player3, player4]

"Containers for graph points"
player1_xaxis = []
player1_yaxis = []
player2_xaxis = []
player2_yaxis = []
player3_xaxis = []
player3_yaxis = []
player4_xaxis = []
player4_yaxis = []

"""Start the iterations"""
for step in range(1,2000):
		
	beta = step/100 

	"Choose random player for a step t"
	moving_player = random.choice(players)

	"Choosen player take random trial action"
	trial_action = random.choice(moving_player.r_action_set())

	"Calculate trial action probabilities"
	trial_prob_act =  math.exp(beta*moving_player.trial_utility(trial_action))/ \
						(math.exp(beta*moving_player.trial_utility(trial_action))+
							math.exp(beta*moving_player.utility_function()))
	trial_prob_stay = 1 - trial_prob_act
	weight_choice = random.random()
	#print 'Old position', moving_player.current_position()
	if weight_choice < trial_prob_act:
		#print trial_action
		moving_player.update_position(trial_action[0],trial_action[1])
		#print 'New position', moving_player.current_position()
	else:
		pass
		#print 'New position same as old', moving_player.current_position()
	player1_xaxis.append(player1.current_position()[0])
	player1_yaxis.append(player1.current_position()[1]) 
	player2_xaxis.append(player2.current_position()[0])
	player2_yaxis.append(player2.current_position()[1])
	player3_xaxis.append(player3.current_position()[0])
	player3_yaxis.append(player3.current_position()[1])
	player4_xaxis.append(player4.current_position()[0])
	player4_yaxis.append(player4.current_position()[1])
	
	if global_function() == 0.0:
		print 'Found equilibrium at step: %d! Global utility is: %d' % (step, global_function())
		print 'Player 1 position: ', player1.current_position()
		print 'Player 2 position: ', player2.current_position()
		print 'Player 3 position: ', player3.current_position()
		print 'Player 4 position: ', player4.current_position()
		break
	
			
if global_function() != 0.0:
	print 'No consensus reached in %d' % step
	print 'Player 1 position: ', player1.current_position()
	print 'Player 2 position: ', player2.current_position()
	print 'Player 3 position: ', player3.current_position()
	print 'Player 4 position: ', player4.current_position()


"Plot the graph"

plt.plot(player1_xaxis, player1_yaxis, 'r-', label='Player 1')
plt.plot([1], [5], 'ro', markersize=10) 
plt.plot(player2_xaxis, player2_yaxis, 'g-', label='Player 2')
plt.plot([5], [1], 'go', markersize=10)
plt.plot(player3_xaxis, player3_yaxis, 'b-', label='Player 3')
plt.plot([9], [5], 'bo', markersize=10)
plt.plot(player4_xaxis, player4_yaxis, 'y-', label='Player 4')
plt.plot([5], [9], 'yo', markersize=10)
plt.plot(player1.current_position()[0], player1.current_position()[1], 'ko', markersize=20)
plt.plot([6, 6, 6, 6, 6, 6], [3, 4, 5, 6, 7, 8], 'k-')
plt.plot([4, 5, 6], [3, 3, 3], 'k-')
plt.plot([4, 5, 6], [8, 8, 8], 'k-')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.axis([0, 10, 0, 10])
plt.show()
	




