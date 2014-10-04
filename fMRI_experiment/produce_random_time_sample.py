import numpy as np
import trial_parameters as tp
import random
import pickle
import datetime
import matplotlib.pyplot as mp
import os

output_folder = 'run_parameters/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

number_of_trials = tp.blocks[0]*tp.blocks[1]


#balanced variables:    Modus order, EV_gap
blocks = []
EV_gap = []
#random variables:      inversions(stim order, option marker possition, decision marker possition, higher EV possition),
#                       timing, Actual EV(left, right)
timing = np.zeros((number_of_trials,9))
inversions = np.zeros((number_of_trials,4))
EV_values = np.zeros((number_of_trials,2))


#randomize Modus order
j = random.randint(1,np.shape(tp.trial_modi)[0])
for i in range(tp.blocks[0]):
    blocks.append(tp.trial_modi[(i+j)%np.shape(tp.trial_modi)[0]])
random.shuffle(blocks) 

#balance timings:

if tp.geometric_parameter == 'mean':
    delay_1_prob = 1./tp.mean_delay_1_trs
    delay_2_prob = 1./tp.mean_delay_2_trs
    baseline_prob = 1./tp.mean_baseline_trs
if tp.geometric_parameter == 'meadian':
    print 'median probabilities not yet implemented'


delay_1_times = []
delay_2_times = []
baseline_times = []
for k in range(100):
    total_trial_duration = 0
    print k, 'th of', 100, 'samples working'
    while total_trial_duration != tp.target_trial_duration:
        for i in range(tp.blocks[0]):
            kind = blocks[i]
            i1 = i*tp.blocks[1]
            i2 = (i+1)*tp.blocks[1]
            no_long_trials = True
            too_long_trials = True
            while (no_long_trials or too_long_trials) == True:

                #set fixed timings:
                if kind == 'arithmetic':
                    timing[i1:i2,0] = tp.time_math_stim_1
                    timing[i1:i2,1] = tp.time_break_1
                    timing[i1:i2,2] = tp.time_math_stim_2
                    timing[i1:i2,3] = tp.time_break_2
                if kind == 'visual':
                    timing[i1:i2:,0] = tp.time_dot_stim_1
                    timing[i1:i2:,1] = tp.time_break_1
                    timing[i1:i2:,2] = tp.time_dot_stim_2
                    timing[i1:i2:,3] = tp.time_break_2
                if kind == 'auditory':
                    timing[i1:i2,0] = tp.time_audio_stim_1
                    timing[i1:i2,1] = tp.time_break_1
                    timing[i1:i2,2] = tp.time_audio_stim_2
                    timing[i1:i2,3] = tp.time_break_2

                timing[i1:i2,5] = tp.time_options
                timing[i1:i2,7] = tp.time_response

                for j in range(i1,i2):
                    tmp = tp.max_delay_ts+1
                    while tmp > tp.max_delay_ts:
                        tmp = np.random.geometric(delay_1_prob)
                    timing[j,4] = tmp

                for j in range(i1,i2):
                    tmp = tp.max_delay_ts+1
                    while tmp > tp.max_delay_ts:
                        tmp = np.random.geometric(delay_2_prob)
                    timing[j,6] = tmp

                for j in range(i1,i2):
                    tmp = tp.max_delay_ts+1
                    while tmp > tp.max_delay_ts:
                        tmp = np.random.geometric(baseline_prob)
                    timing[j,8] = tmp

                no_long_trials = True
                c1,c2,c3 = False,False,False
                if (timing[i1:i2,4]>=tp.long_trial_ts).sum()>=tp.long_trial_number:
                    c1 = True
                if (timing[i1:i2,6]>=tp.long_trial_ts).sum()>=tp.long_trial_number:
                    c2 = True
                if (timing[i1:i2,8]>=tp.long_trial_ts).sum()>=tp.long_trial_number:
                    c3 = True
                if c1 == True and c2 == True and c3 == True:
                    no_long_trials = False

                too_long_trials = True
                if ((   timing[i1:i2,4]>tp.max_delay_ts).sum() \
                        + (timing[i1:i2,6]>tp.max_delay_ts).sum() \
                        + (timing[i1:i2,8]>tp.max_delay_ts).sum()) == 0:
                    too_long_trials = False
        total_trial_duration = round(sum(sum(timing[:,:])),0)
        print 'actual time is', total_trial_duration, 'required time is', tp.target_trial_duration
    delay_1_times.append(timing[:,4])
    delay_2_times.append(timing[:,6])
    baseline_times.append(timing[:,8])

head = 'delay_1_times, delay_2_times, baseline_times'
out = np.zeros((np.shape(np.hstack(delay_1_times))[0],3))
out[:,0] = np.hstack(delay_1_times)
out[:,1] = np.hstack(delay_2_times)
out[:,2] = np.hstack(baseline_times)
np.savetxt('sample_of_delay_times.txt', out, delimiter = '\t', header = head)
