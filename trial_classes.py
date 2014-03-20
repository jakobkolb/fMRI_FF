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

from psychopy import core, visual, event
import numpy as np
import random
import trial_parameters as globvar
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
        self.dif_stim_2     = difficulties[2] #difficulty of stim_2
        self.reward_1       = difficulties[1] #relative reward for task 1
        self.reward_2       = difficulties[3] #relative reward for task 2
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
                self.tA, self.tB, self.tC, self.tD


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
            #difficulty and direction must be set up
            possible_rdm_directions = [[0,'left'],[180,'right']]
            print random.choice(possible_rdm_directions)
            dot_direction_1, self.correct_answer_easy = random.choice(possible_rdm_directions)
            dot_direction_2, self.correct_answer_hard = random.choice(possible_rdm_directions)
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
            #Ofset of numbers from absolute task position
            offset = 0.1
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
            #draw elements on slide
            marker_1.draw()
            marker_2.draw()
            #draw all numbers belonging to the tasks by iterating the list of numbers
            [stim.draw() for stim in stim_1]
            [stim.draw() for stim in stim_2]
            reward_1.draw()
            reward_2.draw()
            cross.draw()
            self.window.flip()
            core.wait(self.time_stimulus)

        elif self.name=='audio':
            stim_1 = visual.TextStim(self.window, text='audiostim1', pos=spos1)
            stim_2 = visual.TextStim(self.window, text='audiostim2', pos=spos2)
            marker_1.draw()
            marker_2.draw()
            stim_1.draw()
            stim_2.draw()
            reward_1.draw()
            reward_2.draw()
            cross.draw()

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
            for key in event.getKeys(keyList=['left','right']):
                rt = time.getTime()-self.tC
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
        time = core.MonotonicClock()
        #get time of presentation of task slide from time counter
        self.tA = time.getTime()
        #present stimulus slide for time self.time_stimulus
        self.present_slide_A()
        #delay delay slide
        self.define_slide_B()
        #get time for presentation of delay slide
        self.tB = time.getTime()
        #show delay slide
        self.window.flip()
        #wait for delay time
        core.wait(self.time_delay_1)
        #response slide shows motor markers and records user input.
        #get start time
        self.tC = time.getTime()
        self.present_slide_C()
        #draw baseline slide
        self.define_slide_D()
        #get time of baseline slide presentation
        self.tD = time.getTime()
        #show baseline slide
        self.window.flip()
        #wait for baseline slide presentation
        core.wait(self.time_delay_2)
        #get time of end of trial
        self.tEnd = time.getTime()

