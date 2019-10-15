# SWE4S Assignment \#5: Time Series Basics

[![Build Status](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-tlfobe.svg?branch=master)](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-tlfobe)

## About

Time Series Basics - importing, cleaning, printing to csv

Note date files are synthetic data. 

Time Series Basics is a software used for compiling and printing multiple csv timeseries files into an aligned master file.

## Usage

This package consists of the `data_import.py`, which has an `ImportData` class, a `roundTimeArray` method and a `printArray` method. These three components work together to merge various time series csv files.

The `ImportData` is our how this program represents csv files internally. This class requires the path to the csv (`data_csv`) being imported, a `highlow` flag, and a `verbose` flag. Once this object is initialized, it will have a `_time` array and `_value` array containing the information from the csv file. This class has a `linear_search_value()` method, where using a `datetime.datetime()` object you can linearly search through the values in the csv file. We have also implemented a `binary_search_value()` method for faster performance! 

In order to run this program run the following lines while in the top directory of this repo:

```
insert code here!
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
