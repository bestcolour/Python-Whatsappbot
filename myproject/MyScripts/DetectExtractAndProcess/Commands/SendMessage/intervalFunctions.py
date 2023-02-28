import datetime

class interval():

    def __init__(self,day =0,hour=0,minute=0):
        self.day = day
        self.hour= hour
        self.minute= minute

    def recalculate_values(self):

        a = int(self.minute/60) # excess minutes convert to hours
        self.hour += a
        a = int(self.minute % 60) # set remainder minutes 
        self.minute = a
        
        a = int(self.hour/24) # excess hours convert to days
        self.day += a
        a = int(self.hour % 24) # set remainder hours 
        self.hour = a
        
    def __str__(self):
        return "{day} days {hour} hours {minute} minutes".format(day= self.day,hour = self.hour, minute = self.minute)
    
    

def convert_info_to_interval(timeInfoString):
    '''
    Converts a interal string of these formats: 
    \n2d 2h 4m 
    \ninto datetime.datetime type
    '''
    try:
        splitString = timeInfoString.split()
        unit = length = 0
        finalInterval = interval()

        for i in range(len(splitString)):
            length = len(splitString[i])
            unit = splitString[i][length-1:] # get the unit as in days , hours or minutes
            length = int(splitString[i][0:length-1])  # get the digits
            match unit:
                case 'd':
                    finalInterval.day += length
                    continue
                case 'h':
                    finalInterval.hour += length
                    continue
                case 'm':
                    finalInterval.minute += length
                    continue

        finalInterval.recalculate_values()

        return finalInterval

    except:
        print("Unable to convert the inputed interval '{}' into datetime.time type".format(
            timeInfoString))
        return None


# print(convert_info_to_interval("1d 72h 60m"))