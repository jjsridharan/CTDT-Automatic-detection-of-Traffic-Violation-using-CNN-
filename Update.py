import requests
def update(plate):	
	response=requests.post('https://checkoutstaff.000webhostapp.com/CTDT/CheckVehicle.php',data={'license':plate})
	#print(response.text)
	if "Success" in response.text:
		response=requests.post('https://checkoutstaff.000webhostapp.com/CTDT/Update.php',data={'license':plate})
		if "Succes" in response.text:
			print("Successfully money deducted")
		else :
			print("Error in updating")
		#return 1
	else:
		print("Successfully Updated in unregistered vehicles")
		#return 0
	
