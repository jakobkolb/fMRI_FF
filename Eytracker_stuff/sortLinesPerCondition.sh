#!/bin/bash

cd /Users/elisa/MPI_data/face_land_MRI/eyetrack_analysis
#cd /Users/filevich/MPI_data/face_land_MRI/eyetrack_analysis


for SUBJ in fa03 #fa02 fa03 fa04 fa05 fa06 fa07 fa08 fa09
do

	for BLOCK in 3 #4
	do

		#create empty files just to make sure you don't have the same information twice
		for  COND in FACE LAND BOTH
		do
			for IMAGE_NR in {1..7}
			do
				touch ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}.txt
			done
		done


		filename=${SUBJ}_${BLOCK}.asc
		vi
		
		while read dataLine; 
		do
  			if [[ $dataLine == *'newImageOnset im'* ]]; 
  			then 
  				
  				
  				IMAGE_NR=$(echo ${dataLine:(-2):1})
				#echo $dataLine
  				#echo ${IMAGE_NR}

				COND='none'
				
			elif [[ $dataLine == *'internalStart_self'* ]];
			then
				COND='face'

			elif [[ $dataLine == *'externalStart_self'* ]];
			then
				COND='land'
			
			elif [[ $dataLine == *'bothStart_self'* ]];
			then
				COND='both'

			# and use Fixcross/Scrambled base on as a signal to stop 
			elif [[ $dataLine == *'base on'* ]];
			then
				COND='none'	
				
  			fi  

			
			#then sort things into each file
			if [[ $COND == 'face' ]]; 
			then
	
				echo $dataLine >> FACE_Img${IMAGE_NR}_${SUBJ}_${BLOCK}.txt  			
 				
 			elif [[ $COND == 'land' ]]; 
 			then
 				echo $dataLine >> LAND_Img${IMAGE_NR}_${SUBJ}_${BLOCK}.txt
 	
		 	elif [[ $COND == 'both' ]]; 
 			then
 				echo $dataLine >> BOTH_Img${IMAGE_NR}_${SUBJ}_${BLOCK}.txt
 			fi
 	
		done < $filename    # done while loop through file



		# now clean up each one of the output files
  		for  COND in FACE LAND BOTH
		do
			for IMAGE_NR in {1..7}
			do
				#clean up all messages, fixations and missing data lines
				egrep -wv '(EFIX|SFIX|EBLINK|SBLINK|ESACC|SSACC|EYELNKMSG|END|INPUT|. . 0.0)' ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}.txt > ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}_nomsg.txt	
				
				#remove the ' ...' shit
				cat ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}_nomsg.txt | rev | cut -c 6- | rev > ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}_noEllipse.txt
				#cat ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}_clean.txt | tr -d " ..." > ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}.txt 
				
				#turn into proper csv: replace whitescpaces with commas
				cat ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}_noEllipse.txt |  tr ' ' ', ' > ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}.txt 
				
				cp ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}.txt ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}.csv 
				rm ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}_nomsg.txt
				rm ${COND}_Img${IMAGE_NR}_${SUBJ}_${BLOCK}_noEllipse.txt
				
			done
		done
 



	done    				

done 						



 


