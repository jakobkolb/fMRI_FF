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

2) Time Settings

3) Difficulty Settings

4) Eye Tracker Settings
