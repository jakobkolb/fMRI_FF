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
class trial:
    'class to outline trial structure'
    trialCount = 0
    ts = 1.5


#initialization of the trial parameters

    def __init__(self, kind, win, timing, spacing, difficulties, inversions):
        self.name           = kind
        self.window         = win
        self.flip           = inversions
        self.pos_stim_1     = spacing[0]    #position of right stimulus
        self.pos_stim_2     = spacing[1]    #position of left stimulus
        self.pos_marker_1   = spacing[2]    #position of motor marker for stim_1
        self.pos_marker_2   = spacing[3]    #position of motor marker for stim_2
        self.pos_reward_1   = spacing[4]    #position of the prize for task 1
        self.pos_reward_2   = spacing[5]    #position of the prize for task 2
        self.pos_fixcross   = spacing[6]    #position of fixation cross
        self.dif_stim_1     = difficulties[0] #difficulty of stim_1
        self.dif_stim_2     = difficulties[1] #difficulty of stim_2
        self.time_stimulus  = timing[0]*trial.ts  #display time for stimulus
        self.time_delay_1   = timing[1]*trial.ts  #display time for first delay
        self.time_decision  = timing[2]*trial.ts  #display time for decision screen
        self.time_delay_2   = timing[3]*trial.ts  #display time for baseline
        trial.trialCount    += 1
#define different slides for the trial (A: Stimulus, B: Delay, C: Decision, D: Baseline)
    def getData(self):
        return  self.name, \
                self.user_input[0], \
                self.user_input[1], \
                self.user_input[2], \
                self.user_input[3], \
                self.user_input[4] , \
                self.tA, self.tB, self.tC, self.tD, self.tEnd


    def present_slide_A(self):
        #reverse position of markers if flip[0] == -1
        if self.flip[0] == 1:
            mpos1 = self.pos_marker_1
            mpos2 = self.pos_marker_2
        elif self.flip[0] == -1:
            mpos1 = self.pos_marker_2
            mpos2 = self.pos_marker_1
        #define marker stimuli with files defined in globvar.py
        marker_1= visual.ImageStim(self.window, image=globvar.file_marker_1, pos=mpos1)
        marker_2= visual.ImageStim(self.window, image=globvar.file_marker_2, pos=mpos2)
        #define fixation cross
        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)
        #calculate random reward (equally distributed in intervals defined in globvar.py)
        self.reward_1 = round(globvar.reward_easy[0] + 
                (globvar.reward_easy[1] - globvar.reward_easy[0])*np.random.rand(),2)
        self.reward_2 = round(globvar.reward_hard[0] + 
                (globvar.reward_hard[1] - globvar.reward_hard[0])*np.random.rand(),2)

        #reverse task position if flip[1] == -1. default is easy on the left, hard on the right
        if self.flip[1] == 1:
            spos1, rpos1 = self.pos_stim_1, self.pos_reward_1
            spos2, rpos2 = self.pos_stim_2, self.pos_reward_2
        elif self.flip[1] == -1:
            spos1, rpos1 = self.pos_stim_2, self.pos_reward_2
            spos2, rpos2 = self.pos_stim_1, self.pos_reward_1
        #define reward stimuli according to the possitions of the easy and hard task
        reward_1 = visual.TextStim(self.window, text= `round(self.reward_1,2)` + ' Eur', pos=rpos1)
        reward_2 = visual.TextStim(self.window, text= `round(self.reward_2,2)` + ' Eur', pos=rpos2)

        #define stimuli here as stim_1 and stim_2 according to self.name
        #stim_1 is easy, stim_2 is hard
        #'dot' is for random dot movement, 'math' is for arithmetic task and 'noise' will be for noise task
        print self.name
        if self.name=='dot':
            #randomly choose direction of rdm and according correct answer
            dot_direction_1, self.correct_answer_easy = random.choice(globvar.possible_rdm_directions)
            dot_direction_2, self.correct_answer_hard = random.choice(globvar.possible_rdm_directions)
            #setup rdm coherences from difficulty levels
            dot_coherence_1, dot_coherence_2 = self.dif_stim_1, self.dif_stim_2

            stim_1 = visual.DotStim(
                    #constant parameters for dot motion
                    self.window, color=(1.0,1.0,1.0), nDots=500, fieldShape='circle', fieldSize=0.7, 
                    dotLife=100, signalDots='same', noiseDots='direction', speed=0.002, 
                    #variable parameters for dot motion
                    coherence=dot_coherence_1,
                    dir=dot_direction_1,
                    fieldPos=spos1
                    )
            stim_2 = visual.DotStim(
                    #constant parameters for dot motion
                    self.window, color=(1.0,1.0,1.0), nDots=500, fieldShape='circle', fieldSize=0.7,
                    dotLife=100, signalDots='same', noiseDots='direction', speed=0.002, 
                    #variable parameters for dot motion
                    coherence=dot_coherence_2,
                    dir=dot_direction_2,
                    fieldPos=spos2
                    )
            dot_timer = core.CountdownTimer(self.time_stimulus)
            while (dot_timer.getTime()>=0):
                stim_1.draw()
                stim_2.draw()
                cross.draw()
                marker_1.draw()
                marker_2.draw()
                reward_1.draw()
                reward_2.draw()
                self.window.flip()
                core.wait(0.01)
                
        elif self.name=='math':
            #generate numbers for the actual arithmetic task
            self.numbers_to_sum = np.zeros((4))
            for i in range(4):
                self.numbers_to_sum[i] = np.random.randint(1,21)
            self.correct_answer = sum(self.numbers_to_sum)
            #build intervals around the correct answer
            easy_interval = '['+`int(self.correct_answer - self.dif_stim_1)`+' - '+`int(self.correct_answer + self.dif_stim_1)`+']'
            hard_interval = '['+`int(self.correct_answer - self.dif_stim_2)`+' - '+`int(self.correct_answer + self.dif_stim_2)`+']'
            #create stimuli for the intervals
            stim_1 = visual.TextStim(self.window, text=easy_interval, pos=spos1)
            stim_2 = visual.TextStim(self.window, text=hard_interval, pos=spos2)
            #draw stimuli
            stim_1.draw()
            stim_2.draw()
            marker_1.draw()
            marker_2.draw()
            reward_1.draw()
            reward_2.draw()
            cross.draw()
            self.window.flip()
            core.wait(self.time_stimulus)


        elif self.name=='audio':
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
            #add noise to sound tracks
            if self.flip[1] == 1:
                noise_level_1 = self.dif_stim_1
                noise_level_2 = self.dif_stim_2
            elif self.flip[1] == -1:
                noise_level_1 = self.dif_stim_2
                noise_level_2 = self.dif_stim_1
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
            stim_file = wave.open('stim_file.wav', 'w')
            stim_file.setparams((2,2,file_1_parameters[3],0,'NONE', 'not compressed'))
            stim_sound_data = ''
            for i in range(sound_frames):
                stim_sound_data += pack('h', stim_1_data[i]) #track for left chanel
                stim_sound_data += pack('h', stim_2_data[i]) #track for right chanel
            stim_file.writeframes(stim_sound_data)
            stim_file.close()
            file_1.close()
            file_2.close()

            audit_stim = sound.Sound(value='stim_file.wav', sampleRate = file_1_parameters[3])
             

            marker_1.draw()
            marker_2.draw()
            reward_1.draw()
            reward_2.draw()
            cross.draw()
            self.window.flip()
            audit_stim.play(loops = -1)
            core.wait(self.time_stimulus)
            audit_stim.stop()

        else :
            stim_1 = visual.TextStim(self.window, text='someotherstim1', pos=spos1)
            stim_2 = visual.TextStim(self.window, text='someotherstim2', pos=spos2)
            marker_1.draw()
            marker_2.draw()
            stim_1.draw()
            stim_2.draw()
            cross.draw()


#Delay slide without interactivity

    def define_slide_B(self):
        print 'define slide B'
        self.window.clearBuffer()
        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)
        cross.draw()

#Decision slide presented during recording of user input

    def present_slide_C(self):
        print 'present slide C'
        self.window.clearBuffer()
        if self.flip[2] == 1:
            mpos1 = self.pos_marker_1
            mpos2 = self.pos_marker_2
        elif self.flip[2] == -1:
            mpos1 = self.pos_marker_2
            mpos2 = self.pos_marker_1
        marker_1= visual.ImageStim(self.window, image=globvar.file_marker_1, pos=mpos1)
        marker_2= visual.ImageStim(self.window, image=globvar.file_marker_2, pos=mpos2)

        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)

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
                    rt = self.time.getTime()-self.tC
                    if (self.flip[0]*self.flip[1]*self.flip[2]) == 1:
                        if key == 'left':
                            user_choice_dif, user_choice_reward = 'easy', self.reward_1
                        elif key == 'right':
                            user_choice_dif, user_choice_reward = 'hard', self.reward_2
                    elif (self.flip[0]*self.flip[1]*self.flip[2]) == -1:
                        if key == 'left':
                            user_choice_dif, user_choice_reward = 'hard', self.reward_2
                        elif key == 'right':
                            user_choice_dif, user_choice_reward = 'easy', self.reward_1
                    user_active = True
                    input_correc = True
                    self.user_input = [1,key,rt,user_choice_dif, user_choice_reward, input_correct]
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
                    pause = True
                    message = visual.TextStim(win=self.window, text='the experiment is paused \n press p again to continue')
                    message.draw()
                    self.window.flip()
                    while pause == True:
                        for key in event.getKeys(keyList=['p']):
                            if key == 'p':
                                pause = False
            if user_active == False:
                self.user_input = [0,'none',-78,'none', 0.0, input_correct]
#Baseline slide

    def define_slide_D(self):
        print 'define slide D'
        self.window.clearBuffer()
        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)

        cross.draw()

#Method to run trial i.e. define slides, show for certain time, record user input. Store data.

    def run_trial(self):
        #start time counter for the trial
        self.time = core.MonotonicClock()
        #get time of presentation of task slide from time counter
        self.tA = self.time.getTime()
        #present stimulus slide for time self.time_stimulus
        self.present_slide_A()
        #delay delay slide
        self.define_slide_B()
        #get time for presentation of delay slide
        self.tB = self.time.getTime()
        #show delay slide
        self.window.flip()
        #wait for delay time
        core.wait(self.time_delay_1)
        #response slide shows motor markers and records user input.
        #get start time
        self.tC = self.time.getTime()
        self.present_slide_C()
        #draw baseline slide
        self.define_slide_D()
        #get time of baseline slide presentation
        self.tD = self.time.getTime()
        #show baseline slide
        self.window.flip()
        #wait for baseline slide presentation
        core.wait(self.time_delay_2)
        #get time of end of trial
        self.tEnd = self.time.getTime()


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
    blub = 1

    def __init__(self, modus, number_of_trials, max_rep, dif_easy, dif_hard, mean_delay_average, mean_baseline_average):
        self.desired_delay_average      = mean_delay_average
        self.desired_baseline_average   = mean_baseline_average
        self.max_rep                    = max_rep
        self.number_of_trials           = number_of_trials
        self.dif_easy                   = dif_easy
        self.dif_hard                   = dif_hard
        self.mode                       = modus
        
    def rand_trial_parameters(self, kind):

        too_many_repetitions =True

        while too_many_repetitions == True:

            #time for slides A, B, C, D
            timing = np.zeros((self.number_of_trials,4))
            timing[:,0:4] = [3,2,1,2]
            for i in range(self.number_of_trials):
                timing[i,1] = np.random.randint(1,5)
                timing[i,3] = np.random.randint(2,5)
            #adjust means of timing for delay and baseline slides to fit the desired time averages
            Estimated_delay_time  = sum(timing[:,1])/self.number_of_trials
            M   = int(self.number_of_trials*(Estimated_delay_time - self.desired_delay_average))
            n=1
            while n<M:
                #pick random time in the trial sequence
                i = np.random.randint(self.number_of_trials)
                #only change the value, if it is not equal to the time before and after
                if timing[i,1]-1!=timing[(i+1)%self.number_of_trials,1] \
                        or timing[i,1]-1!=timing[(i-1)%self.number_of_trials,1] \
                        and timing[i,1]-1>0:
                    timing[i,1]-=1
                    n+=1
            Estimated_baseline_time  = sum(timing[:,3])/self.number_of_trials
            M   = int(self.number_of_trials*(Estimated_baseline_time - self.desired_baseline_average))
            n=1
            while n<M:
                i = np.random.randint(self.number_of_trials-1)
                if timing[i,3]-1!=timing[(i+1)%self.number_of_trials,3] \
                        or timing[i,3]-1!=timing[(i-1)%self.number_of_trials,3] \
                        and timing[i,3]-2>0:
                    timing[i,3]-=1
                    n+=1

            #difficulties for the current trial in the form [easy, hard], units for difficulty of different trials have to be
            #set according to participants performance.
            if kind == 'math':
                difficulties = np.zeros((self.number_of_trials,2))
                difficulties[:,0:4] = [10, 1]
            elif kind == 'dot':
                difficulties = np.zeros((self.number_of_trials,2))
                difficulties[:,0:4] = [1,0.1]
            elif kind == 'audio':
                difficulties = np.zeros((self.number_of_trials,2))
                difficulties[:,0:4] = [0.5,0.2]

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
                for j in range(i,i+self.max_rep):
                    if inversions[j,0] != inversions[i,0]:
                        same_1 = False
                    if  inversions[j,1] != inversions[i,1]:
                        same_2 = False
                    if inversions[j,2] != inversions[i,2]:
                        same_3 = False
                    if  timing[j,1] != timing[i,1]:
                        same_4 = False
                    if timing[j,3] != timing[i,3]:
                        same_5 = False
                if same_1 == True or same_2 == True or same_3 == True or same_4 == True or same_5 == True :
                        too_many_repetitions = True
                        break

        print 'mean delay time is ', sum(timing[:,1])/self.number_of_trials
        print 'mean baseline time is ', sum(timing[:,3])/self.number_of_trials
        return timing, difficulties, inversions

