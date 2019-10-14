import unittest
import data_import
import numpy as np
import os


class TestImportData(unittest.TestCase):
    def setUp(self):
        with open('testfile.csv', 'w') as f:
            f.write('Id,time,value\n')
            for i in range(1000):
                f.write(str(10)+(","+str(10))*2+'\n')

        with open('rand_testfile.csv', 'w') as f:
            f.write('Id,time,value\n')
            for i in range(1000):
                f.write(",".join([str(a)
                                  for a in np.random.uniform(-1, 1, size=3)])+'\n')

        with open('test_highlow.csv', 'w') as f:
            f.write('id,time,value\n')
            f.write('1476,3/16/18 0:20,high,\n')
            f.write('1477,3/16/18 0:21,low,\n')
            f.write('1478,3/16/18 0:22,150,\n')

    def tearDown(self):
        os.remove("testfile.csv")
        os.remove("rand_testfile.csv")
        os.remove('test_highlow.csv')

    def test_importdata_init_no_file(self):
        self.assertRaises(TypeError, data_import.ImportData, None)

    def test_importdata_init_invalid_file(self):
        self.assertRaises(FileNotFoundError,
                          data_import.ImportData, "not_a_file.txt")

    def test_importdata_init_testfile(self):
        csv_reader = data_import.ImportData('testfile.csv')
        assert np.average(csv_reader._value) == 10

    def test_importdata_init_testfile_rand(self):
        csv_reader = data_import.ImportData('rand_testfile.csv')
        value_avg = np.average(csv_reader._value)
        np.testing.assert_almost_equal(value_avg, 0, decimal=1)

    def test_importdata_init_smalldata(self):
        csv_reader = data_import.ImportData('rand_testfile.csv')
        for time in csv_reader._time:
            assert type(time) == data_import.datetime.datetime

    def test_import_data_skip_empty(self):
        csv_reader = data_import.ImportData('smallData/smbg_small.csv')
        assert len(csv_reader._value) == 13

    def test_linear_search_bolus(self):
        csv_reader = data_import.ImportData('smallData/bolus_small.csv')
        time_1 = data_import.datetime.datetime(2018, 3, 19, 18, 26)
        assert csv_reader.linear_search_value(time_1) == 0.7

    def test_import_data_highlow(self):
        csv_reader = data_import.ImportData('test_highlow.csv', highlow=True)
        time_high = data_import.datetime.datetime(2018, 3, 16, 0, 20)
        time_low = data_import.datetime.datetime(2018, 3, 16, 0, 21)
        time_normal = data_import.datetime.datetime(2018, 3, 16, 0, 22)
        assert csv_reader.linear_search_value(time_high) == 300.0
        assert csv_reader.linear_search_value(time_low) == 40.0
        assert csv_reader.linear_search_value(time_normal) == 150.0

    def test_linear_search_incorrect_time_format(self):
        csv_reader = data_import.ImportData('smallData/smbg_small.csv')
        self.assertRaises(TypeError, csv_reader.linear_search_value, 10)
