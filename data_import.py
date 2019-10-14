import csv
import dateutil.parser
import copy
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import numpy as np


class ImportData:
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
    __init__(self, data_csv, highlow, verbose)
        constructor method for ImportData
    linear_search_value(key_time)
        linearly search for value given a datetime key
    binary_search_value(key_time)
        binary search for value given a datetime key
    """
    # open file, create a reader from csv.DictReader,
    # and read input times and values

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
                        "ImportData: the file provided does" +
                        "not have columns for time or value")
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
        performs a linear search on the time array
        and returns the corresponding value

        Arguments
        ---------
        key_time : datetime.datetime
            a datetime object used to denote the time/date of
            a measurement was taken

        Returns
        -------
        hit_list : array of values corresponding to the specific date/time
        """
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        if not isinstance(key_time, datetime.datetime):
            raise TypeError(
                "ImportData.linear_search_value : this function only " +
                "supports datetime.datetime inputs")
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
    """
    a function which aligns data sets based on datetime objects

    Arguments
    ---------
    data_list : list of zip objects
        list of zipped (date, value) pairs. see output of roundTimeArray
    annotation_list : list of strings
        list of strings with column labes for data value
    base_name : str
        name of file to output to
    key_file : str
        name from annotation list to align data on
    """
    # Exception raising

    if not isinstance(data_list, list):
        raise TypeError("printArray: data_list in must be a list type!")
    if not isinstance(annotation_list, list):
        raise TypeError("printArray: annotation_list in must be a list type!")
    if not isinstance(base_name, str):
        raise TypeError("printArray: base_name in must be a string type!")
    if not isinstance(key_file, str):
        raise TypeError("printArray: key_file in must be a string type!")

    type_data_list = [not isinstance(data, zip) for data in data_list]
    print(type_data_list)
    type_ann_list = [not isinstance(ann, str) for ann in annotation_list]
    if any(type_data_list):
        raise IndexError(
            "printArray: a value in data_list was not a zip type!")
    if any(type_ann_list):
        raise IndexError(
            "printArray: a value in annotation_list was not a string type!")
    if key_file not in annotation_list:
        raise IndexError("printArray: key_file is not in annotation_list!")

    # combine and print on the key_file

    base_data = []
    key_index = 0
    data_list = [list(zip_obj) for zip_obj in data_list]
    for i in range(len(annotation_list)):
        if annotation_list[i] == key_file:
            base_data = data_list[i]
            key_index = i
            break
        if i == len(annotation_list)-1:
            print("Key not found ")
    if '.csv'not in base_name:
        base_name = base_name+'.csv'

    with open(base_name, 'w') as f:
        f.write('time,')
        f.write(annotation_list[key_index].split('_')[0]+',')
        non_key = list(range(len(annotation_list)))
        non_key.remove(key_index)

        for index in non_key:
            f.write(annotation_list[index].split('_')[0]+',')
        f.write('\n')

        for time, value in base_data:
            f.write(str(time)+','+str(value)+',')
            for n in non_key:
                t_list = [pair[0] for pair in data_list[n]]
                if time in t_list:
                    f.write(str(data_list[n][t_list.index(time)][1])+',')
                else:
                    f.write('0,')
            f.write('\n')


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description='A class to import,' +
                                     ' combine, and print data from a folder.',
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
