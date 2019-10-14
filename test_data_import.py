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
                f.write(",".join([str(a) for a in np.random.uniform(-1,1, size = 3)])+'\n')

    def tearDown(self):
        os.remove("testfile.csv")
        os.remove("rand_testfile.csv")

    def test_importdata_init_no_file(self):
        self.assertRaises(TypeError, data_import.ImportData, None)
    
    def test_importdata_init_invalid_file(self):
        self.assertRaises(FileNotFoundError, data_import.ImportData, "not_a_file.txt")

    def test_importdata_init_testfile(self):
        csv_reader = data_import.ImportData('testfile.csv')
        assert np.average(csv_reader._value) == 10

    def test_importdata_init_testfile_rand(self):
        csv_reader = data_import.ImportData('rand_testfile.csv')
        value_avg = np.average(csv_reader._value)
        print(value_avg)
        np.testing.assert_almost_equal(value_avg, 0, decimal = 1)
