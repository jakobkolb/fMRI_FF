#----------------------------------------------------------------------------
#this class can be used to structure one trial.
#input is:
#kind   :   the kind of stimulus presented
#win    :   the window the stimulus will be presented in
#timing :   time each slide shall be presented
#spacing:   spacing array containing the positions of the different objects in the trail
#           [stim1, stim2, marker1, marker2, fixation_cross]
#difficulties : difficulties for the different stimuli

#----------------------------------------------------------------------------
#trial is activated by calling the self.run_trail() method.

from psychopy import core, visual, sound, event
import numpy as np
import random
import wave
import trial_parameters as globvar
from struct import pack
import pylink
class trial:
    'class to outline trial structure'
    trialCount = 0
    ts = globvar.fmri_time


#initialization of the trial parameters

    def __init__(self, kind, gap, win, timing, spacing, difficulties, inversions):
        self.name           = kind
        self.diff_gap       = gap
        self.window         = win
        self.flip           = inversions
        self.pos_stim_1     = spacing[0]    #position of right stimulus
        self.pos_stim_2     = spacing[1]    #position of left stimulus
        self.pos_marker_1   = spacing[2]    #position of motor marker for stim_1
        self.pos_marker_2   = spacing[3]    #position of motor marker for stim_2
        self.pos_reward_1   = spacing[4]    #position of the prize for task 1
        self.pos_reward_2   = spacing[5]    #position of the prize for task 2
        self.pos_fixcross   = spacing[6]    #position of fixation cross
        self.dif_easy       = difficulties[0] #difficulty for easy stimulus
        self.dif_hard       = difficulties[1] #difficulty for hard stimulus
        self.time_stim_1    = timing[0]*trial.ts  #display time for stimulus
        self.time_stim_2    = timing[1]*trial.ts  #display time for stimulus
        self.time_break_1   = timing[2]*trial.ts  #display time for first delay
        self.time_break_2   = timing[3]*trial.ts  #display time for first delay
        self.time_options   = timing[4]*trial.ts  #display time for decision screen
        self.time_delay_1   = timing[5]*trial.ts  #display time for first delay
        self.time_delay_2   = timing[6]*trial.ts  #display time for first delay
        self.time_decision  = timing[7]*trial.ts  #display time for decision screen
        self.time_baseline  = timing[8]*trial.ts  #display time for baseline
        trial.trialCount    += 1
#define different slides for the trial (A: Stimulus, B: Delay, C: Decision, D: Baseline)
    def getData(self):
        return  self.name, \
                self.user_input[0], \
                self.user_input[1], \
                self.user_input[2], \
                self.user_input[3], \
                round(self.user_input[4],4), \
                self.user_input[5], \
                self.user_input[6], \
                round(self.user_input[7],4)
                
    def getTiming(self):
        return  self.name, self.t_stimuli, self.t_delay_1, self.t_options, self.t_delay_2, self.t_response, self.t_baseline, self.t_end, self.tR

    def present_stimuli(self):
        #reverse task position and time if flip[1] == -1. default is easy first on the left, hard second on the right
        if self.flip[1] == 1:
            stime1, spos1 = 0, self.pos_stim_1
            stime2, spos2 = 1, self.pos_stim_2
        elif self.flip[1] == -1:
            stime1, spos1 = 1, self.pos_stim_2
            stime2, spos2 = 0, self.pos_stim_1

        #define fixation cross
        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)
        #define stimuli here as stim_1 and stim_2 according to self.name
        #stim_1 is easy, stim_2 is hard
        #'dot' is for random dot movement, 'math' is for arithmetic task and 'noise' will be for noise task
        if self.name=='dot':
            #randomly choose direction of rdm and according correct answer
            dot_direction_1, self.correct_answer_easy = random.choice(globvar.possible_rdm_directions)
            dot_direction_2, self.correct_answer_hard = random.choice(globvar.possible_rdm_directions)
            #setup rdm coherences from difficulty levels
            dot_coherence_1, dot_coherence_2 = self.dif_easy, self.dif_hard
            stim = []
            stim.extend([visual.DotStim(
                    #constant parameters for dot motion
                    self.window, color=(1.0,1.0,1.0), nDots=500, fieldShape='circle', fieldSize=4*globvar.size, 
                    dotLife=5, signalDots='same', noiseDots='direction', speed=0.005, 
                    #variable parameters for dot motion
                    coherence=dot_coherence_1,
                    dir=dot_direction_1,
                    fieldPos=spos1
                    )])
            stim.extend([visual.DotStim(
                    #constant parameters for dot motion
                    self.window, color=(1.0,1.0,1.0), nDots=500, fieldShape='circle', fieldSize=4*globvar.size,
                    dotLife=5, signalDots='same', noiseDots='direction', speed=0.005, 
                    #variable parameters for dot motion
                    coherence=dot_coherence_2,
                    dir=dot_direction_2,
                    fieldPos=spos2
                    )])
            t1 = self.time_stim_1+self.time_stim_2+self.time_break_1+self.time_break_2
            dot_timer = core.CountdownTimer(t1)
            while True :
                t = t1 - dot_timer.getTime()
                if (t>=t1):
                    break
                if (0<t and t<self.time_stim_1):
                    stim[stime1].draw()
                elif (self.time_stim_1+self.time_break_1<t and t<self.time_stim_1 + self.time_break_1 + self.time_stim_2):
                    stim[stime2].draw()
                cross.draw()
                self.window.flip()
                core.wait(0.01)
                
        elif self.name=='math':
            #generate numbers for the actual arithmetic task
            self.numbers_to_sum = np.zeros((4))
            for i in range(4):
                self.numbers_to_sum[i] = np.random.randint(1,21)
            self.correct_answer = sum(self.numbers_to_sum)
            #build intervals around the correct answer
            easy_interval = '+/-'+`int(self.dif_easy)`
            hard_interval = '+/-'+`int(self.dif_hard)`
            #create stimuli for the intervals
#            stim_1 = visual.TextStim(self.window, text=easy_interval, pos=spos1)
#            stim_2 = visual.TextStim(self.window, text=hard_interval, pos=spos2)

            #Ofset of numbers from absolute task position
            offset = globvar.size
            relative_number_possitions=[(-offset, -offset),(offset,-offset),(offset,offset),(-offset,offset)]
            numbers = np.zeros((2,4))
            #Generation of numbers to sum over by the participant
            for i in range(4):
                numbers[0,i] = np.random.randint(1,21)
                numbers[1,i] = np.random.randint(1,21)
            #generate stimuli 
            stim_1 = []
            stim_2 = []
            for i in range(4):
                #calculate the positions of the numbers relative to the absolute task position
                p1 = tuple(x+y for x,y in zip(spos1, relative_number_possitions[i]))
                p2 = tuple(x+y for x,y in zip(spos2, relative_number_possitions[i]))
                #add all numbers belonging to one task to one list.
                stim_1.extend([visual.TextStim(self.window, text=`int(numbers[0,i])`, pos=p1)])
                stim_2.extend([visual.TextStim(self.window, text=`int(numbers[1,i])`, pos=p2)])

            stim_1.extend([visual.TextStim(self.window, text=easy_interval, color='red', 
                colorSpace='rgb', pos = (0,1.7*offset))])
            stim_2.extend([visual.TextStim(self.window, text=hard_interval, color='red', 
                colorSpace='rgb', pos = (0,1.7*offset))])
            #draw elements on slide

            #draw all numbers belonging to the tasks by iterating the list of numbers
            
            t1 = self.time_stim_1+self.time_stim_2+self.time_break_1+self.time_break_2
            dot_timer = core.CountdownTimer(t1)
            while True :
                t = t1 - dot_timer.getTime()
                if (t>=t1):
                    break
                if stime1 == 0 :
                    if (0<t and t<self.time_stim_1):
                        [stim.draw() for stim in stim_1]
                    elif (self.time_stim_1+self.time_break_1<t and t<self.time_stim_1 + self.time_break_1 + self.time_stim_2):
                        [stim.draw() for stim in stim_2]
                elif stime1 == 1 :
                    if (0<t and t<self.time_stim_1):
                        [stim.draw() for stim in stim_2]
                    elif (self.time_stim_1+self.time_break_1<t and t<self.time_stim_1 + self.time_break_1 + self.time_stim_2):
                        [stim.draw() for stim in stim_1]
                cross.draw()
                self.window.flip()
                core.wait(0.01)

        elif self.name=='audio':
            stim_files=['stim_file_1.wav','stim_file_2.wav']
            #we weather ru|lu or ba|da sould be right resp. left
            sounds = [['ru','lu'],['ba','da']]
            rd = range(3)
            for i in range(3):
                rd[i] = np.random.randint(0,2)
            i_1 = rd[0]
            i_2 = (rd[0]+1)%2
            #and chose then, which of ru|lu and ba|da will be played
            sound_1 = sounds[i_1][rd[1]]
            sound_2 = sounds[i_2][rd[2]]
            #then we open the according wav files
            file_1 = wave.open(sound_1 + '.wav','r')
            file_2 = wave.open(sound_2 + '.wav','r')
            #and get their file details
            #Returns a tuple (nchannels, sampwidth, framerate, nframes, comptype, compname)
            file_1_parameters = file_1.getparams()
            file_2_parameters = file_2.getparams()
            print file_1_parameters
            print file_2_parameters
            #since the sound tracks will be combined, they must have the same length
            sound_frames = min(file_1_parameters[3], file_2_parameters[3])
            print sound_frames, file_1_parameters[3], file_2_parameters[3]
            #read raw wav data from files
            file_1_raw = file_1.readframes(sound_frames)
            file_2_raw = file_2.readframes(sound_frames)
            #unpack wav data to be able to work with it
            file_1_data = np.frombuffer(file_1_raw, dtype='<i2')
            file_2_data = np.frombuffer(file_2_raw, dtype='<i2')
            #extract maximum amplitude from wav data
            max_amp_file_1 = max(abs(file_1_data))
            max_amp_file_2 = max(abs(file_2_data))
            #create white noise
            noise = np.random.randn(sound_frames)
            #switch noise levels on left and right chanal according to flip
            if self.flip[1] == 1:
                noise_level_1 = self.dif_easy
                noise_level_2 = self.dif_hard
            elif self.flip[1] == -1:
                noise_level_1 = self.dif_hard
                noise_level_2 = self.dif_easy
            #ad noise to signals
            stim_1_data = np.zeros((sound_frames))
            stim_2_data = np.zeros((sound_frames))
            for i in range(sound_frames):
                stim_1_data[i] = (file_1_data[i]*(1-noise_level_1) + noise[i]*noise_level_1*max_amp_file_1)/2.
                stim_2_data[i] = (file_2_data[i]*(1-noise_level_2) + noise[i]*noise_level_2*max_amp_file_2)/2.
                #cut sound tracks if their combined amplitude exceeds the max_amplitude of the source file
                if abs(stim_1_data[i]) > max_amp_file_1:
                    sign_1 = file_1_data[i]/abs(file_1_data[i])
                    stim_1_data[i] = max_amp_file_1*sign_1
                if abs(stim_2_data[i]) > max_amp_file_2:
                    sign_2 = file_2_data[i]/abs(file_2_data[i])
                    stim_2_data[i] = max_amp_file_2*sign_2
            #open output files
            stim_file_1 = wave.open(stim_files[0], 'w')
            stim_file_2 = wave.open(stim_files[1], 'w')
            #set output file parameters
            stim_file_1.setparams((2,2,file_1_parameters[2],0,'NONE', 'not compressed'))
            stim_file_2.setparams((2,2,file_1_parameters[2],0,'NONE', 'not compressed'))
            #merge sound tracks for output and pack them to an appropriate data format
            stim_sound_data_1 = ''
            stim_sound_data_2 = ''
            for i in range(sound_frames):
                stim_sound_data_1 += pack('h', stim_1_data[i]) #track for file_1
                stim_sound_data_1 += pack('h', stim_1_data[i]) #track for file_1
                stim_sound_data_2 += pack('h', stim_2_data[i]) #track for file_2
                stim_sound_data_2 += pack('h', stim_2_data[i]) #track for file_2
            #write data to file
            stim_file_1.writeframes(stim_sound_data_1)
            stim_file_2.writeframes(stim_sound_data_2)
            stim_file_1.close()
            stim_file_2.close()
            file_1.close()
            file_2.close()
            #generate sound stimulus
            audit_stim_1 = sound.Sound(value=stim_files[stime1], sampleRate = file_1_parameters[3])
            audit_stim_2 = sound.Sound(value=stim_files[stime2], sampleRate = file_1_parameters[3])
            speaker_symbol = visual.ImageStim(self.window, image=globvar.speaker_symbol, pos=(0,globvar.size), size = 0.2)
            #draw other objects
            cross.draw()
            #flip window and play sound
            self.window.flip()
            t1 = self.time_stim_1+self.time_stim_2+self.time_break_1+self.time_break_2
            dot_timer = core.CountdownTimer(t1)
            start1, stop1 = False, False
            start2, stop2 = False, False
            while True :
                t = t1 - dot_timer.getTime()
                print t
                if (t>=t1):
                    break
                if (0<t and start1 == False):
                    audit_stim_1.play(loops = -1)
                    start1 = True
                    print '1 started'
                if (0<t and t<self.time_stim_1):
                    cross.draw()
                    speaker_symbol.draw()
                elif (self.time_stim_1<t and stop1 == False):
                    audit_stim_1.stop()
                    stop1 = True
                    print '1 stopped'
                elif (self.time_stim_1+self.time_break_1<t and start2 == False):
                    audit_stim_2.play(loops = -1)
                    start2 = True
                    print '2 started'
                elif (self.time_stim_1+self.time_break_1<t and t<self.time_stim_1 + self.time_break_1 + self.time_stim_2):
                    cross.draw()
                    speaker_symbol.draw()
                elif (self.time_stim_1 + self.time_break_1 + self.time_stim_2<t and stop2 == False):
                    audit_stim_2.stop()
                    stop2 = True
                    print '2 stopped'
                self.window.flip()
        else :
            stim_1 = visual.TextStim(self.window, text='someotherstim1', pos=spos1)
            stim_2 = visual.TextStim(self.window, text='someotherstim2', pos=spos2)
            stim_1.draw()
            stim_2.draw()
            cross.draw()

#Option slide with markers and rewards
    def present_options(self):
        #reverse position of markers if flip[0] == -1
        if self.flip[0] == 1:
            mpos1 = self.pos_marker_1
            mpos2 = self.pos_marker_2
        elif self.flip[0] == -1:
            mpos1 = self.pos_marker_2
            mpos2 = self.pos_marker_1
        #reverse reward position if flip[1] == -1. default is easy on the left, hard on the right
        if self.flip[1] == 1:
            rpos1 = self.pos_reward_1
            rpos2 = self.pos_reward_2
        elif self.flip[1] == -1:
            rpos1 = self.pos_reward_2
            rpos2 = self.pos_reward_1

        #define marker stimuli with files defined in globvar.py
        print globvar.file_marker_1, mpos1
        marker_1= visual.ImageStim(self.window, image=globvar.file_marker_1, pos=mpos1)
        marker_2= visual.ImageStim(self.window, image=globvar.file_marker_2, pos=mpos2)
        #define fixation cross
        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)
        #calculate random reward (equally distributed in intervals defined in globvar.py)
        if self.diff_gap == 'small':
            self.reward_1 = round(globvar.reward_easy_s[0] + 
                    (globvar.reward_easy_s[1] - globvar.reward_easy_s[0])*np.random.rand(),2)
            self.reward_2 = round(globvar.reward_hard_s[0] + 
                    (globvar.reward_hard_s[1] - globvar.reward_hard_s[0])*np.random.rand(),2)
        if self.diff_gap == 'large':
            self.reward_1 = round(globvar.reward_easy_l[0] + 
                    (globvar.reward_easy_l[1] - globvar.reward_easy_l[0])*np.random.rand(),2)
            self.reward_2 = round(globvar.reward_hard_l[0] + 
                    (globvar.reward_hard_l[1] - globvar.reward_hard_l[0])*np.random.rand(),2)
        #define reward stimuli according to the possitions of the easy and hard_l task
        eur = u"\u20AC"
        reward_1 = visual.TextStim(self.window, text= `round(self.reward_1,2)` + eur, pos=rpos1)
        reward_2 = visual.TextStim(self.window, text= `round(self.reward_2,2)` + eur, pos=rpos2)

        marker_1.draw()
        marker_2.draw()
        reward_1.draw()
        reward_2.draw()
        cross.draw()
        self.window.flip()
        core.wait(self.time_options)

#Delay slide 1 without interactivity

    def present_delay_1(self):
        timer = core.CountdownTimer(self.time_delay_1)
        print 'define slide B'
        self.window.clearBuffer()
        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)
        cross.draw()
        event.clearEvents()
        self.premature_input = []
        active = False
        self.window.flip()
        while timer.getTime() > 0:
            for key in event.getKeys():
                self.premature_input = ['premature input',key]
                active = True
        if active == False:
            self.premature_input = ['no input during delay','']


#Delay slide 2 without interactivity

    def present_delay_2(self):
        timer = core.CountdownTimer(self.time_delay_2)
        print 'define slide B'
        self.window.clearBuffer()
        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)
        cross.draw()
        event.clearEvents()
        self.premature_input = []
        active = False
        self.window.flip()
        while timer.getTime() > 0:
            for key in event.getKeys():
                self.premature_input = ['premature input',key]
                active = True
        if active == False:
            self.premature_input = ['no input during delay','']


#Decision slide presented during recording of user input

    def present_response(self):
        print 'present slide C'
        #load actual difficulties from trial_parameters according to trial modus
        if self.diff_gap == 'small':
            if self.name == 'dot':
                expected_performace_easy = globvar.dot_motion_difficulty_s[0]
                expected_performace_hard = globvar.dot_motion_difficulty_s[1]
            elif self.name == 'audio':
                expected_performace_easy = globvar.audio_trial_difficulty_s[0]
                expected_performace_hard = globvar.audio_trial_difficulty_s[1]
            elif self.name == 'math':
                expected_performace_easy = globvar.math_trial_difficulty_s[0]
                expected_performace_hard = globvar.math_trial_difficulty_s[1]
        if self.diff_gap == 'large':
            if self.name == 'dot':
                expected_performace_easy = globvar.dot_motion_difficulty_l[0]
                expected_performace_hard = globvar.dot_motion_difficulty_l[1]
            elif self.name == 'audio':
                expected_performace_easy = globvar.audio_trial_difficulty_l[0]
                expected_performace_hard = globvar.audio_trial_difficulty_l[1]
            elif self.name == 'math':
                expected_performace_easy = globvar.math_trial_difficulty_l[0]
                expected_performace_hard = globvar.math_trial_difficulty_l[1]
        self.window.clearBuffer()
        if self.flip[2] == 1:
            mpos1 = self.pos_marker_1
            mpos2 = self.pos_marker_2
        elif self.flip[2] == -1:
            mpos1 = self.pos_marker_2
            mpos2 = self.pos_marker_1
        marker_1= visual.ImageStim(self.window, image=globvar.file_marker_1, pos=mpos1)
        marker_2= visual.ImageStim(self.window, image=globvar.file_marker_2, pos=mpos2)

        cross   = visual.TextStim(self.window, color='red', colorSpace='rgb', text='+', pos=self.pos_fixcross)

        marker_1.draw()
        marker_2.draw()
        cross.draw()
        #clear events: empty user input list before response is recorded
        event.clearEvents()

        timer = core.CountdownTimer(self.time_decision)
        #present response slide
        self.window.flip()
        #wait for time_decision seconds for user input
        #record keystroke here as [input==True, key, rt]
        self.user_input = []
        user_active = False
        input_correct = False
        while timer.getTime()>=0:
            for key in event.getKeys(keyList=['left','right', 'p', 'escape']):
                if key in ['left', 'right']:
                    self.tR = self.time.getTime()-self.t_response
                    if (self.flip[0]*self.flip[1]*self.flip[2]) == 1:
                        if key == 'left':
                            accepted_choice_dif, accepted_choice_reward = expected_performace_easy, self.reward_1
                            rejected_choice_dif, rejected_choice_reward = expected_performace_hard, self.reward_2
                        elif key == 'right':
                            accepted_choice_dif, accepted_choice_reward = expected_performace_hard, self.reward_2
                            rejected_choice_dif, rejected_choice_reward = expected_performace_easy, self.reward_1
                    elif (self.flip[0]*self.flip[1]*self.flip[2]) == -1:
                        if key == 'left':
                            accepted_choice_dif, accepted_choice_reward = expected_performace_hard, self.reward_2
                            rejected_choice_dif, rejected_choice_reward = expected_performace_easy, self.reward_1
                        elif key == 'right':
                            accepted_choice_dif, accepted_choice_reward = expected_performace_easy, self.reward_1
                            rejected_choice_dif, rejected_choice_reward = expected_performace_hard, self.reward_2
                    user_active = True
                    input_correc = True
                    self.user_input = [1,key,
                            accepted_choice_dif, accepted_choice_reward, accepted_choice_dif*accepted_choice_reward, 
                            rejected_choice_dif, rejected_choice_reward, rejected_choice_dif*rejected_choice_reward]
                    break
                elif key in ['escape']:
                    print 'aborting'
                    message = visual.TextStim(win=self.window, text='you pressed escape. \n The experiment will now end.')
                    message.draw()
                    self.window.flip()
                    core.wait(3)
                    self.window.close()
                    core.quit()
                elif key in ['p']:
                    self.tR = -78
                    pause = True
                    message = visual.TextStim(win=self.window, text='the experiment is paused \n press p again to continue')
                    message.draw()
                    self.window.flip()
                    while pause == True:
                        for key in event.getKeys(keyList=['p']):
                            if key == 'p':
                                pause = False
            if user_active == False:
                self.tR = -78
                self.user_input = [0,'none',0,0,0,0,0,0]
#Baseline slide

    def present_baseline(self):
        print 'define slide D'
        self.window.clearBuffer()
        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)
        cross.draw()
        self.window.flip()
        core.wait(self.time_baseline)

#Method to run trial i.e. define slides, show for certain time, record user input. Store data.

    def run_trial(self):
        #start time counter for the trial
        self.time = core.MonotonicClock()
#------------------------------------
        #get time of presentation of task slide from time counter
        self.t_stimuli = self.time.getTime()
        #present stimulus slide for time self.time_stimulus
        self.present_stimuli()
#------------------------------------
        #get time for presentation of delay slide
        self.t_delay_1 = self.time.getTime()
        #first delay slide
        self.present_delay_1()
#------------------------------------
        #show choice options and rewards
        self.t_options = self.time.getTime()
        self.present_options()
#------------------------------------
        #second delay slide
        self.t_delay_2 = self.time.getTime()
        self.present_delay_2()
#------------------------------------
        #response slide shows motor markers and records user input.
        #get start time
        self.t_response = self.time.getTime()
        #present slide
        self.present_response()
#------------------------------------
        #slide for baseline time
        #get time of baseline slide
        self.t_baseline = self.time.getTime()
        #present baseline slide
        self.present_baseline()
        #get time of end of trial
        self.t_end = self.time.getTime()


#----------------------------------------------------------------------------
#this class can be used to generate the parameters for the trials on an experiment.
#input is:
#modus              :the modus for the next trials (math, dot or audio)
#number_of_trials   :the number of the next trials of type modus
#max_rep            :the maximum number of repetitions in the parameter series allowed
#dif_easy, dif_hard :the difficulty levels for the next trials
#mean_delay_average :mean time of delay slide in units of fmri 
#mean_baseline_average:mean time of baseline slide in units of fmri
#output is timing, difficulties and inversions for the next series of trials

#----------------------------------------------------------------------------
class init:
    'class to randomize trial parameters'

    def __init__(self):
        self.desired_delay_average      = globvar.mean_delay_average
        self.desired_baseline_average   = globvar.mean_baseline_average
        self.max_rep                    = globvar.max_rep
        self.number_of_trials           = globvar.blocks[1]
        
    def rand_trial_parameters(self, kind):

        too_many_repetitions =True

        while too_many_repetitions == True:

            #time for slides
            timing = np.zeros((self.number_of_trials,9))
            timing[:,0:9] = [0,0,globvar.time_break_1,globvar.time_break_2,
                    globvar.time_options,globvar.time_delay_1[0],globvar.time_delay_2[0],
                    globvar.time_response,globvar.time_baseline[0]]

            #set timing for stimuli presentation dependent on kind 
            if kind == 'math':
                timing[:,0] = globvar.time_math_stim_1
                timing[:,1] = globvar.time_math_stim_2
            if kind == 'dot':
                timing[:,0] = globvar.time_dot_stim_1
                timing[:,1] = globvar.time_dot_stim_2
            if kind == 'audio':
                timing[:,0] = globvar.time_audio_stim_1
                timing[:,1] = globvar.time_audio_stim_2

            for i in range(self.number_of_trials):
                timing[i,5] = random.choice(range(globvar.time_delay_1[0],globvar.time_delay_1[1]+1,1))
                timing[i,6] = random.choice(range(globvar.time_delay_2[0],globvar.time_delay_2[1]+1,1))
                timing[i,8] = random.choice(range(globvar.time_baseline[0],globvar.time_baseline[1]+1,1))
            #adjust means of timing for delay and baseline slides to fit the desired time averages
            #Estimated_delay_time  = sum(timing[:,1])/self.number_of_trials
           #M   = int(self.number_of_trials*(Estimated_delay_time - self.desired_delay_average))
           #n=1
           #while n<M:
           #    #pick random time in the trial sequence
           #    i = np.random.randint(self.number_of_trials)
           #    #only change the value, if it is not equal to the time before and after
           #    if timing[i,1]-1!=timing[(i+1)%self.number_of_trials,1] \
           #            or timing[i,1]-1!=timing[(i-1)%self.number_of_trials,1] \
           #            and timing[i,1]-1>0:
           #        timing[i,1]-=1
           #        n+=1
           #Estimated_baseline_time  = sum(timing[:,3])/self.number_of_trials
           #M   = int(self.number_of_trials*(Estimated_baseline_time - self.desired_baseline_average))
           #n=1
           #while n<M:
           #    i = np.random.randint(self.number_of_trials-1)
           #    if timing[i,3]-1!=timing[(i+1)%self.number_of_trials,3] \
           #            or timing[i,3]-1!=timing[(i-1)%self.number_of_trials,3] \
           #            and timing[i,3]-2>0:
           #        timing[i,3]-=1
           #        n+=1

            #difficulties for the current trial in the form [easy, hard], units for difficulty of different trials have to be
            #set according to participants performance.
            diff_gap = []
            for i in range(self.number_of_trials):
                diff_gap.append(random.choice(['small', 'large']))

            difficulties = np.zeros((self.number_of_trials,2))
            for i in range(self.number_of_trials):
                if diff_gap[i] == 'small':
                    if kind == 'math':
                        difficulties[i,0:2] = globvar.math_trial_interval_s
                    elif kind == 'dot':
                        difficulties[i,0:2] = globvar.dot_motion_trial_coherence_s
                    elif kind == 'audio':
                        difficulties[i,0:2] = globvar.audio_trial_stn_ratio_s
                if diff_gap[i] == 'large':
                    if kind == 'math':
                        difficulties[i,0:2] = globvar.math_trial_interval_l
                    elif kind == 'dot':
                        difficulties[i,0:2] = globvar.dot_motion_trial_coherence_l
                    elif kind == 'audio':
                        difficulties[i,0:2] = globvar.audio_trial_stn_ratio_l

            #deviation from standard order of elements on slide A and C
            inversions = np.zeros((self.number_of_trials,3))
            inversions[:,0:3] = [0,0,0]
            for i in range(self.number_of_trials):
                inversions[i,0] = random.choice([-1,1])
                inversions[i,1] = random.choice([-1,1])
                inversions[i,2] = random.choice([-1,1])

            #check if the maximum number of repetitions satisfies max_rep
            too_many_repetitions = False
            for i in range(self.number_of_trials - self.max_rep):
                same_1 = True
                same_2 = True
                same_3 = True
                same_4 = True
                same_5 = True
                same_6 = True
                for j in range(i,i+self.max_rep):
                    if inversions[j,0] != inversions[i,0]:
                        same_1 = False
                        k = i
                    if inversions[j,1] != inversions[i,1]:
                        same_2 = False
                        k = i
                    if inversions[j,2] != inversions[i,2]:
                        same_3 = False
                        k = i
                    if timing[j,5] != timing[i,5]:
                        same_4 = False
                        k = i
                    if timing[j,6] != timing[i,6]:
                        same_5 = False
                        k = i
                    if timing[j,8] != timing[i,8]:
                        same_6 = False
                        k = i
                if same_1 == True or same_2 == True or same_3 == True or same_4 == True or same_5 == True or same_6 == True :
                        too_many_repetitions = True
                        break

        print 'mean delay time is ', sum(timing[:,1])/self.number_of_trials
        print 'mean baseline time is ', sum(timing[:,3])/self.number_of_trials
        return timing, difficulties, inversions, diff_gap

