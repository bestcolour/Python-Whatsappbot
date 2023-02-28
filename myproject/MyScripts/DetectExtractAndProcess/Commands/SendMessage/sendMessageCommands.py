'''
\nFiles that contains the send message bot command.
\nThe keywords for inputing information about the message to be sent are also defined here.
'''
from ..baseBotCommand import baseBotCmd
import datetime
from .timeFunctions import convert_to_datetime_time as convert_time
from .dateFunctions import convert_info_to_datetime_date as convert_date
from .intervalFunctions import convert_info_to_interval as convert_interval, interval
from .commonFunctions import extract_keyword_info, extract_keyword_info_with_spaces
from ...clickerFunctions import type_and_send_convo_input, enter_group_chat, return_to_default_group, start_convo_with_new_num
import settings
import pytz
import time
import phonenumbers

# region === Key Words ===
TIME_KEYWORD = "at"
DATE_KEYWORD = "on"
INTERVAL_KEYWORD = "every"
MSG_KEYWORD = "msg:"
TO_KEYWORD = "to"

keywords = {
    TIME_KEYWORD, DATE_KEYWORD, INTERVAL_KEYWORD, MSG_KEYWORD,TO_KEYWORD
}
# endregion


class sendMessageToGroup(baseBotCmd):
    '''
    \nThe command class that sends a message to the current whatsapp group focused at a certain time, date and interval.
    \nself.dueDate = The date and time in which the message ought to be sent.
    \nself.UTC_dueDate = The UTC version of date and time in which the message ought to be sent.
    \nself.repeatInterval = The interval in which the message will be sent.
    \nself.messageToSend = The string that is behind the MSG_KEYWORD
    '''

    def __init__(self, groupChatName, msg, loadedJsonData=None, isLoadingFromJSON=False):
        '''
        \nReads the message and extracts certain keywords and their respective information to set this class's values to.
        \n
        '''
        super().__init__(groupChatName, msg, loadedJsonData, isLoadingFromJSON)
        self.isInstant = False
        self.failedNumberOfTimes = 0

        if not isLoadingFromJSON:
            # region === Not Loading From JSON ===
            # I need to split everything in the string until the start of message msg
            startOfMsg = msg.index(MSG_KEYWORD)
            # split message now contains everything except for the msg keyword and the string beyond that
            splitMsg = msg[0:startOfMsg]
            splitMsg = splitMsg.split()

            # region --- Message ---
            try:
                # remove the msg keyword
                self.messageToSend =  msg[startOfMsg + len(MSG_KEYWORD):]
                '''
                \nThe string that is behind the MSG_KEYWORD
                '''
                self.messageToSend = self.messageToSend.strip()
            except:
                print("Message to send must be inputed!")
                raise ValueError("Message to send must be inputed!")
            # endregion

           

            #region --- GroupChat Name ---
            # this code here allows the bot to send messages to other groups apart from the one it is in
            # it also allows users to send messages to phone numbers
            try:
                # ONLY ADMINS CAN HAVE THIS FEATURE AND TO USE IT, IT MUST BE TEXTED PRIVATELY TO THE BOT
                # the feature of sending to other groups and phonenumbers
                try:
                    # if the person privately messaging the bot is in the admin list, then allow the code to flow
                    # this is because the group chat name will be the person's phone number when the bot reads the message
                    settings.get("ADMIN_NUMBERS").index(groupChatName)
                except ValueError:
                    print("The name/number: '{}' is not on the admin list!.".format(groupChatName))
                    raise Exception

                #region ___ Extracting 'to' Keyword ___
                # the msg and split msg var here has everything past the msgkeyword removed
                # this is to make the extract_keyword_info_with_spaces work
                # if you require the raw msg, use self.msg instead
                msg = msg[0:startOfMsg] 

                # try to get the groupchat name/number first by seeing if there is any "to" keyword
                x = extract_keyword_info_with_spaces(msg,splitMsg,keywords,TO_KEYWORD)
                self.groupChatName = x.strip() # remove leading and trailing whitespace

                # try parse the groupname into a phonenumber to format it
                try:
                    x = self.groupChatName 
                    x = phonenumbers.parse(x, None)
                    x = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                    self.groupChatName = x
                except:
                    print("Unable to parse the phone number: '{}'".format(self.groupChatName))
                    pass
                    #endregion

            except:
                # if there is no "to" keyword in the msg, get current groupchat message
                self.groupChatName = groupChatName
            #endregion

            # region --- Time ---
            try:
                time = extract_keyword_info(splitMsg, keywords, TIME_KEYWORD)
                # self time will be like this "['somenumber','am']" so we need to join it
                time = "".join(time)
                time = convert_time(time)
                # print("Time: {}".format(time))
            except:  # if no time was given, it prolly means the msg needs to be sent immediately
                time = datetime.datetime.now()
                time = datetime.time(hour=time.hour, minute=time.minute)

            # endregion

            # region --- Date ---
            try:
                # self time will be like this "['somenumber','am']" so we need to join it
                date = "".join(extract_keyword_info(
                    splitMsg, keywords, DATE_KEYWORD))
                date = convert_date(date)
            except:  # if no date was given, it prolly means the msg needs to be sent today
                now = datetime.datetime.now()
                date = datetime.date(
                    year=now.year, month=now.month, day=now.day)
            # endregion

            #region --- DateTime ---
            # create a time  aware datetime in MY TIMEZONE
            self.dueDate = datetime.datetime(
                year=date.year, month=date.month, day=date.day, hour=time.hour, minute=time.minute, tzinfo=settings.TIMEZONE)
            '''
            \nThe date and time in which the message ought to be sent.
            '''
            # then, convert it to utc time zone for comparisons in the update func
            self.UTC_dueDate = self.dueDate.replace(tzinfo=pytz.UTC)
            '''
            \nThe UTC version of date and time in which the message ought to be sent.
            '''
            #endregion

            # region --- Repeat Interval ---
            try:
                self.repeatInterval = " ".join(extract_keyword_info(
                    splitMsg, keywords, INTERVAL_KEYWORD))
                '''
                \nThe interval in which the message will be sent.
                '''
                self.repeatInterval = convert_interval(self.repeatInterval)
            except:
                self.repeatInterval = None
            # endregion

           

            print("\n--- Send Grp Cmd Overview ---\ndatetime: '{}'\nGroupchat Name: '{}'\ninterval: '{}'\nmessage: '{}'".format(
                self.dueDate.strftime("%m/%d/%Y, %H:%M"),self.groupChatName, self.repeatInterval, self.messageToSend))
            # endregion
        else:
            # region === Loading From JSON ===
            self.groupChatName = loadedJsonData["groupChatName"]
            self.msg = loadedJsonData["msg"]
            self.id = loadedJsonData["id"]
            self.dueDate = datetime.datetime(
                year=loadedJsonData["dueDate"]["year"],
                month=loadedJsonData["dueDate"]["month"],
                day=loadedJsonData["dueDate"]["day"],
                hour=loadedJsonData["dueDate"]["hour"],
                minute=loadedJsonData["dueDate"]["minute"],
                tzinfo=settings.TIMEZONE
            )
            # then, convert it to utc time zone for comparisons in the update func
            self.UTC_dueDate = self.dueDate.replace(tzinfo=pytz.UTC)

            if loadedJsonData["repeatInterval"] is None:
                self.repeatInterval = None
            else: 
                self.repeatInterval = interval(
                    day=loadedJsonData["repeatInterval"]["day"],
                    hour=loadedJsonData["repeatInterval"]["hour"],
                    minute=loadedJsonData["repeatInterval"]["minute"]
                )
            self.messageToSend = loadedJsonData["messageToSend"]
            # endregion
            pass

    def save_as_dictionary(self):
        '''
        \nThis method is called to convert the data needed to instantiate this class into a json format. Returns a dictionary of all the data needed.
        '''

        x = {
            "groupChatName": self.groupChatName,
            "msg": self.msg,
            "id": self.id,
            "dueDate": {
                "year": self.dueDate.year,
                "month": self.dueDate.month,
                "day": self.dueDate.day,
                "hour": self.dueDate.hour,
                "minute": self.dueDate.minute
            },
            "messageToSend": self.messageToSend
        }

        if self.repeatInterval is None:
            x["repeatInterval"] = None
        else:
            x["repeatInterval"] = {
                "day": self.repeatInterval.day,
                "hour": self.repeatInterval.hour,
                "minute": self.repeatInterval.minute,
            }

        return x

    def update(self):
        '''
        \nThis method is called to update the command instance within an update loop.
        '''
        # make 'now' timeaware with my timezone before converting it to utc timezone
        now = datetime.datetime.now(settings.TIMEZONE)
        # this needs to be called because of how datetimes with the same timezones can give different utc offsets which results in inaccurate comparisons of datetimes. UTC time zone is always +00:00 so it's best to use it for comparisons
        nowUTC = now.replace(tzinfo=pytz.UTC)

        # print("Timenow: {}".format(now))
        # print(" self.UTC_datetime: {}".format( self.UTC_datetime))
        # print("now <  self.UTC_datetime {}".format(now <   self.UTC_datetime))

        if nowUTC < self.UTC_dueDate:
            return False

        self.finish()
        if (self.repeatInterval != None):
            # set new datetime using the interval
            add = datetime.timedelta(
                days=self.repeatInterval.day, hours=self.repeatInterval.hour, minutes=self.repeatInterval.minute)
            self.dueDate = now + add
            self.UTC_dueDate = nowUTC + add
            print("New Datetime for '{}':\n{}".format(
                self.messageToSend, self.dueDate.strftime("%m/%d/%Y, %H:%M")))
            return False

        return True

    def finish(self):
        try:
            enter_group_chat(self.groupChatName)
            type_and_send_convo_input(self.messageToSend)
        except ValueError:
            # that means that the groupchatname is likely a new number to start a chat with and will need to send message to the number with the  wae.method
            #but first we check if it is a number
            if self.groupChatName[0] != '+':
                raise ValueError

            # open new tab etc and go to start a conversation with that number without the '+'
            editedPhoneNum = self.groupChatName[1:]
            editedPhoneNum = editedPhoneNum.replace(" ","")
            start_convo_with_new_num(editedPhoneNum)
            time.sleep(settings.get("MSG_NEW_NUMBER_PAUSE"))
            type_and_send_convo_input(self.messageToSend)
        except AssertionError:
            # if something was to happen (like unable to find a group)
            self.failedNumberOfTimes+=1

            # if max number of try attempts has been reached, dont raise any exception and consider the command done
            if self.failedNumberOfTimes < settings.get("MAX_NUM_OF_TRIES_B4_CMD_REMOVES_ITSELF"):
                raise Exception
        finally:
            return_to_default_group()

