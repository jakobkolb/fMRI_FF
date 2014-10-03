install.packages("pixmap")

library(pixmap)

setwd("/Users/filevich/MPI_data/face_land_MRI/eyetrack_analysis")
setwd("/Users/elisa/MPI_data/face_land_MRI/eyetrack_analysis")

# this will need to be made into a for loop

gaze <- as.matrix(read.csv(file="FACE_Img1_fa03_3.csv", header=FALSE))
colnames(gaze) <- c("time", "x", "y", "pupil")

#now invert y, so that x and y coordinates of both psychtoolbox and eyedata match the image
gaze[,'y'] <- -1*gaze[,'y']

require(pixmap)
theImage <- read.pnm("/Users/elisa/Dropbox/Elisa and Maxis folder/more FALA images/final images/monocular_1.pnm")


plot(theImage) #find a way to plot this onto the right pixels
par(new=TRUE)
plot(gaze[,'x'], gaze[,'y'])








