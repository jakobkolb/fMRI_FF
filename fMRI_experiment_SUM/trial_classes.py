#----------------------------------------------------------------------------
#this class can be used to structure one trial.
#one trial is initiated by evoking a trial() object with the following input
#kind           The type of the trial (visual, arithmetic, auditory)
#win            The experiment window for display of visuals
#trial_number   The number of the ongoing trial


#----------------------------------------------------------------------------
#the trial is activated by calling the self.run_trail() method.

from psychopy import core, visual, sound, event, gui
import numpy as np
import matplotlib.pyplot as mp
import random
import wave
import trial_parameters as globvar
from struct import pack
import pylink
import operator
import pickle

def prod(iterable):
        return reduce(operator.mul, iterable, 1)

class trial:
    'class to outline trial structure'
    trialCount = 0
    ts = globvar.fmri_time

#initialization of the trial parameters

    def __init__(self, kind, win, trial_number, anouncement):
        self.easyhard       = 0
        self.difficulty     = 0
        self.anounce        = anouncement
        self.corrupted      = False
        self.name           = kind
        self.window         = win
        self.flip           = globvar.run_parameters['inversions'][trial_number,:] #inversions specify if task order, 
                                                                                   #high ev possition on reward slide 
                                                                                   #and marker possition from options to 
                                                                                   #reward slide is reversed
        self.pos_stim_1     = globvar.spacing[0]    #position of right stimulus
        self.pos_stim_2     = globvar.spacing[1]    #position of left stimulus
        self.pos_marker_1   = globvar.spacing[2]    #position of motor marker 1
        self.pos_marker_2   = globvar.spacing[3]    #position of motor marker 2
        self.pos_reward_1   = globvar.spacing[4]    #position of the prize for task 1
        self.pos_reward_2   = globvar.spacing[5]    #position of the prize for task 2
        self.pos_fixcross   = globvar.spacing[6]    #position of fixation cross
        self.dif_stim_1     = globvar.run_parameters['difficulties'][trial_number,0]    #expected subj acc for fist stim
        self.dif_stim_2     = globvar.run_parameters['difficulties'][trial_number,1]    #expected subj acc for second stim
        self.EV_1           = globvar.run_parameters['EV_values'][trial_number,0]       #expected value for first stim
        self.EV_2           = globvar.run_parameters['EV_values'][trial_number,1]       #expected value for second stim
        self.EV_gap         = globvar.run_parameters['EV_gap'][trial_number]            #ev gap for this trial (small/large)
        self.par_stim_1     = globvar.run_parameters['stim_parameters'][trial_number,0] #parameters for first stim
        self.par_stim_2     = globvar.run_parameters['stim_parameters'][trial_number,1] #parameters for second stim
        self.reward_1       = globvar.run_parameters['rewards'][trial_number,0]         #reward for first stim
        self.reward_2       = globvar.run_parameters['rewards'][trial_number,1]         #reward for second stim
        self.time_stim_1    = globvar.run_parameters['timing'][trial_number,0]*trial.ts  #display time for stimulus
        self.time_break_1   = globvar.run_parameters['timing'][trial_number,1]*trial.ts  #display time for first delay
        self.time_stim_2    = globvar.run_parameters['timing'][trial_number,2]*trial.ts  #display time for stimulus
        self.time_break_2   = globvar.run_parameters['timing'][trial_number,3]*trial.ts  #display time for first delay
        self.time_delay_1   = globvar.run_parameters['timing'][trial_number,4]*trial.ts  #display time for first delay
        self.time_options   = globvar.run_parameters['timing'][trial_number,5]*trial.ts  #display time for decision screen
        self.time_delay_2   = globvar.run_parameters['timing'][trial_number,6]*trial.ts  #display time for first delay
        self.time_decision  = globvar.run_parameters['timing'][trial_number,7]*trial.ts  #display time for decision screen
        self.time_baseline  = globvar.run_parameters['timing'][trial_number,8]*trial.ts  #display time for baseline
        trial.trialCount    += 1


#routine to return user input data from the trial
    def getData(self):
        
        #account for balancing of EV possition on Options slide
        if self.flip[1] == 1:
            self.highEVpossition = 'high_left' 
        elif self.flip[1] == -1:
            self.highEVpossition = 'high_right'
        if self.name == 'visual':
            self.modality = 1
        elif self.name == 'auditory':
            self.modality = 2
        elif self.name == 'arithmetic':
            self.modality = 3
        #THIS IS A DUMMY AND HAS TO BE CORRECTED AS SOON AS THE CORRECT ARITHMETIC TRIAL IS IMPLEMENTED
        self.arith_single_digits = 1

        return  [0,0,0,
                self.modality,
                0,
                self.EV_gap,
                self.highEVpossition,
                self.arith_single_digits,#something weird that richard made up
                str(self.stimulus_1),#direction, lower boundary of sum, or sound
                str(self.par_stim_1),#coherence, whatever, noise ratio
                str(self.reward_1),
                str(self.dif_stim_1),
                str(self.EV_1),
                str(self.stimulus_2),
                str(self.par_stim_2),
                str(self.reward_2),
                str(self.dif_stim_2),
                str(self.EV_2),
                self.key_pressed,
                str(self.tr),
                self.high_ev_chosen]

#routine to refresh the visual elements of the 
#experiment window and check for premature/late
#user input
    def refresh(self, elements):
        #draw all elements from input (fixation cross, stimuli, rewards, markers, whatever you put in)
        for element in elements:
            element.draw()
        self.window.flip()
        core.wait(0.01)
        #wait for user input/exit signal
        for key in event.getKeys():
            if key == globvar.exit_key:
                self.window.close()
                globvar.output_user_interaction.close()
                globvar.output_run_timing.close()
                core.quit()
            if key in globvar.participant_input_keys:
                print>>globvar.output_run_timing, globvar.experiment_timer[-1].getTime(), \
                            'PREMATURE_INPUT', key
                self.corrupted = True
#routine to write regressor timestamps
    def write_regressor_timestamp(self, regressor):
        print>>globvar.output_run_timing, globvar.sequential_timer[-1], \
                regressor +  self.name + 'EVgap' + self.EV_gap

#routine to present anouncement slide at beginning of each block
    def present_anouncement(self):
        self.stim = []
        if self.name == 'visual':
            self.stim.extend([visual.TextStim(win=self.window, text='VISUAL')])
        elif self.name == 'arithmetic':
            self.stim.extend([visual.TextStim(win=self.window, text='ARITHMETIC')])
        elif self.name == 'auditory':
            self.stim.extend([visual.TextStim(win=self.window, text='AUDITORY')])

        while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + globvar.time_anouncement:
            self.refresh(self.stim)

        self.write_regressor_timestamp('message')
        globvar.sequential_timer[-1] += globvar.time_anouncement

         
#routine to present baseline slide and prepare stimuli in the background:
    def present_baseline(self):
        print 'baseline'
        #create and show elements of baseline slide:
        self.window.clearBuffer()
        cross = visual.TextStim(self.window, 
                                color=-1, 
                                colorSpace='rgb', 
                                text='+', 
                                pos=self.pos_fixcross, 
                                height=globvar.text_height*globvar.f_y)
        self.refresh([cross])

        #Preparestimuli:
        #create visual stimuli:
        if self.name=='visual':
            #randomly choose direction of rdm and according correct answer
            dot_direction_1, self.correct_answer_easy = random.choice(globvar.possible_rdm_directions)
            dot_direction_2, self.correct_answer_hard = random.choice(globvar.possible_rdm_directions)
            self.stimulus_1, self.stimulus_2 = dot_direction_1, dot_direction_2 
            #setup rdm coherences from difficulty levels
            dot_coherence_1, dot_coherence_2 = self.par_stim_1, self.par_stim_2
            #put dot stimuli into a list
            self.stim = []
            self.stim.extend([visual.DotStim(
                    #constant parameters for dot motion
                    self.window, color=(1.0,1.0,1.0), nDots=500, fieldShape='circle',
                    dotLife=2, signalDots='same', noiseDots='direction', speed=0.01, 
                    #variable parameters for dot motion
                    fieldSize=4*globvar.size,
                    coherence=dot_coherence_1,
                    dir=dot_direction_1,
                    fieldPos=self.pos_stim_1
                    )])
            self.stim.extend([visual.DotStim(
                    #constant parameters for dot motion
                    self.window, color=(1.0,1.0,1.0), nDots=500, fieldShape='circle',
                    dotLife=2, signalDots='same', noiseDots='direction', speed=0.01, 
                    #variable parameters for dot motion
                    fieldSize=4*globvar.size,
                    coherence=dot_coherence_2,
                    dir=dot_direction_2,
                    fieldPos=self.pos_stim_2
                    )])
            #resize stimuli according to screen size
            for stimulus in self.stim:
                stimulus.fieldSize*=(globvar.f_x,globvar.f_y)


        #Generate stimuli for arithmetic trial
        elif self.name=='arithmetic':
            self.trial_data = 3
            #Ofset of numbers from absolute task position
            x_offset = globvar.size*globvar.f_x
            y_offset = globvar.size*globvar.f_y
            relative_number_possitions=[(-x_offset,-y_offset),
                                        ( x_offset,-y_offset),
                                        ( x_offset, y_offset),
                                        (-x_offset, y_offset)]
#########################################################################################
#HI RICHARD - THESE ARE THE NUMBERS THAT HAVE TO BE GENERATED ACCORDING TO YOU NEW SCHEME:
            numbers = np.zeros((2,4))
            #Generation of numbers to sum over by the participant
            for i in range(4):
                numbers[0,i] = np.random.randint(1,21)
                numbers[1,i] = np.random.randint(1,21)
            
            self.stimulus_1, self.stimulus_2 = sum(numbers[0,:]), sum(numbers[1,:])
#########################################################################################
            #generate stimuli and put them in a list
            self.stim_1 = []
            self.stim_2 = []
            for i in range(4):
                #calculate the positions of the numbers relative to the absolute task position
                p1 = tuple(x+y for x,y in zip(self.pos_stim_1, relative_number_possitions[i]))
                p2 = tuple(x+y for x,y in zip(self.pos_stim_2, relative_number_possitions[i]))
                #add all numbers belonging to one task to one list.
                self.stim_1.extend([ visual.TextStim(self.window, text=`int(numbers[0,i])`, pos=p1,
                                height=globvar.text_height*globvar.f_y)])
                self.stim_2.extend([ visual.TextStim(self.window, text=`int(numbers[1,i])`, pos=p2,
                                height=globvar.text_height*globvar.f_y)])
            #append fixation cross to stimuli list
            self.stim_1.extend([cross])
            self.stim_2.extend([cross])

        #generate stimuli for auditory trial:
        elif self.name=='auditory':
            t1 = globvar.experiment_timer[-1].getTime()
            stim_files=globvar.audio_files
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
            self.stimulus_1, self.stimulus_2 = sound_1, sound_2
            #then we open the according wav files
            file_1 = wave.open(globvar.audio_file_folder + sound_1 + '.wav','r')
            file_2 = wave.open(globvar.audio_file_folder + sound_2 + '.wav','r')
            #and get their file details
            #Returns a tuple (nchannels, sampwidth, framerate, nframes, comptype, compname)
            file_1_parameters = file_1.getparams()
            file_2_parameters = file_2.getparams()
            #since the sound tracks will be combined, they must have the same length
            sound_frames = min(file_1_parameters[3], file_2_parameters[3])
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
            #set noise levels
            noise_level_1 = self.par_stim_1
            noise_level_2 = self.par_stim_2
            #ad noise to signals
            stim_1_data = np.zeros((sound_frames))
            stim_2_data = np.zeros((sound_frames))
            for i in range(sound_frames):
                stim_1_data[i] = (  file_1_data[i]*(1-noise_level_1) 
                                    + noise[i]*noise_level_1*file_1_data[i]*globvar.noise_factor)
                stim_2_data[i] = (  file_2_data[i]*(1-noise_level_2) 
                                    + noise[i]*noise_level_2*file_2_data[i]*globvar.noise_factor)
                #cut sound tracks if their combined amplitude exceeds the max_amplitude of the source file
                if abs(stim_1_data[i]) > max_amp_file_1:
                    sign_1 = file_1_data[i]/abs(file_1_data[i])
                    stim_1_data[i] = max_amp_file_1*sign_1
                if abs(stim_2_data[i]) > max_amp_file_2:
                    sign_2 = file_2_data[i]/abs(file_2_data[i])
                    stim_2_data[i] = max_amp_file_2*sign_2
            #normalize audio streams to fixed amplitude
            amp1 = max(abs(stim_1_data))
            amp2 = max(abs(stim_2_data))
            max_amp = globvar.max_amp
            stim_2_data = stim_2_data/amp2*max_amp
            stim_1_data = stim_1_data/amp1*max_amp
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
            #generate sound stimulus. open sound files in row
            self.audit_stim_1 = sound.Sound(value=stim_files[0], sampleRate = file_1_parameters[3])
            self.audit_stim_2 = sound.Sound(value=stim_files[1], sampleRate = file_1_parameters[3])
            print globvar.speaker_size, globvar.f_y
            self.speaker_symbol = visual.ImageStim(  self.window, 
                                                image=globvar.speaker_symbol, 
                                                pos=(0,globvar.size), 
                                                size = globvar.speaker_size)
            self.speaker_symbol.size*=(globvar.f_x, globvar.f_y)
 

        while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_baseline:
            self.refresh([cross])

        self.write_regressor_timestamp('baseline')
        globvar.sequential_timer[-1] += self.time_baseline



#routine to present stimuli to participant
    def present_stimuli(self):
        print 'stim', self.name
        #define fixation cross
        cross   = visual.TextStim(  self.window, color=-1, colorSpace='rgb', 
                                    text='+', pos=self.pos_fixcross, 
                                    height=globvar.text_height*globvar.f_y)
        
        #define stimuli here as stim_1 and stim_2 according to self.name 
        #with difficulties from randomization 'dot' is for random dot movement, 
        #'math' is for arithmetic task and 'noise' will be for noise task
        
        #present stimuli and breaks according to timing and print entries to timestamp file
        #present visual stimuli (random dot motion)
        if self.name=='visual':


            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_stim_1:
                self.refresh([self.stim[0], cross])

            self.write_regressor_timestamp('stim1')
            globvar.sequential_timer += self.time_stim_1

            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_break_1:
                self.refresh([cross])

            globvar.sequential_timer += self.time_break_1


            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_stim_2:
                self.refresh([self.stim[1], cross])

            self.write_regressor_timestamp('stim2')
            globvar.sequential_timer += self.time_stim_2

            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_break_2:
                self.refresh([cross])

            globvar.sequential_timer += self.time_break_2


        #present arithmetic stimuli
        elif self.name=='arithmetic':

            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_stim_1:
                self.refresh(self.stim_1)

            self.write_regressor_timestamp('stim1')
            globvar.sequential_timer += self.time_stim_1

            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_break_1:
                self.refresh([cross])

            globvar.sequential_timer += self.time_break_1


            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_stim_2:
                self.refresh(self.stim_2)

            self.write_regressor_timestamp('stim2')
            globvar.sequential_timer += self.time_stim_2

            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_break_2:
                self.refresh([cross])

            globvar.sequential_timer += self.time_break_2
        
        #draw icons and play sound for auditory trial
        if self.name=='auditory':
            
            self.audit_stim_1.play(loops = 0)

            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_stim_1:
                self.refresh([self.speaker_symbol, cross])

            self.write_regressor_timestamp('stim1')
            globvar.sequential_timer += self.time_stim_1

            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_break_1:
                self.refresh([cross])

            self.audit_stim_1.stop()
            globvar.sequential_timer += self.time_break_1

            self.audit_stim_2.play(loops = 0)

            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_stim_2:
                self.refresh([self.speaker_symbol, cross])

            self.write_regressor_timestamp('stim2')
            globvar.sequential_timer += self.time_stim_2

            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_break_2:
                self.refresh([cross])

            self.audit_stim_2.stop()
            globvar.sequential_timer += self.time_break_2

#routine to present ption slide with markers and rewards
    def present_options(self):
        print 'options'
        #define marker stimuli with files defined in globvar.py
        marker_1= visual.ImageStim( self.window, 
                                    image=globvar.file_marker_1,
                                    pos=self.pos_marker_1,
                                    size = globvar.marker_size)
        marker_2= visual.ImageStim( self.window, 
                                    image=globvar.file_marker_2,
                                    pos=self.pos_marker_2,
                                    size = globvar.marker_size)
        #resize markers according to display size
        marker_1.size*=(globvar.f_x,globvar.f_y)
        marker_2.size*=(globvar.f_x,globvar.f_y)
        #define fixation cross
        cross   = visual.TextStim(  self.window, 
                                    color=-1, 
                                    colorSpace='rgb', 
                                    text='+',
                                    pos=self.pos_fixcross, 
                                    height=globvar.text_height*globvar.f_y)
        #define reward stimuli according to the possitions of the easy and hard_l task
        eur = u"\u20AC"
        #reward 1 is allways left and corresponds to EV[i,0]
        #reward 2 is allways right and corresponds to EV[i,1]
        reward_1 = visual.TextStim( self.window, 
                                    text= `round(self.reward_1,2)` + eur,
                                    pos=self.pos_reward_1, 
                                    height=globvar.text_height*globvar.f_y)
        reward_2 = visual.TextStim( self.window, 
                                    text= `round(self.reward_2,2)` + eur,
                                    pos=self.pos_reward_2, 
                                    height=globvar.text_height*globvar.f_y)

        #write markers and rewards to screen
        event.clearEvents()

        #check for premature input
        while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_options:
            self.refresh([marker_1, marker_2, reward_1, reward_2, cross])

        self.write_regressor_timestamp('options')
        globvar.sequential_timer[-1] += self.time_options


#routine to present delay slide 1 without interactivity
    def present_delay_1(self):
        print 'delay1'
        self.window.clearBuffer()
        #define fixation cross
        cross = visual.TextStim(self.window, 
                                color=-1, 
                                colorSpace='rgb', 
                                text='+',
                                pos=self.pos_fixcross, 
                                height=globvar.text_height*globvar.f_y)
        event.clearEvents()

        for i in range(int(self.time_delay_1/globvar.fmri_time)):


            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + globvar.fmri_time:
                self.refresh([cross])

            #write timestamp to file
            self.write_regressor_timestamp('delay1')

            globvar.sequential_timer[-1] += globvar.fmri_time


#routine to present delay slide 2 without interactivity
    def present_delay_2(self):
        print 'delay2'
        self.window.clearBuffer()
        #define fixation cross
        cross = visual.TextStim(self.window, 
                                color=-1, 
                                colorSpace='rgb', 
                                text='+',
                                pos=self.pos_fixcross, 
                                height=globvar.text_height*globvar.f_y)

        event.clearEvents()

        for i in range(int(self.time_delay_2/globvar.fmri_time)):



            while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + globvar.fmri_time:
                self.refresh([cross])

            #write timestamp to file
            self.write_regressor_timestamp('delay2')

            globvar.sequential_timer[-1] += globvar.fmri_time

#routine to present decision slide and recording of user input
    def present_response(self):
        print 'response'
        
        #revert marker possitions according to flip
        self.window.clearBuffer()
        if self.flip[3] == 1:
            mpos1 = self.pos_marker_1
            mpos2 = self.pos_marker_2
        elif self.flip[3] == -1:
            mpos1 = self.pos_marker_2
            mpos2 = self.pos_marker_1
        #define markers
        marker_1= visual.ImageStim( self.window, 
                                    image=globvar.file_marker_1,
                                    pos=mpos1,
                                    size =globvar.marker_size)
        marker_2= visual.ImageStim( self.window, 
                                    image=globvar.file_marker_2,
                                    pos=mpos2, 
                                    size = globvar.marker_size)
        #resize markers according to display size
        marker_1.size*=(globvar.f_x,globvar.f_y)
        marker_2.size*=(globvar.f_x,globvar.f_y)
        #define fixation cross
        cross   = visual.TextStim(self.window, 
                                    color='red', 
                                    colorSpace='rgb', 
                                    text='+',
                                    pos=self.pos_fixcross, 
                                    height=globvar.text_height*globvar.f_y)
        #draw markers and fixation cross to buffer
        marker_1.draw()
        marker_2.draw()
        cross.draw()
        #clear events: empty user input list before response is recorded
        event.clearEvents()
        #initiate countown for response time
        timer = core.CountdownTimer(self.time_decision)
        #present response slide and write timestamp to file
        self.window.flip()
        #wait for time_decision seconds for user input
        #record keystroke here as [input==True, key, rt]
        self.user_input = []
        user_active = False
        nout = 0
        self.key_pressed = 'none'
        while globvar.experiment_timer[-1].getTime() < globvar.sequential_timer[-1] + self.time_decision:
            for key in event.getKeys():
                #check wheather user input is one of left, right 
                #and set his choice parameter accordingly
                if key in globvar.participant_input_keys and user_active == False:
                    self.tr = self.time.getTime()-self.t_response
                    if key == globvar.participant_input_keys[0]:
                        self.key_pressed = 'left'
                        choice = 1
                    elif key == globvar.participant_input_keys[1]:
                        self.key_pressed = 'right'
                        choice = -1
                    marker_flips = [2,3]
                    EV_flips = [1,2,3]
                    #figure out which reward/difficulty level the user 
                    #accepted/rejected by cross checking his choice
                    #with the position of the elements in the trial. 
                    #by default easy trial is first, low reward is left and
                    #marker_1 is always left each deviation of this setup 
                    #is given by a flip = -1.
                    if prod(self.flip[marker_flips])*choice == 1:
                        accepted_choice_reward = self.reward_1
                        rejected_choice_reward = self.reward_2
                        accepted_choice_dif = self.dif_stim_1
                        rejected_choice_dif = self.dif_stim_2
                    elif prod(self.flip[marker_flips])*choice == -1:
                        accepted_choice_reward = self.reward_2
                        rejected_choice_reward = self.reward_1
                        accepted_choice_dif = self.dif_stim_2
                        rejected_choice_dif = self.dif_stim_1
                    if prod(self.flip[EV_flips])*choice == 1:
                        accepted_EV = 'high'
                        self.high_ev_chosen = 1
                    elif prod(self.flip[EV_flips])*choice == -1:
                        accepted_EV = 'low'
                        self.high_ev_chosen = 0
                    print>>globvar.output_run_timing, globvar.experiment_timer[-1].getTime(), \
                            'user_input', 'reaction_time=',self.tr,\
                            ' accepted_EV=', accepted_choice_reward*accepted_choice_dif, \
                            ' rejected_EV=', rejected_choice_reward*rejected_choice_dif, \
                            ' EV_gap=', self.EV_gap

                    user_active = True
                    self.user_input = [ 1,
                                        key,
                                        accepted_choice_dif, 
                                        accepted_choice_reward, 
                                        accepted_choice_dif*accepted_choice_reward, 
                                        rejected_choice_dif, 
                                        rejected_choice_reward, 
                                        rejected_choice_dif*rejected_choice_reward]
                #check wheaterh user wants to exit experiment
                elif key == globvar.exit_key:
                    print 'aborting'
                    message = visual.TextStim(  win=self.window, 
                                                text='you pressed escape. \n The experiment will now end.', 
                                                height=globvar.text_height*globvar.f_y)
                    message.draw()
                    self.window.flip()
                    core.wait(3)
                    self.window.close()
                    core.quit()
                #pause experiment if user presses 'p'
                elif key == globvar.pause_key:
                    pause = True
                    message = visual.TextStim(  win=self.window, 
                                                text='the experiment is paused \n press p again to continue', 
                                                height=globvar.text_height*globvar.f_y)
                    message.draw()
                    self.window.flip()
                    while pause == True:
                        for key in event.getKeys(keyList=['p']):
                            if key == globvar.pause_key:
                                pause = False

        if user_active == False:
            print>>globvar.output_run_timing, globvar.experiment_timer[-1].getTime(), \
                    'NO_USER_RESPONSE'
            self.tr = -78
            self.high_ev_chosen = -78
            self.user_input = [0,'none',0,0,0,0,0,0]

        self.write_regressor_timestamp('response')
        globvar.sequential_timer += self.time_decision
        if self.corrupted:
            self.high_ev_chosen = -79
        print globvar.sequential_timer

#Method to run trial i.e. define slides, show for certain time, record user input. Store data.

    def run_trial(self):
        #start time counter for the trial
        self.time = core.MonotonicClock()

#------------------------------------
        #for every first trial of a block make an announcement
        if self.anounce:
            self.present_anouncement()
#------------------------------------
        #slide for baseline time
        #get time of baseline slide
        self.t_baseline = self.time.getTime()
        #present baseline slide
        self.present_baseline()
        #get time of end of trial
        self.t_end = self.time.getTime()
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
        self.number_of_trials = globvar.blocks[0]*globvar.blocks[1]
        
    def load_trial_parameters(self):
        
        with open('run_parameters/run_'+`globvar.run_number`+'_parameters_.p', 'rb') as fp:
                    globvar.run_parameters = pickle.load(fp)

    def participant_parameter_dialog(self):
       # first, we ask for the subject id etc
       myDlg = gui.Dlg(title="Flavia's fMRI Study")
       myDlg.addText('Subject info')
       myDlg.addField('ID:', globvar.participant_id)
       myDlg.addText('RDM coherence')
       myDlg.addField('easy:', globvar.dot_motion_trial_coherence[0])
       myDlg.addField('hard:', globvar.dot_motion_trial_coherence[1])
       myDlg.addText('Auditory noise')
       myDlg.addField('easy:', globvar.audio_trial_stn_ratio[0])
       myDlg.addField('hard:', globvar.audio_trial_stn_ratio[1])
       myDlg.addText('Arithmetic range')
       myDlg.addField('easy:', globvar.math_trial_interval[0])
       myDlg.addField('hard:', globvar.math_trial_interval[1])
       myDlg.addText('Expected accuracy')
       myDlg.addField('easy:', globvar.anticipated_participant_performance[0])
       myDlg.addField('hard:', globvar.anticipated_participant_performance[1])
       myDlg.addText('Run number')
       myDlg.addField('Nr.', globvar.run_number)
       myDlg.show()  # show dialog and wait for OK or Cancel
       if myDlg.OK:  # then the user pressed OK
           subjinfo = myDlg.data
           globvar.participant_id = subjinfo[0]
           globvar.dot_motion_trial_coherence[0] = subjinfo[1]
           globvar.dot_motion_trial_coherence[1] = subjinfo[2]
           globvar.audio_trial_stn_ratio[0] = subjinfo[3]
           globvar.audio_trial_stn_ratio[1] = subjinfo[4]
           globvar.math_trial_interval[0] = subjinfo[5]
           globvar.math_trial_interval[1] = subjinfo[6]
           globvar.anticipated_participant_performance[0] = subjinfo[7]
           globvar.anticipated_participant_performance[1] = subjinfo[8]
           globvar.run_number = subjinfo[9]
    def randomize_participant_specific_variables(self):
        blocks = globvar.run_parameters['blocks']
        EV_gap = globvar.run_parameters['EV_gap']
        EV_values = globvar.run_parameters['EV_values']
        timing = globvar.run_parameters['timing']
        inversions = globvar.run_parameters['inversions']


        #deduced variables:     first/second participant performance aka. 
        #                       difficulties, fist/second stim_parameter
        difficulties = np.zeros((self.number_of_trials,2))
        stim_parameters = np.zeros((self.number_of_trials,2))

        #calculated variables:  Rewards(left, right)
        rewards = np.zeros((self.number_of_trials,2))

        #fig1 = mp.figure()
        #mp.hist(EV_value[:,0] - EV_value[:,1], bins = 2)
        #fig2 = mp.figure()
        #mp.hist(abs(EV_value[:,0] - EV_value[:,1]), bins = 2)
        #mp.show()

        #set first/second expected participant performance and stimulus parameter

        for i in range(globvar.blocks[0]):
            kind = blocks[i]
            i1 = i*globvar.blocks[1]
            i2 = (i+1)*globvar.blocks[1]
            for j in range(i1,i2):
                difficulty = globvar.anticipated_participant_performance 
                if kind == 'arithmetic':
                    stim_parameter = globvar.math_trial_interval
                elif kind == 'visual':
                    stim_parameter = globvar.dot_motion_trial_coherence
                elif kind == 'auditory':
                    stim_parameter = globvar.audio_trial_stn_ratio
                if inversions[j,0] == 1:
                    difficulties[j,:] = difficulty
                    stim_parameters[j,:] = stim_parameter
                elif inversions[j,0] == -1:
                    difficulties[j,:] = [difficulty[1],difficulty[0]]
                    stim_parameters[j,:] = [stim_parameter[1], stim_parameter[0]]

        #calculate left/right rewards from participant performance and EV

        for i in range(self.number_of_trials):
            for j in range(2):
                rewards[i,j] = round(float(EV_values[i,j])/difficulties[i,j],globvar.digits)
                EV_values[i,j] = rewards[i,j]*difficulties[i,j]

        globvar.run_parameters['EV_values'] = EV_values
        globvar.run_parameters['difficulties'] = difficulties
        globvar.run_parameters['stim_parameters'] = stim_parameters
        globvar.run_parameters['rewards'] = rewards

        with open(globvar.output_folder + 'full_run_parameters_participant'+`globvar.participant_id`+'run'+`globvar.run_number`+'.p', 'wb') as fb:
                    pickle.dump(globvar.run_parameters, fb)

        return blocks, EV_gap, timing, inversions, EV_values, difficulties, stim_parameters, rewards

