import numpy as np
import matplotlib.pyplot as mp

#Reward randomization from Richard

def randomize_two_rewards((lower_1, upper_1),(lower_2, upper_2)): 
    from numpy import random
    val_1 = random.randint(lower_1*10,upper_1*10+1)
    val_2 = random.randint(lower_2*10,upper_2*10+1)
    return float(val_1)/10, float(val_2)/10

#assumed participant performances on hard and easy tasks

diff_hard = 0.9
diff_easy = 0.65

#Reward intervals currently in use

reward_high_s = [4,7]          
reward_low_s = [3,6]
reward_high_l = [6,8]          
reward_low_l = [2,4]

#number of hypothetic trials in this statistical analysis

trial_number = 1024

#Array for trial balancing parameters relevant for EV calculation

trial_parameters = np.zeros((trial_number,3))
#0:diff left/right
#1:higher reward left/right
#2:high or small reward difference

#Arrays for actual trial parameters resulting from balancing

diff_left = np.zeros((trial_number))
diff_right = np.zeros((trial_number))

reward_left = np.zeros((trial_number))
reward_right = np.zeros((trial_number))

EV_difference = np.zeros((trial_number))
EV_difference_l = np.zeros((trial_number/2))
EV_difference_s = np.zeros((trial_number/2))
m=0
n=0

#Balancing according to Richard:
#1st stage:
#Half of the trials have difficult task first, half of the trials have difficult task second
#2nd stage:
#Half of the 'difficult task first' trials have high reward difference half of them have small reward
#difference. Half of the 'difficult task second' trials have high reward difference, the other half
#has low reward difference
#3rd stage:
#Of the resulting proportions each proportion has high reward left (corresponding to first task) 
#and half of the time and high reward right (corresponding to second task) the other half of the time.

for i in range(trial_number):
    j = i%(trial_number)
#half of the trials is hard
    if j<trial_number/2:
        trial_parameters[i,0] = 1
        diff_left[i] = diff_hard
        diff_right[i] = diff_easy
    elif j>= trial_number/2:
        trial_parameters[i,0] = 2
        diff_left[i] = diff_easy
        diff_right[i] = diff_hard
    k = i%(trial_number/2)
#half of this half has high reward difference
    if k < trial_number/4:
        trial_parameters[i,1] = 1
        reward_high = reward_high_l
        reward_low = reward_low_l
    elif k >= trial_number/4:
        trial_parameters[i,1] = 2
        reward_high = reward_high_s
        reward_low = reward_low_s
    l = i%(trial_number/4)
#half of the resulting fourth has high reward left
    if l < trial_number/8:
        trial_parameters[i,2] = 1
        reward_left[i], reward_right[i] = randomize_two_rewards((reward_high[0],reward_high[1]),(reward_low[0],reward_low[1]))
    elif l >= trial_number/8:
        trial_parameters[i,2] = 2
        reward_right[i], reward_left[i] = randomize_two_rewards((reward_high[0],reward_high[1]),(reward_low[0],reward_low[1]))
#as a result all combinations of task difficulty, reward difference and reward size are equally distributed.
#This does not mean that this is the case for EV differences as you will see.


#For the resulting combinations EV gaps are calculated for all tasks together and for wide and small
#reward difference separately.

    EV_difference[i] = (diff_left[i]*reward_left[i] - diff_right[i]*reward_right[i])
    if k < trial_number/4:
        EV_difference_l[m] = abs(diff_left[i]*reward_left[i] - diff_right[i]*reward_right[i])
        m += 1
    elif k >= trial_number/4:
        EV_difference_s[n] = abs(diff_left[i]*reward_left[i] - diff_right[i]*reward_right[i])
        n += 1

#Resulting reward distributions are plotted in histograms

fig1 = mp.figure()
ax1 = fig1.add_subplot(111)
mp.hist(EV_difference)
ax1.set_title('distribution of EV difference for all modalities')
ax1.set_xlabel('EV difference')

fig2 = mp.figure()
ax2 = fig2.add_subplot(111)
mp.hist(EV_difference_l)
ax2.set_title('distribution of EV difference for large reward gap')
ax2.set_xlabel('EV difference')

fig3 = mp.figure()
ax3 = fig3.add_subplot(111)
mp.hist(EV_difference_s)
ax3.set_title('distribution of EV difference for small reward gap')
ax3.set_xlabel('EV difference')

mp.show()
