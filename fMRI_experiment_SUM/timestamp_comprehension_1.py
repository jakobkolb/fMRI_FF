import numpy as np
import sys
import trial_parameters as tp
import os

filename = sys.argv[1]
output_prefix = filename[11:-14]

output_folder = 'output_v1/'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#list of regressors:
regressors = \
[   'message',
    'stim1visual', 'stim1arithmetic', 'stim1auditory',
    'stim2visual', 'stim2arithmetic', 'stim2auditory',
    'delay1visual','delay1arithmetic','delay1auditory',
    'delay2visualEVgapsmall','delay2arithmetic_EVgapsmall','delay2_auditoryEVgapsmall',
    'delay2visualEVgaplarge','delay2arithmetic_EVgaplarge','delay2_auditoryEVgaplarge',
    'optionsvisualEVgapsmall','optionsarithmeticEVgapsmall','optionsauditoryEVgapsmall',
    'optionsvisualEVgaplarge','optionsarithmeticEVgaplarge','optionsauditoryEVgaplarge',
    'responsevisualEVgapsmall','responsearithmeticEVgapsmall','responseauditoryEVgapsmall',
    'responsevisualEVgaplarge','responsearithmeticEVgaplarge','responseauditoryEVgaplarge']

output_files = []
for regressor in regressors:
    print filename
    print output_prefix
    output_files.append(open(output_folder + output_prefix + regressor+'.bfsl','w'))

corrupted_output_files = []
for regressor in regressors:
    print regressor
    corrupted_output_files.append(open(output_folder + 'ERROR_' + output_prefix + regressor+'.bfsl','w'))

with open(filename) as f:
    corrupted = False
    for line in f.readlines():
        parts = line.split(' ')
        for part in parts:
            if part == 'start_trial':
                corrupted = False
            elif part == 'PREMATURE_INPUT':
                corrupted = True
            elif part == 'NO_USER_INPUT':
                corrupted = True
        if ~corrupted:
            for i, regressor in enumerate(regressors):
                for part in parts:
                    if regressor in part:
                        print>>output_files[i], '\t'.join(map(str,[parts[0], tp.fmri_time, 1]))

        elif corrupted:
            for i, regressor in enumerate(regressors):
                for part in parts:
                    if regressor in part:
                        print>>corrupted_output_files[i], '\t'.join(map(str,[parts[0], tp.fmri_time, 1]))
