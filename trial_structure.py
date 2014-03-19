import numpy as np
from psychopy import core, visual, event, logging
from trial_classes import trial
import random
import globvar
logging.console.setLevel(logging.CRITICAL)


#general parameters for the experiment:
#-----------------------------------------------------------------------------
trial.ts = 1.5                                                  #time for one fmri measurement
number_of_trials = 100                                          #obviously the number of trails to be taken
spacing = [(-0.5,-0.2),(0.5,-0.2),(-0.5,0.6),(0.5,0.6),(0,0)]   #positions for objects on slides
                                                                #marker_1, marker_2, stim_1, stim_2, fixation_cross
desired_delay_average = 2
desired_baseline_average = 3
#data arrays for trail parameters and user input and reaction time
output = np.zeros((number_of_trials,10))



#the following block sets up the timing and positioning of the trial features
#-----------------------------------------------------------------------------
print 'trial setup'


#time for slides A, B, C, D
timing = np.zeros((number_of_trials,4))
timing[:,0:4] = [3,2,1,2]
for i in range(number_of_trials):
    timing[i,0] = np.random.randint(1,5)
    timing[i,2] = np.random.randint(2,5)
#adjust means of timing for delay and baseline slides such 
Estimated_delay_time  = sum(timing[:,0])/number_of_trials
M   = int(number_of_trials*(Estimated_delay_time - desired_delay_average))
n=1
print Estimated_delay_time, M
while n<M:
    #pick random time in the trial sequence
    i = np.random.randint(number_of_trials-1)
    #only change the value, if it is not equal to the time before and after
    if timing[i,0]-1!=timing[i+1,0] and timing[i,0]-1!=timing[i+1,0] and timing[i,0]-1>0:
        timing[i,0]-=1
        n+=1

Estimated_baseline_time  = sum(timing[:,2])/number_of_trials
M   = int(number_of_trials*(Estimated_baseline_time - desired_baseline_average))
n=1
while n<M:
    i = np.random.randint(number_of_trials-1)
    if timing[i,2]-1!=timing[i+1,2] and timing[i,2]-1!=timing[i+1,2] and timing[i,2]-2>0:
        timing[i,2]-=1
        n+=1

#difficulties for the current trial in the form [easy, hard] 
difficulties =  np.zeros((number_of_trials,2))
difficulties[:,0:2] = [1, 0.1]

#deviation from standard order of elements on slide A and C
inversions = np.zeros((number_of_trials,3))
inversions[:,0:3] = [0,0,0]
for i in range(number_of_trials):
    inversions[i,0] = random.choice([-1,1])
    inversions[i,1] = random.choice([-1,1])
    inversions[i,2] = random.choice([-1,1])

print 'mean delay time is ', sum(timing[:,0])/number_of_trials
print 'mean baseline time is ', sum(timing[:,2])/number_of_trials

#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#run the actual trials and record user input
#-----------------------------------------------------------------------------
win = visual.Window()

output_file = open('choice_study_results.txt','w')

for i in range(0,number_of_trials):

    current_trial = trial("dot", win, timing[i,:], spacing, difficulties[i,:], inversions[i,:])
    current_trial.run_trial()
#data from trial.getData() is kind, user_active[y,n], input_key, reaction_time, difficulty_chosen, t_slide_a, t_slide_b, t_slide_c, t_slide_d
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
#evaluate user input and save relevant data
#-----------------------------------------------------------------------------
