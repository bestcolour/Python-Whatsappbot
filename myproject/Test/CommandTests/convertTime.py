import datetime


def convert_time(timeInfoString):
    '''
    Converts a time string of these formats: 
    \n12am 9am
    \n12.00am 9.30am
    \n0100 2359
    \ninto datetime.time type
    '''
    length = len (timeInfoString)

    try:

        if timeInfoString.isdigit() and length ==4:
            return datetime.time(
                hour= int(timeInfoString[0:2]),
                minute= int(timeInfoString[2:4])
            )

        ampm_string = timeInfoString[length-2:] #get am/pm string
        timeInfoString = timeInfoString[0:length-2] #remove am/pm string
        timeInfoString = timeInfoString.split('.') #returns list that looks smth like this: ["10","30"]

        # for cases when timeInfo is "12pm"
        if(len(timeInfoString) ==1):
            timeInfoString.append("00")

        match ampm_string[0]:
            # if time is in am
            case 'a':
                # 12am means 00 hrs
                if(timeInfoString[0] == "12"):
                    return datetime.time(
                        hour= 0,
                        minute= int(timeInfoString[1])
                        )

                return datetime.time(hour= int(timeInfoString[0]),minute= int(timeInfoString[1]))
            
            case 'p':
                return datetime.time(hour= int(timeInfoString[0]),minute= int(timeInfoString[1]))
        pass

    except:
        print("Unable to convert the inputed time '{}' into datetime.time type".format(timeInfoString))
        return None




print(convert_time("11.30am"))