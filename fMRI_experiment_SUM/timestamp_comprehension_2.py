import numpy as np
import sys
import trial_parameters as tp
import os

filename = sys.argv[1]

output_folder = 'output_v2/'
output_prefix = filename[11:-14]

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#list of regressors:
single_regressors = \
[   'message'
    'stim1visual', 'stim1arithmetic', 'stim1auditory',
    'stim2visual', 'stim2arithmetic', 'stim2auditory',
    'optionsvisualEVgapsmall','optionsarithmeticEVgapsmall','optionsauditoryEVgapsmall',
    'optionsvisualEVgaplarge','optionsarithmeticEVgaplarge','optionsauditoryEVgaplarge']

delays = ['delay1_visual','delay1arithmetic','delay1auditory',
    'delay2visualEVgapsmall','delay2arithmeticEVgapsmall','delay2auditoryEVgapsmall',
    'delay2visualEVgaplarge','delay2arithmeticEVgaplarge','delay2auditoryEVgaplarge']

response_largeEV = ['responsevisualEVgapsmall','responsearithmeticEVgapsmall','responseauditoryEVgapsmall']
response_smallEV = ['responsevisualEVgaplarge','responsearithmeticEVgaplarge','responseauditoryEVgaplarge']

list_regressors = [delays, response_largeEV, response_smallEV]

output_files = []
for regressor in single_regressors:
    print regressor
    output_files.append(open(output_folder + output_prefix + regressor+'.bfsl','w'))
output_files.append(open(output_folder + output_prefix + 'delay' + '.bfsl', 'w'))
output_files.append(open(output_folder + output_prefix + 'response_largeEV' + '.bfsl', 'w'))
output_files.append(open(output_folder + output_prefix + 'response_smallEV' + '.bfsl', 'w'))

corrupted_output_files = []
for regressor in single_regressors:
    print regressor
    corrupted_output_files.append(open(output_folder + 'ERROR_' + output_prefix + regressor+'.bfsl','w'))
corrupted_output_files.append(open(output_folder + 'ERROR_' + output_prefix + 'delay' + '.bfsl', 'w'))
corrupted_output_files.append(open(output_folder + 'ERROR_' + output_prefix + 'response_largeEV' + '.bfsl', 'w'))
corrupted_output_files.append(open(output_folder + 'ERROR_' + output_prefix + 'response_smallEV' + '.bfsl', 'w'))

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
            for i, regressor in enumerate(single_regressors):
                for part in parts:
                    if regressor in part:
                        print>>output_files[i], '\t'.join(map(str,[parts[0], tp.fmri_time, 1]))
                        print i, regressor
            for j, reglist in enumerate(list_regressors):
                k = i+j+1
                for regressor in reglist:
                    if regressor in part:
                        print>>output_files[k], '\t'.join(map(str,[parts[0], tp.fmri_time, 1]))
                        print k, regressor

        elif corrupted:
            for i, regressor in enumerate(single_regressors):
                for part in parts:
                    if regressor in part:
                        print>>corrupted_output_files[i], '\t'.join(map(str,[parts[0], tp.fmri_time, 1]))
                        print i, regressor
            for j, reglist in enumerate(list_regressors):
                k = i+j+1
                for regressor in reglist:
                    if regressor in part:
                        print>>corrupted_output_files[k], '\t'.join(map(str,[parts[0], tp.fmri_time, 1]))
                        print k, regressor
