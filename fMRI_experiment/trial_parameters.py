#this file offers some general setting options

#-----------------------------------------------------------------------------
#general settings for order of trial modi and object positions
#-----------------------------------------------------------------------------
#Participant ID (with default value)
participant_id = 55
#time for one fmri measurement
fmri_time = 1.5                                     
#Number settings for block structure given as [number of blocks, trials per block]
blocks = [3,16]
#modi of trials to be taken, out of math, dot, audio
trial_modi = ['dot', 'math', 'audio']
#spacing of the objects on slides
size = 0.18
            #stim_1, stim_2
spacing = [ (0,0),(0,0),                             
            #marker_1, marker_2
            (-size,size),(size,size),                               
            #reward_1, reward_2
            (-size,-size),(size,-size),                             
            #fixation_cross
            (0,0)]
#paths for marker files. relative paths must be given, if files are not in the same folder
file_marker_1  = 'star.png'
file_marker_2  = 'square.png'
#path for speaker icon file
speaker_symbol = 'speaker_symbol.png'
#possible directions for random dot moovement with angle and according arrow key
possible_rdm_directions = [[0,'right'],[180,'left']]
#window size in pixels (width, hight)
window_size = (800,600)
#start in Full Screen ?
full_screen = False


#-----------------------------------------------------------------------------
#Some global variables
#-----------------------------------------------------------------------------

#dictionary for all parameters of one run
run_parameters = {}
run_number = 1
run_timer = []
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#Timing settings
#-----------------------------------------------------------------------------
#timing for each part of one trial in units of fmri_time
#timing for the presention of the different tasks can be set independently
time_math_stim_1 = 1.8
time_math_stim_2 = 1.8
time_dot_stim_1 = 0.8
time_dot_stim_2 = 0.8
time_audio_stim_1 = 0.8
time_audio_stim_2 = 0.8
time_break_1 = 0.2
time_break_2 = 0.2
mean_delay_1_trs = 2
time_options = 1.0
mean_delay_2_trs = 2
time_response = 1.
mean_baseline_trs = 2
#parameter to fix shape of geometric distribution
geometric_parameter = 'mean'
#number of ts neccesary to consider a delay to be "long"
long_trial_ts = 6
#maximum time for one delay period i ts
max_delay_ts = 8
#number of long trials neccessary
long_trial_number = 1
#maximum number of repetitions in randomization i.e max same trial types, equal delay times etc in a row
max_rep = 4
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#settings for difficulties of tasks and monetary reward
#-----------------------------------------------------------------------------
#values for Expected Value of user decision for small and large EV gap in the form [min_EV,max_EV]
#settigs for small and large EV gap are marked with _s and _l respectively
EV_high_s = [0.6,0.8]          
EV_low_s = [0.4,0.6]
EV_high_l = [0.8,1]          
EV_low_l = [0.2,0.4]
#anticipated participant performance aka difficulty
anticipated_participant_performance=[0.9,0.65]
#difficulty settings for different trial modi in the form [easy, hard] 
#for math trial:size of interval for correct answer
math_trial_interval       = [10,3]
#for rdm trial:coherence of the dot motion values between 0 and 1
dot_motion_trial_coherence  = [0.9,0.5]
#for the audio trial: signal to noise ratio. 0.2 means 20% noise, 80% signal(i.e. ba da ru lu)
audio_trial_stn_ratio       = [0.35,0.6]
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#settings concerning eye tracking
#-----------------------------------------------------------------------------
tracker_connected = False
tracker_ip = "100.1.1.1"
edf_filename = "trial_eyetracker_output.edf"

#-----------------------------------------------------------------------------


