## Utilities functions related to the extraction and cleaning of the data
## Recommended shortcut "daco"?

import os
import json
import pandas as pd
import csv

def apidict(opmode, edit={}, debugverbose=False):
    """
    Function to write, edit and save your API key dictionary.
    Opmode:
        'edit' = arguments supplied will be added to the API dictionary
        'read' = will retrive the entire content of the API dictionary
    **args: dictionaries of {Data Service: APIKey}
    """
    
    # Builds path to API/key storage
    dicpath = os.getcwd()
    dicpath = dicpath.replace("\\src","\\apikeys.json")
    if debugverbose == True:
        print("Debug dicpath =",dicpath)
    
    # Check that there is an API dictionary otherwise creates it
    # The file will be open after this
    if os.path.isfile(dicpath) == False and opmode == "read":
        raise ValueError("There is no apikeys.json file. Create it with opmode = edit")
    elif os.path.isfile(dicpath) == False and opmode == "edit":
            dic = {}
            dicfile = open(dicpath, "x")
            json.dump(dic, dicfile)
            dicfile.close()
      
    # If there's an API dictionary, then the retrieval/update can take place 
    # Retrieval process
    if opmode == "read":
        dic = pd.read_json(dicpath,typ="series")
        dic = dic.to_dict()
        return dic
    
    # Update/addition process
    if opmode == "edit" and len(edit) > 0:
        
        # Reading the content of JSON and saving as dictionary
        dic = pd.read_json(dicpath,typ="series")
        if debugverbose == True:
            print("Debug dic content",dic)
        dic = dic.to_dict()
        if debugverbose == True:
            print("Debug editing dic", type(dic))
        
        # Edit the dictionary
        dic.update(edit)
        if debugverbose == True:
            print("Debug changes to dic", dic)
        
        # Writes the new dictionary to the file
        dicfile = open(dicpath, "w")
        json.dump(dic, dicfile)
        dicfile.close()
        return
    
    elif opmode == "edit" and len(edit) == 0:
        raise ValueError("You want to edit but did not provide a dictionary.")
        return
                                
def dldocu(source="", save=False):
    """
    Downloads the available documentation and/or tickers to provide for the API
    calls needed by dldata where these are available.
    Returns a file with the tickers or display the list of options
    Leave Source empty for list of available options
    Save = "True" to save the 
    """
    available = ["NASDAQ EUREX Futures"]
    
    if source == "":
        print("Documentation available on the following:")
        print(available)
        return
    elif source == "NASDAQ EUREX Futures":
        docu = pd.read_csv("https://static.quandl.com/Ticker+CSV%27s/Futures/EUREX.csv",encoding='latin-1')
        if save == True:
            
    else:
        raise ValueError("The documentation requested is not valid, check what is available")

    return docu

def savecsv(data, name, folder, mode="", debug=False):
    """
    Saves a dataframe to the requested folder
    data: dataframe to be saved
    name: name of the file to be created
    mode: this is to decide what to do if the file already exists
        overwrite: 
        append: 
        update:
    location: folder where the file is to be created
    debug: triggers verbose for troubleshooting
    """
    
    # Builds path and file name
    path = os.getcwd()
    path = path.replace("\\src","\\" + folder + "\\" + name + ".csv")
    path = path.replace("\\","\\\\")
    if debug == True:
        print("path:", path)
        
    # Saving to CSV!
    data.to_csv(path)
    
    return
    
    