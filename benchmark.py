import time
import data_import
import argparse
import os
import sys


if __name__ == "__main__":

    # adding arguments
    parser = argparse.ArgumentParser(description='A class to import,' +
                                     ' combine, and print data from a folder.',
                                     prog='dataImport')

    parser.add_argument('--folder_name', type=str, help='Name of the folder', required=True)

    parser.add_argument('--output_file', type=str, help='Name of Output file', required=True)

    parser.add_argument('--sort_key', type=str, help='File to sort on', required=True)

    args = parser.parse_args()

    if '.csv' in args.output_file:
        args.output_file = args.output_file.split('.csv')[0]

    # pull all the folders in the file

    files_lst = []  # list the folders
    try:
        csv_files = os.listdir(args.folder_name)
    except FileNotFoundError:
        print("folder_name provided was not found!", file=sys.stderr)
        sys.exit(1)
    for csv_file in csv_files:
        files_lst.append(os.path.join(args.folder_name, csv_file))

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    for file_name in files_lst:
        if 'cgm' in file_name:
            data_lst.append(data_import.ImportData(file_name, highlow=True))
        else:
            data_lst.append(data_import.ImportData(file_name))

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst

    data_5 = []  # a list with time rounded to 5min
    data_15 = []  # a list with time rounded to 15min

    # Linear Search (linear search is default)

    t1 = time.time()
    for data_import_obj in data_lst:
        sum_key = [
            add_file in data_import_obj._file_name for add_file in
            ['activity, bolus, meal']
        ]
        if any(sum_key):
            data_5.append(data_import.roundTimeArray(
                data_import_obj, 5, operation='add'))
        else:
            data_5.append(data_import.roundTimeArray(data_import_obj, 5))
    try:
        data_import.printArray(
            data_5, files_lst, args.output_file+'_5.csv', args.sort_key)
    except IndexError:
        print("sort_key provided was did not apply to the files in " +
              args.folder_name, file=sys.stderr)
        sys.exit(1)

    t2 = time.time()

    for data_import_obj in data_lst:
        sum_key = [
            add_file in data_import_obj._file_name for add_file in
            ['activity, bolus, meal']
        ]
        if any(sum_key):
            data_15.append(data_import.roundTimeArray(
                data_import_obj, 15, operation='add'))
        else:
            data_15.append(data_import.roundTimeArray(data_import_obj, 15))
    try:
        data_import.printArray(data_15, files_lst, args.output_file +
                               '_15.csv', args.sort_key)
    except IndexError:
        print("sort_key provided did not apply to the files in " +
              args.folder_name, file=sys.stderr)
        sys.exit(1)

    t3 = time.time()

    # reinitialize arrays

    data_5 = []  # a list with time rounded to 5min
    data_15 = []  # a list with time rounded to 15min

    t4 = time.time()
    for data_import_obj in data_lst:
        sum_key = [
            add_file in data_import_obj._file_name for add_file in
            ['activity, bolus, meal']
        ]
        if any(sum_key):
            data_5.append(data_import.roundTimeArray(
                data_import_obj, 5, operation='add', search_type="binary"))
        else:
            data_5.append(data_import.roundTimeArray(
                data_import_obj, 5, search_type="binary"))
    try:
        data_import.printArray(
            data_5, files_lst, args.output_file+'_5.csv', args.sort_key)
    except IndexError:
        print("sort_key provided was did not apply to the files in " +
              args.folder_name, file=sys.stderr)
        sys.exit(1)

    t5 = time.time()

    for data_import_obj in data_lst:
        sum_key = [
            add_file in data_import_obj._file_name for add_file in
            ['activity, bolus, meal']
        ]
        if any(sum_key):
            data_15.append(data_import.roundTimeArray(
                data_import_obj, 15, operation='add', search_type="binary"))
        else:
            data_15.append(data_import.roundTimeArray(
                data_import_obj, 15, search_type="binary"))
    try:
        data_import.printArray(data_15, files_lst, args.output_file +
                               '_15.csv', args.sort_key)
    except IndexError:
        print("sort_key provided did not apply to the files in " +
              args.folder_name, file=sys.stderr)
        sys.exit(1)
    t6 = time.time()

    print("time for data_out_5 linear search:", t2 - t1)
    print("time for data_out_15 linear search:", t3 - t2)
    print("time for data_out_5 binary search:", t5 - t4)
    print("time for data_out_15 binary search:", t6 - t5)
