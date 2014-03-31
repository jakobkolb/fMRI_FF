#this file offers some general setting options

#-----------------------------------------------------------------------------
#general settings for timing, order of trial modi and object positions
#-----------------------------------------------------------------------------
#time for one fmri measurement
fmri_time = 1.5                                                 
#modi of trials to be taken
trial_modi = ['audio','math','dot']                             
#the number of trails per modus to be taken
number_of_trials = 5                                            
#maximum number of repetitions in randomization
max_rep = 4                                                     
#desired delay average in fmri time units
mean_delay_average = 2
#desired baseline average in fmir time units
mean_baseline_average = 3
#position of the opbjects on slides
            #stim_1, stim_2
spacing = [ (-0.5,-0.1),(0.5,-0.1),                             
            #marker_1, marker_2
            (-0.5,0.5),(0.5,0.5),                               
            #reward_1, reward_2
            (-0.5,-0.7),(0.5,-0.7),                             
            #fixation_cross
            (0,0)]
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#settings for difficulties of tasks and monetary reward
#-----------------------------------------------------------------------------
#values for reward for easy and hard tasks in the form [min_reward,max_reward] in Euro
reward_hard = [0.5,1]          
reward_easy = [0,0.5]
#difficulty settings for different trial modi in the form [easy, hard]
#for math trial:size of interval for correct answer
math_trial_interval         = [10,3]
#for rdm trial:coherence of the dot motion values between 0 and 1
dot_motion_trial_coherence  = [0.8,0.2]
#for the audio trial: signal to noise ratio. 0.2 means 20% noise, 80% signal(i.e. ba da ru lu)
audio_trial_stn_ratio       = [0.2,0.4]
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#some other settings..
#-----------------------------------------------------------------------------
#paths for marker files. relative paths must be given, if files are not in the same folder
file_marker_1  = 'star.jpg'
file_marker_2  = 'square.jpg'
#possible directions for random dot moovement with angle and according arrow key
possible_rdm_directions = [[0,'right'],[180,'left']]
#-----------------------------------------------------------------------------


