import numpy as np
import os
import sys
import matplotlib.pyplot as mp

input_filename = sys.argv[1]

output_folder = 'eyedata_analysis_output'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

gaze_data_x = []
gaze_data_y = []
tracked_timestamps = []

with open(input_filename) as f:
    for line in f.readlines():
        parts = line.split('\t')
        if parts[0][0] == '1':
            if not parts[1][-1] == '.':
                gaze_data_x.append(float(parts[1]))
                gaze_data_y.append(float(parts[2]))
                tracked_timestamps.append(float(parts[0]))

heatmap, xedges, yedges = np.histogram2d(gaze_data_x, gaze_data_y, bins=50)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

mp.clf()
mp.imshow(heatmap, extent=extent)
mp.colorbar()
mp.savefig('gaze_data_heatmap.pdf')

