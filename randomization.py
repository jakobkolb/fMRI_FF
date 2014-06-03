import numpy as np
import trial_parameters as tp
import random
import pickle

blocks = []
j = random.randint(1,np.shape(tp.trial_modi)[0])
for i in range(tp.blocks[0]):
    blocks.append(tp.trial_modi[(i+j)%np.shape(tp.trial_modi)[0]])
random.shuffle(blocks) 

number_of_trials = tp.blocks[0]*tp.blocks[1]

if tp.geometric_parameter == 'mean':
    delay_1_prob = 1./tp.mean_delay_1_trs
    delay_2_prob = 1./tp.mean_delay_2_trs
    baseline_prob = 1./tp.mean_baseline_trs
if tp.geometric_parameter == 'meadian':
    print 'median probabilities not yet implemented'


timing = np.zeros((number_of_trials,9))
EV_gap = []
difficulties = np.zeros((number_of_trials,2))
inversions = np.zeros((number_of_trials,4))

#set timing for stimuli presentation dependent on kind 
for i in range(tp.blocks[0]):
    kind = blocks[i]
    i1 = i*tp.blocks[1]
    i2 = (i+1)*tp.blocks[1]
    no_long_trials = True
    while no_long_trials == True :
        if kind == 'math':
            timing[i1:i2,0] = tp.time_math_stim_1
            timing[i1:i2,1] = tp.time_break_1
            timing[i1:i2,2] = tp.time_math_stim_2
            timing[i1:i2,3] = tp.time_break_2
        if kind == 'dot':
            timing[i1:i2:,0] = tp.time_dot_stim_1
            timing[i1:i2:,1] = tp.time_break_1
            timing[i1:i2:,2] = tp.time_dot_stim_2
            timing[i1:i2:,3] = tp.time_break_2
        if kind == 'audio':
            timing[i1:i2,0] = tp.time_audio_stim_1
            timing[i1:i2,1] = tp.time_break_1
            timing[i1:i2,2] = tp.time_audio_stim_2
            timing[i1:i2,3] = tp.time_break_2

        timing[i1:i2,4] = np.random.geometric(delay_1_prob,tp.blocks[1])

        timing[i1:i2,5] = tp.time_options

        timing[i1:i2,6] = np.random.geometric(delay_2_prob,tp.blocks[1])

        timing[i1:i2,7] = tp.time_response

        timing[i1:i2,8] = np.random.geometric(baseline_prob,tp.blocks[1])
        
        c1,c2,c3 = False,False,False
        if (timing[i1:i2,4]>tp.long_trial_ts).sum()>=tp.long_trial_number:
            c1 = True
        if (timing[i1:i2,6]>tp.long_trial_ts).sum()>=tp.long_trial_number:
            c2 = True
        if (timing[i1:i2,8]>tp.long_trial_ts).sum()>=tp.long_trial_number:
            c3 = True
        if c1 == True and c2 == True and c3 == True:
            no_long_trials = False

    too_many_repetitions = True

    while too_many_repetitions == True:

        #difficulties for the current trial in the form [easy, hard], units for difficulty of different trials have to be
        #set according to participants performance.
        for i in range(tp.blocks[1]):
            EV_gap.append(random.choice(['small', 'large']))

        if kind == 'math':
            difficulties[i1:i2,0:2] = tp.math_trial_interval
        elif kind == 'dot':
            difficulties[i1:i2,0:2] = tp.dot_motion_trial_coherence
        elif kind == 'audio':
            difficulties[i1:i2,0:2] = tp.audio_trial_stn_ratio

        #deviation from standard order of elements on slide A and C
        inversions[i1:i2,0:4] = [0,0,0,0]
        for i in range(i1,i2):
            inversions[i,0] = random.choice([-1,1])
            inversions[i,1] = random.choice([-1,1])
            inversions[i,2] = random.choice([-1,1])
            inversions[i,3] = random.choice([-1,1])

        #check if the maximum number of repetitions satisfies max_rep
        too_many_repetitions = False
        for i in range(i1,i2 - tp.max_rep):
            same_1 = True
            same_2 = True
            same_3 = True
            same_4 = True
            for j in range(i,i+tp.max_rep):
                if inversions[j,0] != inversions[i,0]:
                    same_1 = False
                    k = i
                if inversions[j,1] != inversions[i,1]:
                    same_2 = False
                    k = i
                if inversions[j,2] != inversions[i,2]:
                    same_3 = False
                    k = i
                if inversions[j,3] != inversions[i,3]:
                    same_4 = False
                    k = i
            if same_1 == True or same_2 == True or same_3 == True or same_4 == True:
                    too_many_repetitions = True
                    break


print 'mean delay 1 time is ', sum(timing[:,4])/number_of_trials, 'ts'
print 'mean delay 2 time is ', sum(timing[:,6])/number_of_trials, 'ts'
print 'mean baseline time is ', sum(timing[:,8])/number_of_trials, 'ts'

print 'average times that difficult task is first is', (inversions[:,0]==1).sum()/float(number_of_trials)
print 'averate times that high reward is left is', (inversions[:,1]==1).sum()/float(number_of_trials)
print 'averate times that marker_1 is left on options slide is', (inversions[:,2]==1).sum()/float(number_of_trials)
print 'average times that marker_1 is left on decision slide is', (inversions[:,3]==1).sum()/float(number_of_trials)

trial_parameters = {}
trial_parameters['blocks'] = blocks
trial_parameters['timing'] = timing
trial_parameters['inversions'] = inversions
trial_parameters['difficulties'] = difficulties
trial_parameters['EV_gap'] = EV_gap

with open('run_parameters.p', 'wb') as fb:
            pickle.dump(trial_parameters, fb)


