'''
\nHolds bot events such as:
- on message processed done
'''


from events import Events

# This is the event that will be subscribed by the message extraction thread to be notified that the program has entered a whatsapp group after cliking it
_event_holders = Events(("OnMessageProcessingDone")) 

# This is the event that will be subscribed by the message extraction thread to be notified that there is new message(s) in the current group chat that it is extracting messages from
def raise_on_msg_processed_done(cmdTasks):
    global _event_holders
    _event_holders.OnMessageProcessingDone(cmdTasks)

def sub_to_on_msg_processed_done(func):
    global _event_holders
    _event_holders.OnMessageProcessingDone +=func

def unsub_from_msg_processed_done(func):
    global _event_holders
    _event_holders.OnMessageProcessingDone -=func