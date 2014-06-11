fMRI_FF
=======

fMRI experiment for Flavia Filimon @ MPIB

Usage Instructions:
-------------------------------------------------

To start the experiment open the trial_structure.py file using the psychopy standalone program.
The programm requires the followint files to be in the same folder as the trial_structure.py:
-trial_classes.py
-trial_parameters.py
-star.png
-square.png
-speaker_symbol.png
-ba.wav
-da.wav
-ru.wav
-lu.wav

The programm accepts Input during the Response phase.
Possible inputs are:
left arrow
right arrow
p
esc

Left/Right arrows are for user input, p is for pause, esc is for quitting the experiment.

Experiment Structure
-------------------------------------------------
The experiments consists of N blocks of N trials each.
Each trial is structured in 3 stages.
1) In the first stage, the participant is presented with the stimuli which are either dot motion, arithmetic or auditorial tasks.
The participants is presented with two tasks of the same kind but of different difficulty for 1300 ms each with a 200 ms delay after every task.
After the first stage there is a variable delay of 1500 ms to 3000 ms.

2) In the second stage the participant is presented with two combinations of markers and monetary rewards. The left combination refers to the first task shown in the previous state, the right combination refers to the second.
After the second stage there is again a variable delay of 1500 ms to 3000 ms.

3) In the third stage the participant is requested to choose one of the two presented tasks/rewards. Therefore the markers are shown again (not necessarily in the same possition) and the participant has to choose one using left and right arrow keys.

Experiment Parameters
-------------------------------------------------

The parameters of the experiment can be modified within the trial_parameters file.
The file is structured in four sections:

1) General Settings

-fmri_time=(real): the time for one fmri sweep in seconds. All other time settings are given in units of this fmri time.
-blocks=[(int),(int)]: the first entry of the tuple is the number of blocks, the second is the number of trials per block.
-trial_modi=[(string),...,(string)]: trial modi to be used in the experiment. Possible entries are 'math', 'dot', 'audio'.
-size=(real): paremeter for overall spacing of visual objects. Gives distance of markers and rewards from fixation cross and defines size of task stimuli.
-spacing[(x1,y1),...,(x7,y7)] with xi, yi real: coordinates of visual components relative to the center of the screen
-file_marker_1=(string): gives the relative path of the file to be displayed as marker_1
-file_marker_2=(string): same for marker_2
-speaker_symbol=(string): gives the relative path of the file to be displayed when sound is playing
-possible_rdm_direcions=[[(ang1),(dir1),...,[(angN),(dirN)]] with angi=(real), diri=(string): gives the possible directions for random dot motions.where ang is the angle and dir the according direction.
-window_size=((int),(int)): gives the window widht x hight size in pixels.
-full_screen=(bolean): sets the full screen modus on or off.

2) Time Settings

Time settings are given in units of fmri_time. Fixed times are set as (real), variable times are set as [(min),(max)].
time_stim_1, time_stim_2, time_break_1 and time_break_2 are times for the stimuli and breaks in the first stage of the trial.
time_options is the time for the presentation of the choice options and time_response is the time the subject has to make a choice and input a keystroke. time_delay_1, time_delay_2 and time_baseline are min and max of the variable delays between stimuli, option and response stage and for the baseline at the end of each trial

-max_rep is the maximum number of repetitions of all random elements in the experiment (i.e. trial type, delay times and marker possitions)

3) Difficulty Settings

For the difficulty settings it is necessary to know that there again two types of trials. One where the difficulties of the presented tasks are clearly distinguishable and one where the difficulties of the presented tasks are more similliar yet still distinct.
The settings for the first type are denoted with an _l at the end, the settings for the second type are marked with an _s.

-reward_hard=[(real),(real)]: sets min and max of the monetary reward for the hard task.
-reward_easy=[(real),(real)]: sets min and max of the monetary reward for the easy taks.

For the different types of trials one has to set the actual parameters for the trial and the anticipated performance of the participant seperately. The connection between both has to be known preveously. The 'difficulty' in the following denotes the anticipated fraction of trials that the participant is supposed to answer correctly and is therefore between 0 and 1.

-math_trial_intervall = [(easy),(hard)]: gives the intervals for the solution of the easy vs. hard arithmetic tasks.
-dot_motion_trial_coherence = [(real),(real)]: gives the coherence in [0,1] of the random dot motion for the easy vs. hard rdm trials.
-audio_trial_stn_ratio = [(easy),(hard)]: gives the signal to noise ratio for the easy vs. hard audio trials. a stn_ratio  of 0.2 means that the signal consists of 20% noise and 80% signal.

4) Eye Tracker Settings



