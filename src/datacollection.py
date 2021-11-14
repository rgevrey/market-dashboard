## Utilities functions related to the extraction and cleaning of the data
## Recommended shortcut "daco"?


def apidict(opmode, edit={}, debugverbose=False):
    """
    Function to write, edit and save your API key dictionary.
    Opmode:
        'edit' = arguments supplied will be added to the API dictionary
        'read' = will retrive the entire content of the API dictionary
    **args: dictionaries of {Data Service: APIKey}
    """
    import os
    import json
    import pandas as pd
    
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
                                
