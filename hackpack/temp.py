 #Automatic notification system if the child requires a new vaccine
    difference = datetime.datetime.now() - birthday
    for vaccine in vaccineTimes:
        if difference >= vaccineTimes[vaccine] and db[from_number][vaccine] == 0:
            response.sms("VaMoNoS! LET'S GO get your " + vaccine.upper() + " vaccine!")
