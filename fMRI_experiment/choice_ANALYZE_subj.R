# choice task analysis script for flavia
# by richard
# 07/2014

# Flavia says:
#   The analysis script should process the log file and spit out (for visual,
#                                                                 auditory, arithmetic):
#   - % trials in which higher EV chosen, % lower EV chosen, % incorrect
#     response
#   - % of "difficult" trials in which the higher EV was chosen, % of "easy"
#     trials in which higher EV was chosen

##### start of the script here ####
library(reshape)
library(ggplot2)

# what subject should be analyzed?
subj_id <- 056
run_nr <- 1
path <- "/home/jakob/Code/MPIB/Flavia/fMRI_experiment/raw_output"
path_to_data <- file.path(path, paste("sub", sprintf("%03d",subj_id), "_run", run_nr,  "_behavioral.txt", sep=""))

data_choice_task <- data.frame(read.table(file=path_to_data, header=TRUE, sep=",", stringsAsFactors=FALSE))
str(data_choice_task)
data_choice_task$modality <- factor(data_choice_task$modality)
levels(data_choice_task$modality) <- c("visual","auditory","arithmetic")

# compute exact ev distance
data_choice_task$ev_distance_exact <- abs(data_choice_task$ev_1 - data_choice_task$ev_2)
table(data_choice_task$ev_distance_exact)
data_choice_task$reward_distance_exact <- abs(data_choice_task$reward_1 - data_choice_task$reward_2)
table(data_choice_task$reward_distance_exact)

# how many invalid trials are there? extract invalid trials
table(data_choice_task$modality, data_choice_task$high_ev_chosen)
data_choice_task_correct <- data_choice_task[data_choice_task$high_ev_chosen==0 | data_choice_task$high_ev_chosen==1, ]


# aggregate. first, check whether people choose higher ev more reliably in the large ev_distance condition
data_agg_c <- cast(data=data_choice_task_correct, value="high_ev_chosen", modality + ev_distance  ~ .,  
                   function(x) c( M = mean(x), 
                                  SD = sd(x), 
                                  N = length(x), 
                                  SE = signif(sd(x)/sqrt(length(x)), 2) ))
# plot this
p_data_agg_c <- qplot(data=data_agg_c, x=ev_distance, y=M, facets=modality ~ . ,
                         xlab="EV distance", ylab="% higher EV chosen (+/-SE)", geom=c("line", "point") ) +
  geom_errorbar(aes(max = M + SE, min = M - SE), width=.15, size=1) +  geom_point(size=5) + geom_line(size=1) #+ 
p_data_agg_c + theme_bw(base_size=20) + ggtitle("Choice task")



