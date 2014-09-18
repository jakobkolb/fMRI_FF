import numpy as np
import sys
import trial_parameters as tp
import os

filename = sys.argv[1]

output_folder = 'output_2/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#list of regressors:
regressors = \
[   'stim_1_visual', 'stim_1_arithmetic', 'stim_1_auditory',
    'stim_2_visual', 'stim_2_arithmetic', 'stim_2_auditory',
    'delay_1_visual','delay_1_arithmetic','delay_1_auditory',
    'delay_2_visual_EVgap=small','delay_2_arithmetic_EVgap=small','delay_2_auditory_EVgap=small',
    'delay_2_visual_EVgap=large','delay_2_arithmetic_EVgap=large','delay_2_auditory_EVgap=large',
    'options_visual_EVgap=small','options_arithmetic_EVgap=small','options_auditory_EVgap=small',
    'options_visual_EVgap=large','options_arithmetic_EVgap=large','options_auditory_EVgap=large',
    'response_visual_EVgap=small','response_arithmetic_EVgap=small','response_auditory_EVgap=small',
    'response_visual_EVgap=large','response_arithmetic_EVgap=large','response_auditory_EVgap=large']

output_files = []
for regressor in regressors:
    print regressor
    output_files.append(open(output_folder + regressor+'.dat','w'))


with open(filename) as f:
    for line in f.readlines():
        parts = line.split(' ')
        for i, regressor in enumerate(regressors):
            for part in parts:
                if regressor in part:
                    print parts, regressor
                    print>>output_files[i], parts[0], tp.fmri_time, 1

