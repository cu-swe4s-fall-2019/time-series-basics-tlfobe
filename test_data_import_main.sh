#!/bin/bash
test -e ssshtest ||  wget -q http://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

# Testing PEP8 style
run test_data_import_style pycodestyle data_import.py
assert_exit_code 0
assert_no_stdout

run test_test_data_import_style pycodestyle test_data_import.py
assert_exit_code 0
assert_no_stdout

# Test csv write out
run test_data_import_normal python data_import.py --folder_name smallData --output_file data_out --sort_key cgm_small
assert_exit_code 0
assert_no_stdout

run test_csv_out cat data_out_5.csv
assert_in_stdout 2018-03-16 00:05:00,151