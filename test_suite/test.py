def calc_times(brevdist, control):
 
	brev_list=[(200,15,34),(200,15,32),(200,15,30),(400,11.428,28),(300,13.333,26)]
  
	finished_close={200:13.5,300:20,400:27,600:40,1000:75}
	finished_open={200:5.8833333,300:9,400:12.1333333,600:18.8,1000:21.0833333}
  
	intopen = 0
	intclose = 0
	finished = "Race not yet finished"
  

	#race is finished 
	if (control >= brevdist):
		intopen	 =finished_open[brevdist]
		intclose =finished_close[brevdist]
		finished = "Race is Finished!" 
	#control < brevdist
	elif control < brev_list[0][0]:
		intopen += control/(brev_list[0][2])
		intclose += control/(brev_list[0][1])
	else:
		km_counter = control
		for i in range(len(brev_list)): 
			if (km_counter >= brev_list[i][0]):
				km_counter = km_counter - brev_list[i][0]
				intopen += (brev_list[i][0])/(brev_list[i][2])
				intclose+= (brev_list[i][0])/(brev_list[i][1])
			
			elif(0 < km_counter <brev_list[i][0]):	
				intopen += (km_counter)/(brev_list[i][2])
				intclose += (km_counter)/(brev_list[i][1])
				break
	return[round(intopen,2),round(intclose,2)] 
  	