from datetime import date

def _convert_2digit_year_to_4digits_(yearString):
    '''
    Converts years expressed in 2 digits like "23" to 4 digits like "2023". 
    '''
    # take the current year's first 2 digits and add them with the last 2 digits that was given as an argument
    currentYear = str(date.today().year)
    currentYear = currentYear[0:2]
    currentYear = currentYear+ yearString
    return currentYear
    

def convert_info_to_datetime_date(dateInfoString):
    '''
    Converts a string that holds date information in these kinds of format: (all formats have to have the day, month, year in this order)
    \n230123
    \n23/03/23 23/03/2023
    \n23/3/23 23/3/2023
    \n3/3/23 3/3/2023
    \nThe returned value will be of datetime.date type
    '''
    date
    returnedDate = None
    currentYear = None

    try:
        # region === Military Date ===
        # accounting for dates like : 150123 
        if dateInfoString.isdigit() and len(dateInfoString) == 6:
            currentYear = _convert_2digit_year_to_4digits_(dateInfoString[len(dateInfoString)-2:])
            returnedDate = date(year =int(currentYear), day = int(dateInfoString[0:2]) , month= int(dateInfoString[2:4]))
            return returnedDate
        #endregion

        # region === Normal Date ===
        dateInfoString = dateInfoString.split("/")

        #if year is represented with 2 digits, convert it to 4
        if(len(dateInfoString[2]) == 2):
            currentYear = _convert_2digit_year_to_4digits_(dateInfoString[2])
        else:
            currentYear = dateInfoString[2]


        returnedDate = date(year =int(currentYear), day = int(dateInfoString[0]) , month= int(dateInfoString[1]))
        return returnedDate
        #endregion

    except:
        print("Unable to convert the text '{}' into a date".format(dateInfoString))
        return None




# print(convert_info_to_datetime_date("1/1/23"))