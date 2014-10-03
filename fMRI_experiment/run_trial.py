
#import dependencies
#-----------------------------------------------------------------------------
import numpy as np
from psychopy import core, visual, event, logging
from trial_classes import trial, init
import random
import trial_parameters as globvar
import pylink
import os
logging.console.setLevel(logging.CRITICAL)
#-----------------------------------------------------------------------------



#preparation of trials: prepare output to file
#-----------------------------------------------------------------------------
#create output folder if nonexistent
if not os.path.exists(globvar.output_folder):
    os.makedirs(globvar.output_folder)
#open output files
globvar.output_user_interaction = open(globvar.output_folder + 'sub' \
                                +str(globvar.participant_id).zfill(3)+'_run' \
                                +`globvar.run_number` + '_behavioral.txt','w')
globvar.output_run_timing = open(globvar.output_folder + 'sub' \
                                +str(globvar.participant_id).zfill(3)+'_run' \
                                +`globvar.run_number`+'_timestamps.txt','w')

#write a short header to the output file
print>>globvar.output_user_interaction, str(['trial_nr', 'block_trial_nr', 'trial_id', 'modality', 'block', 'ev_distance', 'position_high_ev', 'arith_single_digits', 'stimulus_1', 'difficulty_1', 'reward_1', 'exp_acc_1', 'ev_1', 'stimulus_2', 'difficulty_2', 'reward_2', 'exp_acc_2', 'ev_2', 'key_pressed', 'rt', 'high_ev_chosen']).strip('[]')

#-----------------------------------------------------------------------------


#initialize generation of trial parameters
#-----------------------------------------------------------------------------
print 'trial setup'
init_parameters = init()

#change participent specific parameters
init_parameters.participant_parameter_dialog()
    
#load balancing from file
init_parameters.load_trial_parameters()

#generate trial parameters for the upcomming trials
blocks, EV_gap, timing, \
        inversions, EV_values, \
        difficulties, stim_parameters, \
        rewards = init_parameters.randomize_participant_specific_variables()
#-----------------------------------------------------------------------------


#preparation of trials: short introduction and explanation slide
#-----------------------------------------------------------------------------
#open experiment window
win = visual.Window(size=globvar.full_window_size, fullscr=globvar.full_screen)
#define wellcome message
message1 = visual.TextStim(win=win, text='Wellcome to the experiment! \
                                        \n \n \n To start the experiment \
                                        press space. \n To quit the \
                                        experiment press escape.', \
                                        height=globvar.text_height*globvar.f_y)
#draw wellcome message to screen
message1.draw()
event.clearEvents()
win.flip()
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
pylink.getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" \
                                %(globvar.full_window_size[0], globvar.full_window_size[1]))
pylink.getEYELINK().sendMessage("screen_pixel_coords =  0 0 %d %d" \
                                %(globvar.full_window_size[0], globvar.full_window_size[1]))

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


#wait for human start signal
#-----------------------------------------------------------------------------
start_human = False
print 'waiting for human start signal'
while start_human == False:
    for key in event.getKeys():
        if key == globvar.human_start_signal:
            start_human = True
        if key == globvar.exit_key:
            win.close()
            core.quit()
#-----------------------------------------------------------------------------

#wait for machine start signal
#-----------------------------------------------------------------------------
event.clearEvents()
start_machine = False
print 'waiting for machine start signal'
while start_machine == False:
    for key in event.getKeys():
        if key == globvar.fMRI_start_signal:
            start_machine = True
#-----------------------------------------------------------------------------

#Experiment starts if both start signals are given
#initialize run timer
globvar.experiment_timer.append(core.MonotonicClock())
globvar.sequential_timer.append(0)

#iterate over requested number of blocks and set parameters
#-----------------------------------------------------------------------------
for block, kind in enumerate(blocks):
    j = 0
    i1 = block*globvar.blocks[1]
    i2 = (block+1)*globvar.blocks[1]
    print>>globvar.output_run_timing, globvar.sequential_timer[-1], \
            'start_block', block, 'of ', globvar.blocks[1], kind, 'trials'

#-----------------------------------------------------------------------------

#run the actual trials and record user input
#-----------------------------------------------------------------------------
    first_trial = True
    for i in range(i1,i2):
        j += 1
        #check if the eyetracker is still there and start recording
        if eyelink_ver != 0:
            if eye_tracker.isConnected()==False:
                print 'SCANNER CONNECTION LOST'
            pylink.getEYELINK().startRecording(1, 1, 0, 0)
        #set trial parameters
        current_trial = trial(kind,win,i,first_trial)
        first_trial = False
        #write timestamp @ start of trial
        print>>globvar.output_run_timing, globvar.sequential_timer[-1],\
                'start_trial', kind, i, 'EV_gap_is', globvar.run_parameters['EV_gap'][i]
        #run trial
        current_trial.run_trial()
        #write timestamp @ end of trial
        print>>globvar.output_run_timing, globvar.sequential_timer[-1],\
                'end_'+kind+'_trial', i
        #data from trial.getData() is kind, user_active[y,n], input_key, difficulty_chosen, reward_chosen, dif*rew, 
        #                                                                difficulty_rejected, reward_rejected, dif*rew
        #save data from each trial, timing of slides, user input and inversions of stimuli
        print>>globvar.output_user_interaction, str(current_trial.getData()).strip('[]')
        del current_trial
        #stop eyetracker recording
        if eyelink_ver !=0:
            pylink.getEYELINK().stopRecording()
#close experiment window @ end of experiment
win.close()
#close output files @ end of experiment
globvar.output_user_interaction.close()
globvar.output_run_timing.close()
#-----------------------------------------------------------------------------

#debriefing of eyetracker after experiment finished
if pylink.getEYELINK() != None:
   # File transfer and cleanup!
    pylink.getEYELINK().setOfflineMode();                          
    pylink.msecDelay(500);                 

    #Close the file and transfer it to Display PC
    pylink.getEYELINK().closeDataFile()
    pylink.getEYELINK().receiveDataFile(globvar.edf_filename, globvar.edf_filename)
    pylink.getEYELINK().close();
