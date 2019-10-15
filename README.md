# SWE4S Assignment \#5: Time Series Basics

[![Build Status](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-tlfobe.svg?branch=master)](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-tlfobe)

## About

Time Series Basics - importing, cleaning, printing to csv

Note date files are synthetic data. 

Time Series Basics is a software used for compiling and printing multiple csv timeseries files into an aligned master file.

## Usage

This package consists of the `data_import.py`, which has an `ImportData` class, a `roundTimeArray` method and a `printArray` method. These three components work together to merge various time series csv files.

The `ImportData` is our how this program represents csv files internally. This class requires the path to the csv (`data_csv`) being imported, a `highlow` flag, and a `verbose` flag. Once this object is initialized, it will have a `_time` array and `_value` array containing the information from the csv file. This class has a `linear_search_value()` method, where using a `datetime.datetime()` object you can linearly search through the values in the csv file. We have also implemented a `binary_search_value()` method for faster performance!

The `roundTimeArray` function  takes in an `ImportData` object (`in_obj`), a desired resolution in minutes (`res`), and optional inputs like, what kind of `operation` will be used to reconsile matching time values, whether or not to `modify` the `in_obj` and what kind of `search_type` the method will use to produce new rounded time series. The output of this method is a `zip` object which contains the new time series as a set of parrallel arrays.

The `printArray` function is another crucial function in the operation of this program. This function takes in a `data_list`, an `annotation_list`, a `base_name` and a `key_file`. The `data_list` should be a list of of `zip` objects. The `annotation_list` should be a list of file names from which the `zip` objects should of come from. The `base_name` input is a `string` denoting the file to write to. The `key_file` is also a `string` that designates which `annoation_list` value to align the data on.

In order to run this program run the following lines while in the top directory of this repo:

```
python data_import.py --folder_name [desired-folder] --output_file [desired-output] --sort_key [desired-key]
```

An example is setup below with the `smallData` folder in this repo:
```
python data_import.py --folder_name smallData --output_file data_out --sort_key cgm_small
```

## Installation

Time Series Basics depends on a few packages, ensure that these are installed before trying to run this program:
- pycodestyle
- python-dateutil
- numpy

These can be installed with the following code snippet:
```
conda config --add channels r
conda install -y pycodestyle
conda install -y python-dateutil
conda install --yes numpy
```
