import numpy as np
from psychopy import core, visual, event, logging
from classes import trial
import globvar
logging.console.setLevel(logging.CRITICAL)


#general parameters for the experiment:
#-----------------------------------------------------------------------------
trial.ts = 1.5                                                  #time for one fmri measurement
number_of_trials = 100                                          #obviously the number of trails to be taken
spacing = [(-0.5,-0.2),(0.5,-0.2),(-0.5,0.6),(0.5,0.6),(0,0)]   #positions for objects on slides
                                                                #marker_1, marker_2, stim_1, stim_2, fixation_cross

#data arrays for trail parameters and user input and reaction time
output = np.zeros((number_of_trials,10))



#the following variables have to be set for each trial separately. More later.
#-----------------------------------------------------------------------------
#time for slides A, B, C, D
timing = np.zeros((number_of_trials,4))
timing[:,0:4] = [3,2,1,2]
for i in range(number_of_trials):
    timing[i,1] = np.random.randint(1,5)
    timing[i,3] = np.random.randint(2,5)

print sum(timing[:,1])/number_of_trials

#difficulties for the current trial
difficulties =  np.zeros((number_of_trials,2))
difficulties[:,0:2] = [0.1, 0.3]

#deviation from standard order of elements on slide A and C
inversions = np.zeros((number_of_trials,3))
inversions[:,0:3] = [0,0,0]
for i in range(number_of_trials):
    inversions[i,0] = np.random.randint(0,1)
    inversions[i,1] = np.random.randint(0,1)
    inversions[i,2] = np.random.randint(0,1)

#-----------------------------------------------------------------------------


win = visual.Window()

#run trials

for i in range(0,number_of_trials):

    current_trial = trial("dot", win, timing[i,:], spacing, difficulties[i,:], inversions[i,:])
    current_trial.run_trail()
#save data from each trial, timing of slides, user input and inversions of stimuli
    output[i,0:4]   = timing[i,:]
    output[i,4:7]   = current_trial.user_input
    output[i,7:10]  = inversions[i,:]

win.close()

np.savetxt('experiment_output_data.tsv', output)
