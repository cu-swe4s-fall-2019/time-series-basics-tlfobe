import csv
import dateutil.parser
import copy
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import numpy as np


class ImportData:
    # open file, create a reader from csv.DictReader, and read input times and values
    """
    Class used for representing csv time series data

    Attributes
    ----------
    _time : array
        array of time values from csv used to generate object
    _value : array
        array of values from csv used to generate object

    Methods
    -------

    """

    def __init__(self, data_csv, highlow=False, verbose=False):
        """
        constructor method for ImportData

        Arguments
        ---------
        data_csv : string
            name of csv file to be read in
        highlow : bool
            a flag used for checking to replace high/low values with 300/40
        verbise : bool
            a flag used for outputting various error output
        """
        if not isinstance(data_csv, str):
            raise TypeError("ImportData:", str(data_csv), "is not a string!")
        if not isfile(data_csv):
            raise FileNotFoundError(
                "ImportData:", data_csv, "is not a valid file!")
        self._time = []
        self._value = []

        with open(data_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'time' not in row.keys() or 'value' not in row.keys():
                    raise KeyError(
                        "ImportData: the file provided does not have columns for time or value")
                if row['value'] == '' or row['time'] == '':
                    continue
                else:
                    try:
                        self._time.append(dateutil.parser.parse(row['time']))
                    except ValueError:
                        if verbose:
                            print('Bad input format for time')
                            print(row['time'])
                    if highlow:
                        if row['value'] == 'high':
                            self._value.append(300.0)
                            print('Changed high entry to 300 at', row['time'])
                            continue
                        if row['value'] == 'low':
                            self._value.append(40.0)
                            print('Changed low entry to 40 at', row['time'])
                            continue
                    self._value.append(float(row['value']))
            f.close()

    def linear_search_value(self, key_time):
        """
        performs a linear search on the time array and returns the corresponding value

        Arguments
        ---------
        key_time : datetime.datetime
            a datetime object used to denote the time/date an measurement was taken

        Returns
        -------
        hit_list : array of values corresponding to the specific date/time
        """
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        if not isinstance(key_time, datetime.datetime):
            raise TypeError(
                "ImportData.linear_search_value : this function only supports datetime.datetime inputs")
        hit_list = []
        for i in range(len(self._time)):
            if key_time == self._time[i]:
                hit_list.append(self._value[i])
        if len(hit_list) == 0:
            print("Time Value not in csv")
            return(-1)
        else:
            return(hit_list)

    def binary_search_value(self, key_time):
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        pass


def roundTimeArray(in_obj, res, operation='average', modify=False):
    """
    used to reformat time and value array of an ImportData object

    Arguments
    ---------
    in_obj : ImportData
        an instance of an ImportData object that whos data will be transformed
    res : int
        resolution in minutes of the new transformed data
    operation : string
        how value data will be reconsiled for multiple times
    modify : bool
        whether this function changes the original ImportData object

    Returns
    -------
    zip_obj : zip
        a zip object containing parallel arrays of new times and values

    """
    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned
    if modify:
        obj = in_obj
    else:
        obj = copy.deepcopy(in_obj)

    if not isinstance(obj, ImportData):
        raise TypeError(
            "roundTimeArray: in_obj was not of the class ImportData!")
    if not isinstance(res, int):
        raise TypeError("roundTimeArray: res was not an int!")
    if not isinstance(operation, str):
        raise TypeError("roundTimeArray: operation was not a string!")
    if not isinstance(modify, bool):
        raise TypeError("roundTimeArray: modify must be a bool!")
    if not operation == "average" and not operation == "sum":
        raise NotImplementedError(
            "roundTimeArray: "+operation+" not implemented!")
    new_values = []
    new_times = []
    for time in obj._time:
        minminus = datetime.timedelta(minutes=(time.minute % res))
        minplus = datetime.timedelta(minutes=res) - minminus
        if (time.minute % res) <= res/2:
            newtime = time - minminus
        else:
            newtime = time + minplus
        new_times.append(newtime)
    obj._time = new_times
    unique_times = []
    for new_time in new_times:
        if new_time not in unique_times:
            if operation == 'average':
                new_value = np.average(obj.linear_search_value(new_time))
            if operation == 'sum':
                new_value = np.sum(obj.linear_search_value(new_time))
            new_values.append(new_value)
            unique_times.append(new_time)
        else:
            continue

    obj._time = unique_times
    obj._value = new_values
    return(zip(obj._time, obj._value))


def printArray(data_list, annotation_list, base_name, key_file):
    # combine and print on the key_file
    pass


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description='A class to import, combine, and print data from a folder.',
                                     prog='dataImport')

    parser.add_argument('folder_name', type=str, help='Name of the folder')

    parser.add_argument('output_file', type=str, help='Name of Output file')

    parser.add_argument('sort_key', type=str, help='File to sort on')

    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()

    # pull all the folders in the file
    files_lst = []  # list the folders

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = []  # a list with time rounded to 5min
    data_15 = []  # a list with time rounded to 15min

    # print to a csv file
    printLargeArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    printLargeArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
