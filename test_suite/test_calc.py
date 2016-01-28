from test import calc_times

def test_brevet():

	#brevdist < 200
	assert calc_times(200,150)[0] == 4.41
	assert calc_times(200,150)[1] == 10.0
	
	#brevdist <= control
	assert calc_times(200,200)[0] == 5.88
	assert calc_times(200,200)[1] == 13.5
	
	assert calc_times(200,205)[0] == 5.88
	assert calc_times(200,205)[1] == 13.5

	#control is 890 (must be broken up)
	assert calc_times (1000,890)[0] == 29.16
	assert calc_times (1000,890)[1] == 65.38
	
	
	
	
test_brevet()