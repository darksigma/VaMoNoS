import datetime

#define a function that generates a custom user creation confirmation message
#name and zip = strings, dob = datetime.datetime object
def confirmationMsg(name, dob, zipcode):
	year = dob.year
	month = dob.month
	day = dob.day
	birthday = str(month) + "/" + str(day) + "/" + str(year) 
	return "You have successfully registered " + name + " born on " + birthday + " living in the zipcode area " + zipcode + "."
