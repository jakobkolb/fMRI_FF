#this file offers some general setting options

#-----------------------------------------------------------------------------
#settings for difficulties of tasks and monetary reward
#-----------------------------------------------------------------------------
#values for Expected Value of user decision for the higher EV in the 
#form [min_EV,max_EV] the value of the smaller EV is calculated as a fraction 
#of the larger EV where the difference between EVs is given in percent for 
#small and large EV gap.
EV_high = [18,22]
EV_gap_l = 0.50
EV_gap_s = 0.25
#anticipated participant performance aka difficulty
anticipated_participant_performance=[0.9,0.65]
#the displayed rewards are calculated from difficulty and expected value and 
#rounded to the given number of digits:
digits = 0
#difficulty settings for different trial modi in the form [easy, hard] 
#for math trial:lower boundary of total sum of displayed numbers
#upper boundary is determied by math_trial_interval[i] + sum_dist
math_trial_interval       = [70,30]
#for rdm trial:coherence of the dot motion values between 0 and 1
dot_motion_trial_coherence  = [0.9,0.5]
#for the audio trial: signal to noise ratio. 
#0.2 means 20% noise, 80% signal(i.e. ba da ru lu)
audio_trial_stn_ratio       = [0.35,0.6]
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#special parameters for auditory task
#-----------------------------------------------------------------------------
#maximum amplitude for loudness normalization
max_amp = 16000
#multiplication factor for noice
noise_factor = 2
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#special parameters for Dot Motion task
#-----------------------------------------------------------------------------
#possible directions for random dot moovement with angle and according arrow key
possible_rdm_directions = [[0,'right'],[180,'left']]
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# special parameters for the arithmetic task
#-----------------------------------------------------------------------------
# upper boundary of the sum of displayed numbers is diff + sim_dist 
sum_dist = 10
# determine if difficulty should be manipulated by floats
# according to richards arithmetic scheme
arith_difficulty = 'floats'
# determine if you want floats at all
floats = True
#Some more parameters that richard uses in his arithmetic trial
min_value_rev = 1
max_value_rev = 29
fixed_range = 4
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#Timing settings
#-----------------------------------------------------------------------------
#time for one fmri measurement
fmri_time = 1.5                                     

#timing for each part of one trial in units of fmri_time
#timing for the presention of the different tasks can be set independently
#fixed times
time_anouncement = 2
time_math_stim_1 = 1.8
time_math_stim_2 = 1.8
time_dot_stim_1 = 0.8
time_dot_stim_2 = 0.8
time_audio_stim_1 = 0.8
time_audio_stim_2 = 0.8
time_break_1 = 0.2
time_break_2 = 0.2
time_options = 1.0
time_response = 1.0
#mean times for randomization of delays and baseline
mean_delay_1_trs = 1.8
mean_delay_2_trs = 1.8
mean_baseline_trs = 2
#parameter to fix shape of geometric distribution
geometric_parameter = 'mean'
#number of ts neccesary to consider a delay to be "long"
long_trial_ts = 5
#maximum time for one delay period i ts
max_delay_ts = 6
#number of long trials neccessary
long_trial_number = 2
#maximum number of repetitions in randomization i.e max same trial types, 
#equal delay times etc in a row
max_rep = 4
#absolute trial duration in TRs
target_trial_duration = 520
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#Settings for balancing and randomization
#-----------------------------------------------------------------------------
#number of runs to be created by randomization routine
number_of_runs = 6
#Number settings for block structure given as 
#[number of blocks, trials per block]
blocks = [3,16]
#modi of trials to be taken, out of visual, arithmetic, auditory
trial_modi = ['visual', 'arithmetic', 'auditory']
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#default settings for participant id and run number:
#-----------------------------------------------------------------------------
#Default Participant ID (with default value)
participant_id = 56
#Default run number:
run_number = 1
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#settings for input keys and fmri start signal
#-----------------------------------------------------------------------------
#Participant input keys:
participant_input_keys = ['left', 'right'] #[left, right]
#Human start signal
human_start_signal = 'space'
#start signal from fMRI machine
fMRI_start_signal = 'w'
#Human escape signal
exit_key = 'escape'
#Human pause signal
pause_key = 'p'
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#Paths to file locations
#-----------------------------------------------------------------------------
#paths for marker files. Relative paths must be given, if files are not in the
#same folder
symbol_folder = 'symbols/'
file_marker_1  = symbol_folder + 'star.png'
file_marker_2  = symbol_folder + 'square.png'
#path for speaker icon file
speaker_symbol = symbol_folder + 'speaker_symbol.png'
#foldername of audio files
audio_file_folder = 'audiofiles/de/'
#names of audio files
audio_files = [audio_file_folder+'stim_file_1.wav',audio_file_folder+'stim_file_2.wav']
#name of folder for raw output files:
output_folder = 'raw_output/'
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#settings concerning eye tracking
#-----------------------------------------------------------------------------
tracker_connected = False
tracker_ip = "100.1.1.1"
edf_filename = "trial_eyetracker_output.edf"
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
#Settings for visual elements
#-----------------------------------------------------------------------------
# desired window size in pixels (width, hight)
window_size = (800,600)
# how big should the text be? this is an arbitrary value (but it is chosen for 
#visual.Window.units='norm'
text_height = 0.1   
#start in Full Screen ?
full_screen = False
if full_screen:
    full_window_size = (1680,1050)  # this should be the fullscreen resolution
else:
    full_window_size = window_size
# the following are the 
f_x = float(window_size[0])/float(full_window_size[0])
f_y = float(window_size[1])/float(full_window_size[1])
#spacing of the objects on slides
size = 0.18
            #stim_1, stim_2
spacing = [ (0,0),(0,0),                             
            #marker_1, marker_2
            (-size*f_x,size*f_y),(size*f_x,size*f_y),                               
            #reward_1, reward_2
            (-size*f_x,-size*f_y),(size*f_x,-size*f_y),                             
            #fixation_cross
            (0,0)]
#Sizes of image stims
marker_size = (0.15,0.15)
speaker_size = (0.2,0.2)
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
#Some global variables
#-----------------------------------------------------------------------------
#dictionary for all parameters of one run
run_parameters = {}
experiment_timer = []
sequential_timer = []
#-----------------------------------------------------------------------------


