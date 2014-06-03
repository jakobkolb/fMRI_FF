
#import dependencies
#-----------------------------------------------------------------------------
import numpy as np
from psychopy import core, visual, event, logging
from trial_classes import trial, init
import random
import trial_parameters as globvar
import pylink
logging.console.setLevel(logging.CRITICAL)
#-----------------------------------------------------------------------------

#initialize the eyetracker
#-----------------------------------------------------------------------------
print 'initialize eyetracker'

#connect to tracker, if needed
if globvar.tracker_connected == True:
    eye_tracker = pylink.EyeLink(globvar.tracker_ip)
elif globvar.tracker_connected == False:
    eye_tracker = pylink.EyeLink(None)

#open output file
pylink.getEYELINK().openDataFile(globvar.edf_filename)


#send screen size to tracker
pylink.getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" %(globvar.window_size[0], globvar.window_size[1]))
pylink.getEYELINK().sendMessage("screen_pixel_coords =  0 0 %d %d" %(globvar.window_size[0], globvar.window_size[1]))

#get tracker version and tracker software version
tracker_software_ver = 0
eyelink_ver = pylink.getEYELINK().getTrackerVersion()
if eyelink_ver == 3:
	tvstr = pylink.getEYELINK().getTrackerVersionString()
	vindex = tvstr.find("EYELINK CL")
	tracker_software_ver = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))
print 'tracker version', eyelink_ver
print 'tracker software v', tracker_software_ver

# set tracker output file contents 
pylink.getEYELINK().sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
if tracker_software_ver>=4:
	pylink.getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET")
else:
	pylink.getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")
#do tracker setup
if eyelink_ver != 0:
    eye_tracker.doTrackerSetup()
eye_tracker.setOfflineMode()

#-----------------------------------------------------------------------------


#initialize the class for generation of trial parameters
#-----------------------------------------------------------------------------
print 'trial setup'
init_parameters = init()
#generate trial parameters for the upcomming trials
timing, difficulties, inversions, EV_gap, blocks = init_parameters.load_trial_parameters()
#-----------------------------------------------------------------------------


#preparation of trials: prepare output to file
#-----------------------------------------------------------------------------
win = visual.Window(size=globvar.window_size, fullscr=globvar.full_screen)
#write a short readme to the output file
output_user_interaction = open('choice_study_user_input.txt','w')
print>>output_user_interaction, '#output format is the following'
print>>output_user_interaction, '#trial_type, user_active?, user_input_key, accepted difficulty, accepted reward, accepted dif*reward, rejected difficulty, rejected reward, rejected dif*reward, inversions'
print>>output_user_interaction, '#difficulty refers to the exptected participant performance as set in trial_parameters'
print>>output_user_interaction, '#the three columns of inversions refer to the inversion of the default arrangement of the displayed elements. 1 means default arrangement, -1 means inverse of default arrangement.'
print>>output_user_interaction, '#1) the task markers where by default marker_1 is left and marker_2 is right 2) to the task difficulty where by default easy is left and hard is right and 3) to the response markers where again by default marker_1 is left and marker_2 is right'

output_trial_timing = open('choice_study_trial_timing.txt','w')
print>>output_trial_timing, '#this file contains the data for timing of each trial'
print>>output_trial_timing, '#output is given relative timing to trial start. output format is the following:'
print>>output_trial_timing, '#trial_type, time_tasks, time_delay_1, time_options, time_delay_2, time_decision, time_baseline time_trial_end, user_reaction_time'
#-----------------------------------------------------------------------------

#preparation of trials: short introduction and explanation slide
#-----------------------------------------------------------------------------
message1 = visual.TextStim(win=win, text='Wellcome to the experiment! \n \n \n \n \n \n The experiment can be paused by pressing p or be ended by pressing escape on the response slide.')
message1.draw()
win.flip()
core.wait(2)
#-----------------------------------------------------------------------------


#iterate over requested number of blocks and set parameters
#-----------------------------------------------------------------------------
for block, kind in enumerate(blocks):
    i1 = block*globvar.blocks[1]
    i2 = (block+1)*globvar.blocks[1]
    #announce block!
    if kind == 'math':
        announce_text = 'Arithmetic'
    if kind == 'dot':
        announce_text = 'Random Dot Motion'
    if kind == 'audio':
        announce_text = 'Audio'
    text = visual.TextStim(win, text=announce_text, bold=True, height=0.2, pos=(0,0))
   
    text.draw()
    win.flip()
    core.wait(3)
    win.flip()
    core.wait(1)

    #write a short note to the output file, if a new block starts
    print>>output_user_interaction, 'start ', kind, ' block ' + `block`
    print>>output_trial_timing, 'start ', kind, ' block ' + `block`

#-----------------------------------------------------------------------------

#run the actual trials and record user input
#-----------------------------------------------------------------------------
    for i in range(i1,i2):
        if eyelink_ver != 0:
            if eye_tracker.isConnected()==False:
                print 'SCANNER CONNECTION LOST'
            pylink.getEYELINK().startRecording(1, 1, 0, 0)
        #set trial parameters
        current_trial = trial(kind, EV_gap[i], win, timing[i,:], globvar.spacing, difficulties[i,:], inversions[i,:])
        #run trial
        current_trial.run_trial()
        #data from trial.getData() is kind, user_active[y,n], input_key, difficulty_chosen, reward_chosen, dif*rew, 
        #                                                                difficulty_rejected, reward_rejected, dif*rew
        print 'stimuli type is ', current_trial.name, 'difficuly gap is ', EV_gap[i]
        print 'user difficulty choice is ', current_trial.user_input[2]
        print 'user reaction time is ', current_trial.tR
        #save data from each trial, timing of slides, user input and inversions of stimuli
        print>>output_user_interaction, str(current_trial.premature_input).strip('[]')
        print>>output_user_interaction, str(current_trial.getData()).strip('()'), str(inversions[i,:]).strip('[]')
        print>>output_trial_timing, str(current_trial.getTiming()).strip('()')
        del current_trial
        if eyelink_ver !=0:
            pylink.getEYELINK().stopRecording()
win.close()
output_user_interaction.close()
output_trial_timing.close()
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#present actual tasks to participant
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
#evaluate user input and save relevant data
#-----------------------------------------------------------------------------

if pylink.getEYELINK() != None:
   # File transfer and cleanup!
    pylink.getEYELINK().setOfflineMode();                          
    pylink.msecDelay(500);                 

    #Close the file and transfer it to Display PC
    pylink.getEYELINK().closeDataFile()
    pylink.getEYELINK().receiveDataFile(globvar.edf_filename, globvar.edf_filename)
    pylink.getEYELINK().close();
