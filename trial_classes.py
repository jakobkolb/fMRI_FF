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
import globvar
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
        self.pos_fixcross   = spacing[4]    #position of fixation cross
        self.dif_stim_1     = difficulties[0] #difficulty of stim_1
        self.dif_stim_2     = difficulties[1] #difficulty of stim_2
        self.time_stimulus  = timing[0]*trial.ts  #display time for stimulus
        self.time_delay_1   = timing[1]*trial.ts  #display time for first delay
        self.time_decision  = timing[2]*trial.ts  #display time for decision screen
        self.time_delay_2   = timing[3]*trial.ts  #display time for baseline
        trial.trialCount    += 1
#define different slides for the trial (A: Stimulus, B: Delay, C: Decision, D: Baseline)
    def getData(self):
        return self.name, self.user_input[0], self.user_input[1],self.user_input[2],self.user_input[3] , self.tA, self.tB, self.tC, self.tD


    def present_slide_A(self):
        if self.flip[0] == 1:
            mpos1 = self.pos_marker_1
            mpos2 = self.pos_marker_2
        elif self.flip[0] == -1:
            mpos1 = self.pos_marker_2
            mpos2 = self.pos_marker_1
 
        marker_1= visual.ImageStim(self.window, image=globvar.file_marker_1, pos=mpos1)
        marker_2= visual.ImageStim(self.window, image=globvar.file_marker_2, pos=mpos2)

        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)

        if self.flip[1] == 1:
            spos1 = self.pos_stim_1
            spos2 = self.pos_stim_2
        elif self.flip[1] == -1:
            spos1 = self.pos_stim_2
            spos2 = self.pos_stim_1
        
#define stimuli here as stim_1 and stim_2
        print self.name
        if self.name=='dot':
            #difficulty and direction must be set up
            dot_direction_1, dot_direction_2 = 0, 0
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
                self.window.flip()
                core.wait(0.01)
                


        elif self.name=='audio':
            stim_1 = visual.TextStim(self.window, text='audiostim1', pos=spos1)
            stim_2 = visual.TextStim(self.window, text='audiostim2', pos=spos2)
            marker_1.draw()
            marker_2.draw()
            stim_1.draw()
            stim_2.draw()
            cross.draw()


        elif self.name=='math':
            stim_1 = visual.TextStim(self.window, text='mathstim1', pos=spos1)
            stim_2 = visual.TextStim(self.window, text='mathstim2', pos=spos2)
            marker_1.draw()
            marker_2.draw()
            stim_1.draw()
            stim_2.draw()
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
        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)

        cross.draw()

#Decision slide presented during recording of user input

    def define_slide_C(self):
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

#Baseline slide

    def define_slide_D(self):
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
        #present task slide
        #delay slide
        self.define_slide_B()
        self.tB = time.getTime()
        self.window.flip()
        core.wait(self.time_delay_1)
        #response slide
        #clear events: empty user input list before response is recorded
        event.clearEvents()
        self.define_slide_C()
        #get start time
        self.tC = time.getTime()
        timer = core.CountdownTimer(self.time_decision)
        #present response slide
        self.window.flip()
        #wait for time_decision seconds for user input
        #record keystroke here as [input==True, key, rt]
        self.user_input = []
        user_active = False
        while timer.getTime()>=0:
            for key in event.getKeys(keyList=['left','right']):
                rt = time.getTime()-self.tC
                if (self.flip[0]*self.flip[1]*self.flip[2]) == 1:
                    if key == 'left':
                        user_choice_dif = 'easy'
                    elif key == 'right':
                        user_choice_dif = 'hard'
                elif (self.flip[0]*self.flip[1]*self.flip[2]) == -1:
                    if key == 'left':
                        user_choice_dif = 'hard'
                    elif key == 'right':
                        user_choice_dif = 'easy'
                self.user_input = [1,key,rt,user_choice_dif]
                user_active = True
                break
            if user_active == False:
                self.user_input = [0,'none',-78,'none']
        #draw baseline slide
        self.define_slide_D()
        self.tD = time.getTime()
        self.window.flip()
        core.wait(self.time_delay_2)
        self.tEnd = time.getTime()

