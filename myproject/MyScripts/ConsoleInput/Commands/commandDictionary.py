from .consoldeCommands import exit_program , refresh_driver, remove_command, print_help, save_on_going_commands ,clear_console,sendmsg,change_settings
from MyScripts.Background.backgroundThread import print_on_going_commands

# Dictionary key = Command Keyword
# Dictionary Value = (Argument,function)
command_Dictionary = {
    "help":  print_help ,
    "print og":print_on_going_commands,
    "exit": exit_program,
    "refresh" :refresh_driver,
    "remove og" : remove_command,
    "save og" : save_on_going_commands,
    "clear": clear_console,
    "send": sendmsg,
    "settings" : change_settings
}
'''
Stores the available console commands in a dictionary for easy access from the input manager.
'''