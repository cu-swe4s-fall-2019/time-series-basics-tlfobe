import unittest
import data_import
import numpy as np
import os
import copy


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

        with open('not_a_csv.txt', 'w') as f:
            f.write('this file is not a csv\n')
            f.write('it should throw an error!\n')

    def tearDown(self):
        os.remove("testfile.csv")
        os.remove("rand_testfile.csv")
        os.remove('test_highlow.csv')
        os.remove('not_a_csv.txt')

    def test_importdata_init_no_file(self):
        self.assertRaises(TypeError, data_import.ImportData, None)

    def test_importdata_init_invalid_file(self):
        self.assertRaises(FileNotFoundError,
                          data_import.ImportData, "not_a_file.txt")

    def test_importdata_init_not_csv(self):
        self.assertRaises(KeyError,
                          data_import.ImportData, "not_a_csv.txt")

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
        assert csv_reader.linear_search_value(time_1) == [0.7]

    def test_import_data_highlow(self):
        csv_reader = data_import.ImportData('test_highlow.csv', highlow=True)
        time_high = data_import.datetime.datetime(2018, 3, 16, 0, 20)
        time_low = data_import.datetime.datetime(2018, 3, 16, 0, 21)
        time_normal = data_import.datetime.datetime(2018, 3, 16, 0, 22)
        assert csv_reader.linear_search_value(time_high) == [300.0]
        assert csv_reader.linear_search_value(time_low) == [40.0]
        assert csv_reader.linear_search_value(time_normal) == [150.0]

    def test_linear_search_incorrect_time_format(self):
        csv_reader = data_import.ImportData('smallData/smbg_small.csv')
        self.assertRaises(TypeError, csv_reader.linear_search_value, 10)


class TestRoundTimeArray(unittest.TestCase):
    def setUp(self):
        with open('test_timeround.csv', 'w') as f:
            f.write('id,time,value\n')
            f.write('1476,3/16/18 0:20,140,\n')
            f.write('1477,3/16/18 0:25,145,\n')
            f.write('1478,3/16/18 0:30,150,\n')

    def tearDown(self):
        os.remove('test_timeround.csv')

    def test_roundtimearray_wrong_inputs(self):
        csv_reader = data_import.ImportData('smallData/bolus_small.csv')
        self.assertRaises(TypeError, data_import.roundTimeArray,
                          'string!', 10, 'average', False)
        self.assertRaises(TypeError, data_import.roundTimeArray,
                          csv_reader, 'string!', 'average', False)
        self.assertRaises(TypeError, data_import.roundTimeArray,
                          csv_reader, 10, 10, False)
        self.assertRaises(
            NotImplementedError, data_import.roundTimeArray, csv_reader, 10, 'divide', False)
        self.assertRaises(TypeError, data_import.roundTimeArray,
                          'string!', 10, 'average', 'string!')

    def test_roundtimearray_test_file_average(self):
        csv_reader = data_import.ImportData('test_timeround.csv')
        zip_obj = data_import.roundTimeArray(csv_reader, 60, 'average')
        for time_round, value_avg in zip_obj:
            assert value_avg == 145.0
            assert time_round == data_import.datetime.datetime(
                2018, 3, 16, 0, 0)

    def test_roundtimearray_test_file_sum(self):
        csv_reader = data_import.ImportData('test_timeround.csv')
        zip_obj = data_import.roundTimeArray(csv_reader, 60, 'sum')
        for time_round, value_sum in zip_obj:
            assert value_sum == 435.0
            assert time_round == data_import.datetime.datetime(
                2018, 3, 16, 0, 0)

    def test_roundtimearray_test_modify(self):
        csv_reader = data_import.ImportData('test_timeround.csv')
        csv_reader_old = copy.deepcopy(csv_reader)
        data_import.roundTimeArray(
            csv_reader, 60, 'sum', modify=True)
        assert len(csv_reader._time) != len(csv_reader_old._time)


class TestPrintArray(unittest.TestCase):
    def test_printarray_bolus_cgm(self):
        bolus_data = data_import.ImportData('smallData/bolus_small.csv')
        cgm_data = data_import.ImportData('smallData/cgm_small.csv')
        cgm_zip = data_import.roundTimeArray(cgm_data, 60, 'average')
        bolus_zip = data_import.roundTimeArray(bolus_data, 60, 'sum')
        data_list = [cgm_zip, bolus_zip]
        ann_list = ['cgm_small', 'bolus_small']
        base_name = 'test_printarray.csv'
        key_file = 'cgm_small'
        data_import.printArray(data_list, ann_list, base_name, key_file)
        assert os.path.exists(base_name)
        with open(base_name, 'r') as f:
            assert 'time,cgm,bolus' in f.readline()
            assert '2018-03-16 00:00:00,144.5,0.7,' in f.readline()

    def test_printarray_input_types(self):
        bolus_data = data_import.ImportData('smallData/bolus_small.csv')
        cgm_data = data_import.ImportData('smallData/cgm_small.csv')
        cgm_zip = data_import.roundTimeArray(cgm_data, 60, 'average')
        bolus_zip = data_import.roundTimeArray(bolus_data, 60, 'sum')
        data_list = [cgm_zip, bolus_zip]
        ann_list = ['cgm_small', 'bolus_small']
        base_name = 'test_printarray.csv'
        key_file = 'cgm_small'
        self.assertRaises(TypeError, data_import.printArray, 1, ann_list, base_name, key_file)
        self.assertRaises(TypeError, data_import.printArray, data_list, 'string!', base_name, key_file)
        self.assertRaises(TypeError, data_import.printArray, data_list, ann_list, 1.234, key_file)
        self.assertRaises(TypeError, data_import.printArray, data_list, ann_list, base_name, [1,2,3,4])
        self.assertRaises(IndexError, data_import.printArray, [zip([1,2,3,4,5],[1,2,3,4,5]), 'not a zip!'], ann_list, base_name, key_file)
        self.assertRaises(IndexError, data_import.printArray, data_list, ['a', 'b', 10, [1,2,3,4]], base_name, key_file)
        os.remove('test_printarray.csv')

    
        

