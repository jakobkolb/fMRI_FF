import numpy as np
from psychopy import core, visual, event, logging
from trial_classes import trial, init
import random
import trial_parameters as globvar
logging.console.setLevel(logging.CRITICAL)


#general parameters for the experiment:
#-----------------------------------------------------------------------------
trial.ts = 1.5                                                  #time for one fmri measurement
number_of_trials = 30                                           #the number of trails per modus to be taken
max_rep = 4                                                     #maximum number of repetitions in randomization
dif_hard = 0.1                                                  #difficulty for hard trials
dif_easy = 1                                                    #difficulty for easy trials
mean_delay_average = 2                                          #desired delay average in fmri time units
mean_baseline_average = 3
spacing = [ (-0.5,-0.1),(0.5,-0.1),                             #positions for objects on slides
            (-0.5,0.5),(0.5,0.5),                               #stim_1, stim_2, marker_1, marker_2, 
            (-0.5,-0.7),(0.5,-0.7),                              #reward_1, reward_2, fixation_cross
            (0,0)]        

#the following block sets up the timing and positioning of the trial features
#-----------------------------------------------------------------------------
print 'trial setup'

init_parameters = init('choice', number_of_trials, max_rep, dif_easy, dif_hard, mean_delay_average, mean_baseline_average)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#run the actual trials and record user input
#-----------------------------------------------------------------------------
win = visual.Window()
#write a short readme to the output file
output_file = open('choice_study_results.txt','w')
print>>output_file, '#output format is the following'
print>>output_file, '#trial_type, user_input?, user_input, rt, user_choice, according_reward, time_slide_A, time_slide_B, time_slide_C, time_slide_D, time_trial_end'

#short introduction and explanation:
message1 = visual.TextStim(win=win, text='the first slide presents two differently difficult \n options and the reward that can be gained by choosing one of them. \n the third slide lets you choose one of the options \n according to the marker signs using the left and right arrow keys. \n The experiment can be paused by pressing p or be ended by pressing escape on this slide.')
message1.draw()
win.flip()
core.wait(1)
#iterate over the different trial modi
for kind in ['math','dot','audio']:
    #write a short note to the output file, if a new trial modus starts
    print>>output_file, `number_of_trials`+ ' ' + kind + ' trials'
    #generate trial parameters for the upcomming trials
    timing, difficulties, inversions = init_parameters.rand_trial_parameters(kind)
    for i in range(0,number_of_trials):

        current_trial = trial(kind, win, timing[i,:], spacing, difficulties[i,:], inversions[i,:])
        current_trial.run_trial()
        #data from trial.getData() is kind, user_active[y,n], input_key, reaction_time, difficulty_chosen, t_slide_a, t_slide_b, t_slide_c, t_slide_d, t_end
        print 'stimuli type is ', current_trial.name
        print 'user difficulty choice is ', current_trial.user_input[3]
        print 'user reaction time is ', current_trial.user_input[2]
        #save data from each trial, timing of slides, user input and inversions of stimuli
        print>>output_file, current_trial.getData() 
        del current_trial

win.close()
output_file.close()
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#present actual tasks to participant
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#evaluate user input and save relevant data
#-----------------------------------------------------------------------------


