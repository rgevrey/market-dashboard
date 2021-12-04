## Utilities functions related to the extraction and cleaning of the data
## Recommended shortcut "daco"?

import os
import json
import pandas as pd
import csv
import datetime
import quandl

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
                                
def docu_dl(source="", save=False):
    """
    Downloads the available documentation and/or tickers to provide for the API
    calls needed by dldata where these are available.
    Returns a file with the tickers or display the list of options
    Leave Source empty for list of available options
    Save = "True" to save the 
    """
    available = ["ECB Data", "NASDAQ EUREX Futures"]
    
    if source == "":
        print("Documentation available on the following:")
        print(available)
        return
    
    elif source == "NASDAQ EUREX Futures":
        docu = pd.read_csv("https://static.quandl.com/Ticker+CSV%27s/Futures/EUREX.csv",encoding='latin-1')

        # The meta data added here is to help with the creation of the filename
        # The structure is predictable so it can be unwound to help with the standardisation
        meta_provider = "nasdaq"
        meta_desc = "eurex"
        meta_subdesc = "futures"
        save_name = meta_provider + "_" + meta_desc + "_" + meta_subdesc
        if save == True:
            # Let's standardise the file at this stage and see if it causes problems
            # Standardisation is simply adding identifiers (meta data) so it can be collated into one big table (the data catalogue)
            docu = docu_standardise(docu, meta_provider, meta_desc, meta_subdesc)
            save_csv(docu, save_name, "docs")
            return docu
    
    elif source == "ECB Data":
        # Nothing yet
        print("Nothing yet")
    else:
        raise ValueError("The documentation requested is not valid, check what is available")

    return docu

def save_csv(data, name, folder, mode="", debug=False):
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
    
def data_dl (dataref="", date="latest"):
    """
    Universal data download function that handles the different API calls based
    on what is being requested. Will ask for your identifiers where required.
    dataref: to provide the reference of the data to extract. The reference can be found in the datacatalogue.
    date: 'latest' will use today as reference point and pull out the latest available data
    Returns a time series.
    Leave dataref blank for dictionary of available sources. 
    """
   
    # Overall logic
    # 1. Provide datareference and dates
    #   a. If you don't know them you can retrieve a full list of what is available in the function
    #   b. But for this list you need a consolidated list of catalogues!
    # 2. The function retrieves the codes to get the data so you do not have to remember
    #   a. Retrieves the codes from files for the service requested
    #   b. If not available on the file then goes and download them from the support location
    #   c. Builds the request
    # 3. Sends the request to the API
    # 4. If the time period isn't available then the next best?
    # OUTPUT: data file downloaded

    # To do - use the data catalogue function here
    available = [
        "NASDAQ EUREX Futures"
    ]
    
    # Loads up all the available API to only have one call to the file
    api_dictionary = daco.apidict("read")
    
    # Works out the time period requested
    # There will be adjustments made to the date to match the specific requirements of the API queries
    if date == "latest":
         date = datetime.datetime.now()
    
    # Shows data sources for which API calls are set up
    # Otherwise proceeds with the downloads
    if dataref == "":
        return available

    elif dataref == "NASDAQ EUREX Futures":
        import quandl
        
        # Sets up the API based on the dictionary
        quandl.ApiConfig.api_key = api_dictionary["NASDAQ"]
        
        # Futures delivery month codes
        futures_delivery_month = {
                "January": "F",
                "February": "G",
                "March": "H",
                "April": "J",
                "May": "K",
                "June": "M",
                "July": "N",
                "August": "Q",
                "September": "U",
                "October": "V",
                "November": "X",
                "December": "Z"
        }

        # Building the query
        # To do - retrieve the code dynically via the catalogue
        query = {
            "code" : "EUREX/FVS",
            "month" : "",
            "year" : ""
        }

        # Translating the data to the futures format
        query['year'] = date.strftime('%Y')
        query['month'] = futures_delivery_month[date.strftime('%B')]
        query = query["code"] + query["month"] + query["year"]

        # Limiting to the 10 previous days
        # Converting to strings read by the API
        date_delta = datetime.timedelta(days=-10)
        start_date = date + date_delta
        start_date = start_date.strftime('%Y') + "-" + start_date.strftime('%m') + "-" + start_date.strftime('%d')
        end_date = date.strftime('%Y') + "-" + date.strftime('%m') + "-" + date.strftime('%d')

        data = quandl.get('EUREX/FVSJ2022', column_index='1',start_date=start_date, end_date=end_date)
    
    return data

