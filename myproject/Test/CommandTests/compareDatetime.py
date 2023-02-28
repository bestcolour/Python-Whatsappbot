# Simple Python program to compare dates

# importing datetime module
import datetime

# date in yyyy/mm/dd format
d1 = datetime.datetime(2018, 6, 1,23,50)
d2 = datetime.datetime(2018, 6, 1,23,50)

# Comparing the dates will return
# either True or False
print("{}".format(d1) )
print("d1 is greater than d2 : ", d1 > d2)
print("d1 is less than d2 : ", d1 < d2)
print("d1 is not equal to d2 : ", d1 != d2)
