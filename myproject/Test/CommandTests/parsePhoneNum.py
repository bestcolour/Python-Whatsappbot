import phonenumbers

x = "+6591234567"
x = phonenumbers.parse(x, None)
x = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
print(x)