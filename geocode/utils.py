import os
from os.path import sep, join
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def tag_timestamp(filename):
    filename_split = filename.split('.')
    timestamp = datetime.strftime(datetime.now(), '_%Y_%m_%d_%H%M%S%f')
    tagged_filename = ".".join(filename_split[:-1]) + timestamp + '.' + filename_split[-1]
    return tagged_filename

def get_absolute_file_path(*args):
    return join(CURRENT_DIR, *args).replace(sep, '/')

def create_file_on_disk(folder, tagged_filename, file_obj, input_source):
    """
    Creates an excel file on disk
    """
    filepath = get_absolute_file_path(folder, tagged_filename)

    if input_source == "request":
        with open(filepath, 'wb') as dest:
            for chunk in file_obj.chunks():
                dest.write(chunk)
    elif input_source == "dataframe":
        file_obj.to_excel(filepath, index=False)

    return filepath
