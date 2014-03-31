#this file is used to share global variable between modules

#this file offers some general setting options

#paths for marker files. relative paths must be given, if files are not in the same folder
file_marker_1  = 'star.jpg'
file_marker_2  = 'square.jpg'
#values for reward for easy and hard tasks in the form [min_reward,max_reward] in Euro
reward_hard = [0.5,1]          
reward_easy = [0,0.5]
#possible directions for random dot moovement with angle and according arrow key
possible_rdm_directions = [[0,'right'],[180,'left']]

