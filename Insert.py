import requests
def Insert():
	response=requests.post('https://checkoutstaff.000webhostapp.com/CTDT/Insert.php',data={'user':'hello','licno':'tn33e407','amount':'500'})
	#print(response.text)
	if "Succes" in response.text:
		print("Successfully Executed")
		#return 1
	else:
		print("Error in execution")
		#return 0
Insert()	
