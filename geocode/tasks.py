import os
import geocoder
import pandas as pd

from .exceptions import *

##########################################
############ static variables ############
##########################################

# Getting the account API Key from system’s environment variables.
MAPQUEST_API_KEY = os.environ.get("MAPQUEST_API_KEY")


##########################################
########## Function definitions ##########
##########################################

def validate_input_file_and_get_df(xl):
    sheet_names = xl.sheet_names
    if len(sheet_names) > 1:
        raise ValidationError("number of sheets", "is more than 1")
    if sheet_names[0] != "custom_sheet_name":
        raise ValidationError("sheet name", "is not 'custom_sheet_name'")
    """
    Any other validations
    ...
    ...

    """
    df = pd.read_excel(xl, "custom_sheet_name")
    return df

def add_geocodes(df):
    # Lists to store the latitude and longitude values
    lat_list = []
    lng_list = []

    input_addresses_list = list(df["Address"])
    n = len(input_addresses_list)

    # Handling the batch limit of 100 locations at a time, in MAPQUEST Geocoding API
    batch_count = 0
    while True:
        # Condition to break out of the infinite while loop
        if batch_count*100 >= n:
            break
        batch_count += 1

        g = geocoder.mapquest(input_addresses_list[(batch_count-1)*100:batch_count*100], method='batch', key=MAPQUEST_API_KEY)

        for result in g:
            lat_list.append(result.lat)
            lng_list.append(result.lng)

    # Add the extracted information to the dataframe
    df["Latitude"] = lat_list
    df["Longitude"] = lng_list
