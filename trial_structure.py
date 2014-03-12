import numpy as np
from psychopy import core, visual, event, logging
from classes import trial

logging.console.setLevel(logging.CRITICAL)


#general parameters for the experiment:
#-----------------------------------------------------------------------------
trial.ts = 2.0                                                  #time for one fmri measurement
number_of_trials = 4                                            #obviously the number of trails to be taken
spacing = [(-0.5,-0.2),(0.5,-0.2),(-0.5,0.6),(0.5,0.6),(0,0)]   #positions for objects on slides
                                                                #marker_1, marker_2, stim_1, stim_2, fixation_cross
#data arrays for trail parameters and user input and reaction time
output = np.zeros((number_of_trials,10))



#the following variables have to be set for each trial separately. More later.
#-----------------------------------------------------------------------------
#time for slides A, B, C, D
timing = [2,2,2,2]

#difficulties for the current trial
difficulties = [0.1, 0.3]

#deviation from standard order of elements on slide A and C
inversions = [0,0,0]
#-----------------------------------------------------------------------------


win = visual.Window()

#runt trials

for i in range(0,number_of_trials):

    current_trial = trial("dot", win, timing, spacing, difficulties, inversions)
    current_trial.run_trail()
#save data from each trial, timing of slides, user input and inversions of stimuli
    output[i,0:4]   = timing
    output[i,4:7]   = current_trial.user_input
    output[i,7:10]  = inversions

win.close()

np.savetxt('experiment_output_data.tsv', output)
