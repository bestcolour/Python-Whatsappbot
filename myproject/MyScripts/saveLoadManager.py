import settings
import json

def save_to_data_file(jsonString):
    '''
    \nWrites to a json string to a json file.
    '''
    with open (settings.PATH_DATA_JSON,"w") as outfile:
        outfile.write(jsonString)

def read_from_data_file():
    '''
    \nReads from the data json file returns the json data (loaded) as string
    '''
    try:
        with open (settings.PATH_DATA_JSON) as jsonFile:
            return json.load(jsonFile)
    except:
        return None
