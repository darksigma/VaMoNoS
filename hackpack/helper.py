import datetime

#define a function that generates a custom user creation confirmation message
#name and zip = strings, dob = datetime.datetime object
def confirmationMsg(name, dob, zipcode):
	year = dob.year
	month = dob.month
	day = dob.day
	birthday = str(month) + "/" + str(day) + "/" + str(year) 
	return "You have successfully registered " + name + " born on " + birthday + " living in the zipcode area " + zipcode + "."

def responseFromVaccine(vaccine):
	return "You have successfully indicated that your child has received the " + vaccine.upper() + " vaccination."

def info(vacData, times): 
    statement = "You have already taken: \r\n"
    for vaccine in vacData:
        if type(vacData[vaccine]) is datetime.datetime and vaccine != "dob":
            dateTaken = str(vacData[vaccine].month) + "/" + str(vacData[vaccine].day) + "/" + str(vacData[vaccine].year)
            statement += vaccine.upper() + ": " + dateTaken + "\r\n"
    statement += "\n"
    statement += "You are due for: \r\n"
    for vaccine in times: 
        if (datetime.datetime.now() - vacData["dob"]) >= times[vaccine] and vacData[vaccine] == 0:
            statement += vaccine.upper() + ", "
    statement = statement[:-2] + "\r\n"
    return statement
