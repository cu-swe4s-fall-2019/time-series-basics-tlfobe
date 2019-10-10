import unittest
import data_import
import numpy as np
import os

class TestImportData(unittest.TestCase):
    def setUp(self):
        with open('testfile.csv', 'w') as f:
            f.write('Id,time,value')
            for i in range(1000):
                f.write(str(10)+(","+str(10))*2)
        
        with open('rand_testfile.csv', 'w') as f:
            l = np.random.randint(1, 1000, size = 1)
            for i in range(np.random.randint(1, 1000)):
                f.write(",".join([str(a) for a in np.random.uniform(-1000,1000, size = l)]))

    def tearDown(self):
        os.remove("testfile.csv")
        os.remove("rand_testfile.csv")

    def test_importdata_init_no_file(self):
        self.assertRaises(TypeError, data_import.ImportData, None)
    
    def test_importdata_init_invalid_file(self):
        self.assertRaises(FileNotFoundError, data_import.ImportData, "not_a_file.txt")

    def test_importdata_init_testfile(self):
        