"""unittest file to test HW10"""
import unittest
from HW09_Shlok_Khetan import Repository, Student, Instructor
import os, sys
from prettytable import PrettyTable

class Test_HW09(unittest.TestCase):
    """ Class  to perform error checking ad handelling """
    def test_class_instructor(self):
        
        stevens: Repository = Repository(r"C:\\Users\\shlokkhetan\\Desktop\\Second_Sem\\SSW_810\\HW09")
        list1 = list()
        list2 = [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4], ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3], ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3], ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3], ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1], ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1], ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1], ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2], ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]]
        for instructor in stevens.Instructor.values():
            for row in instructor.pretty_instructor():
                list1.append(list(row))

        self.assertEqual(list1, list2)


    def test_class_student(self):
        
        stevens: Repository = Repository(r"C:\\Users\\shlokkhetan\\Desktop\\Second_Sem\\SSW_810\\HW09")
        list1 = list()
        list2 = [['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], '3.4'], ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [],'3.8'], ['10172', 'Forbes, I', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', 'CS 513', 'CS 545'], '3.9'], ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 513', 'CS 545'], '3.6'], ['10183', 'Chapman, O', ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545'], '4.0'], ['11399', 'Cordova, I', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], '3.0'], ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'], ['SSW 540', 'SSW 565', 'SSW 810'], '3.9'], ['11658', 'Kelly, P', [], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], 0.0], ['11714', 'Morton, A', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], '3.0'], ['11788', 'Fuller, E', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], '4.0']]
        for student in stevens.Student.values():
            list1.append(student.pretty_student())
        
        self.assertEqual(list1, list2)
    
    
    def test_file_not_found_error(self) -> None:
       
        with self.assertRaises(FileNotFoundError):
            Repository(r"C:\\Users\\shlokkhetan\\Desktop\\Second_Sem\\SSW_810\\HW09\\Nofile")

   
    
    

        

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)