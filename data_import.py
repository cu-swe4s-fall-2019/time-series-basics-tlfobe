import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime


class ImportData:
    # open file, create a reader from csv.DictReader, and read input times and values

    def __init__(self, data_csv, highlow=False, verbose=False):
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
                            continue
                        if row['value'] == 'low':
                            self._value.append(40.0)
                            continue
                    self._value.append(float(row['value']))
            f.close()

    def linear_search_value(self, key_time):
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        for i in range(len(self._time)):
            if key_time == self._time[i]:
                return(self._value[i])
        print("Time Value not in csv")
        return(-1)

    def binary_search_value(self, key_time):
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        pass


def roundTimeArray(obj, res):
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
    pass


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
