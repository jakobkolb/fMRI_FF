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

    def define_slide_A(self):
        if self.flip[0] == 0:
            mpos1 = self.pos_marker_1
            mpos2 = self.pos_marker_2
        elif self.flip[0] == 1:
            mpos1 = self.pos_marker_2
            mpos2 = self.pos_marker_1
 
        marker_1= visual.ImageStim(self.window, image=globvar.file_marker_1, pos=mpos1)
        marker_2= visual.ImageStim(self.window, image=globvar.file_marker_2, pos=mpos2)

        cross   = visual.TextStim(self.window, color=-1, colorSpace='rgb', text='+', pos=self.pos_fixcross)

        if self.flip[1] == 0:
            spos1 = self.pos_stim_1
            spos2 = self.pos_stim_2
        elif self.flip[1] == 1:
            spos1 = self.pos_stim_2
            spos2 = self.pos_stim_1
        
#define stimuli here as stim_1 and stim_2
        print self.name
        if self.name=='dot':
            direction = 0
            stim_1 = visual.TextStim(self.window, text='dotstim1', pos=spos1)
            stim_2 = visual.TextStim(self.window, text='dotstim2', pos=spos2)

        elif self.name=='audio':
            stim_1 = visual.TextStim(self.window, text='audiostim1', pos=spos1)
            stim_2 = visual.TextStim(self.window, text='audiostim2', pos=spos2)

        elif self.name=='math':
            stim_1 = visual.TextStim(self.window, text='mathstim1', pos=spos1)
            stim_2 = visual.TextStim(self.window, text='mathstim2', pos=spos2)

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
        if self.flip[0] == 0:
            mpos1 = self.pos_marker_1
            mpos2 = self.pos_marker_2
        elif self.flip[0] == 1:
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

    def run_trail(self):
        self.define_slide_A()
        self.window.flip()
        core.wait(self.time_stimulus)
        self.define_slide_B()
        self.window.flip()
        core.wait(self.time_delay_1)
        self.define_slide_C()
        self.window.flip()
        core.wait(self.time_decision)
#record keystroke here
        self.input_stack = event.getKeys(keyList=['left', 'right'] ,timeStamped=True)
#did user make input or sleep?        
        if np.shape(self.input_stack)[0] > 0: #input
            tmp1, tmp2 = self.input_stack[0]
#parse user input to numbers (binary: left=1, right=0)
            if tmp1 == 'left':
                self.user_input = [1,tmp2,1]
            elif tmp1 == 'right':
                self.user_input = [0,tmp2,1]
        elif np.shape(self.input_stack)[0] == 0: #sleep
            self.user_input = [0,0,0]
        self.define_slide_D()
        self.window.flip()
        core.wait(self.time_delay_2)


