import pyperclip

prevCopyText =  pyperclip.paste()
pyperclip.copy('The text to be copied to the clipboard.')
print( pyperclip.paste())
pyperclip.copy(prevCopyText)
print (pyperclip.paste())
