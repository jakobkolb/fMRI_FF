
#import dependencies
#-----------------------------------------------------------------------------
import numpy as np
from psychopy import core, visual, event, logging
from trial_classes import trial, init
import random
import trial_parameters as globvar
import pylink
logging.console.setLevel(logging.CRITICAL)
#-----------------------------------------------------------------------------

#initialize the eyetracker
#-----------------------------------------------------------------------------
print 'initialize eyetracker'
if globvar.tracker_connected == True:
    eye_tracker = pylink.EyeLink(globvar.tracker_ip)
elif globvar.tracker_connected == False:
    eye_tracker = pylink.EyeLink(None)
#-----------------------------------------------------------------------------



#initialize the class for generation of trial parameters
#-----------------------------------------------------------------------------
print 'trial setup'
init_parameters = init('choice')
#-----------------------------------------------------------------------------


#preparation of trials: prepare output to file
#-----------------------------------------------------------------------------
win = visual.Window()
#write a short readme to the output file
output_user_interaction = open('choice_study_user_input.txt','w')
print>>output_user_interaction, '#output format is the following'
print>>output_user_interaction, '#trial_type, user_active?, user_input_key, accepted difficulty, accepted reward, accepted dif*reward, rejected difficulty, rejected reward, rejected dif*reward, inversions'
print>>output_user_interaction, '#difficulty refers to the exptected participant performance as set in trial_parameters'
print>>output_user_interaction, '#the three columns of inversions refer to the inversion of the default arrangement of the displayed elements. 1 means default arrangement, -1 means inverse of default arrangement.'
print>>output_user_interaction, '#1) the task markers where by default marker_1 is left and marker_2 is right 2) to the task difficulty where by default easy is left and hard is right and 3) to the response markers where again by default marker_1 is left and marker_2 is right'

output_trial_timing = open('choice_study_trial_timing.txt','w')
print>>output_trial_timing, '#this file contains the data for timing of each trial'
print>>output_trial_timing, '#output format is the following'
print>>output_trial_timing, '#trial_type, time_slide_A, time_slide_B, time_slide_C, time_slide_D, time_trial_end, user_reaction_time'
#-----------------------------------------------------------------------------

#preparation of trials: short introduction and explanation slide
#-----------------------------------------------------------------------------
message1 = visual.TextStim(win=win, text='the first slide presents two differently difficult \n options and the reward that can be gained by choosing one of them. \n the third slide lets you choose one of the options \n according to the marker signs using the left and right arrow keys. \n The experiment can be paused by pressing p or be ended by pressing escape on this slide.')
message1.draw()
win.flip()
core.wait(3)
#-----------------------------------------------------------------------------

#iterate over the different trial modi and generate trial parameters accordingly
#-----------------------------------------------------------------------------
for kind in globvar.trial_modi:
    #write a short note to the output file, if a new trial modus starts
    print>>output_user_interaction, `globvar.number_of_trials`+ ' ' + kind + ' trials'
    print>>output_trial_timing, `globvar.number_of_trials`+ ' ' + kind + ' trials'
    #generate trial parameters for the upcomming trials
    timing, difficulties, inversions = init_parameters.rand_trial_parameters(kind)
#-----------------------------------------------------------------------------

#run the actual trials and record user input
#-----------------------------------------------------------------------------
    for i in range(0,globvar.number_of_trials):

        current_trial = trial(kind, win, timing[i,:], globvar.spacing, difficulties[i,:], inversions[i,:])
        current_trial.run_trial()
        #data from trial.getData() is kind, user_active[y,n], input_key, difficulty_chosen, reward_chosen, dif*rew, 
        #                                                                difficulty_rejected, reward_rejected, dif*rew
        print 'stimuli type is ', current_trial.name
        print 'user difficulty choice is ', current_trial.user_input[2]
        print 'user reaction time is ', current_trial.tR
        #save data from each trial, timing of slides, user input and inversions of stimuli
        print>>output_user_interaction, str(current_trial.premature_input).strip('[]')
        print>>output_user_interaction, str(current_trial.getData()).strip('()'), str(inversions[i,:]).strip('[]')
        print>>output_trial_timing, str(current_trial.getTiming()).strip('()')
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


