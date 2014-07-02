import numpy as np
import sys

filename = sys.argv[1]

t0 = 0
t1 = 0

small_ev_math_trials = open('small_ev_math_trials.dat','w')
small_ev_audio_trials = open('small_ev_audio_trials.dat','w')
small_ev_visual_trials = open('small_ev_visual_trials.dat','w')
large_ev_math_trials = open('large_ev_math_trials.dat','w')
large_ev_audio_trials = open('large_ev_audio_trials.dat','w')
large_ev_visual_trials = open('large_ev_visual_trials.dat','w')


with open(filename) as f:
    for line in f.readlines():
        parts = line.split(' ')
        if 'trial' in parts[1]:
            if 'start' in parts[1]:
                mode = parts[-1]
                t0 = float(parts[0])
            if 'end' in parts[1]:
                t1 = float(parts[0])
                if 'small' in mode:
                    if 'math' in parts[1]:
                        print>>small_ev_math_trials, t0, t1-t0, 1
                    if 'audio' in parts[1]:
                        print>>small_ev_audio_trials, t0, t1-t0, 1
                    if 'dot' in parts[1]:
                        print>>small_ev_visual_trials, t0, t1-t0, 1
                if 'large' in mode:
                    if 'math' in parts[1]:
                        print>>large_ev_math_trials, t0, t1-t0, 1
                    if 'audio' in parts[1]:
                        print>>large_ev_audio_trials, t0, t1-t0, 1
                    if 'dot' in parts[1]:
                        print>>large_ev_visual_trials, t0, t1-t0, 1


