
#import dependencies
#-----------------------------------------------------------------------------
import numpy as np
from psychopy import core, visual, event, logging
from trial_classes import trial, init
import random
import trial_parameters as globvar
import pylink
import pygame

window_size = (800,600)

#initialize the eyetracker
#-----------------------------------------------------------------------------
print 'initialize eyetracker'

#connect to tracker, if needed
if globvar.tracker_connected == True:
    eye_tracker = pylink.EyeLink(globvar.tracker_ip)
elif globvar.tracker_connected == False:
    eye_tracker = pylink.EyeLink(None)

#open output file
pylink.getEYELINK().openDataFile('test_output')

win = visual.Window(size = window_size)

#send screen size to tracker
pylink.getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" %(window_size[0], window_size[1]))
pylink.getEYELINK().sendMessage("screen_pixel_coords =  0 0 %d %d" %(window_size[0], window_size[1]))

#get tracker version and tracker software version
tracker_software_ver = 0
eyelink_ver = pylink.getEYELINK().getTrackerVersion()
if eyelink_ver == 3:
	tvstr = pylink.getEYELINK().getTrackerVersionString()
	vindex = tvstr.find("EYELINK CL")
	tracker_software_ver = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))
print 'tracker version', eyelink_ver
print 'tracker software v', tracker_software_ver

# set EDF file contents 
pylink.getEYELINK().sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
if tracker_software_ver>=4:
	pylink.getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET")
else:
	pylink.getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")

pylink.setCalibrationColors( (0, 0, 0),(255, 255, 255));  				#Sets the calibration target and background color
pylink.setTargetSize(int(window_size[0]/40), int(window_size[0]/30));	#select best size for calibration target
#-----------------------------------------------------------------------------

pylink.beginRealTimeMode(0)
print 'started real time mode'
pylink.getEYELINK().startRecording(1, 1, 0, 0)

core.wait(3)

pylink.endRealTimeMode()
pylink.getEYELINK().setOfflineMode()

win.close()

if pylink.getEYELINK() != None:
   # File transfer and cleanup!
    pylink.getEYELINK().setOfflineMode();                          
    pylink.msecDelay(500);                 

    #Close the file and transfer it to Display PC
    pylink.getEYELINK().closeDataFile()
    pylink.getEYELINK().receiveDataFile(globvar.edf_filename, globvar.edf_filename)
    pylink.getEYELINK().close();
