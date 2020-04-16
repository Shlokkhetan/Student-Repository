"""unittest file to test HW10"""
import unittest
from Student_Repository_Shlok_Khetan import Repository, Student, Instructor
import os, sys
from prettytable import PrettyTable
import sqlite3

class Test_HW11(unittest.TestCase):
    """ Class  to perform error checking ad handelling """
    def test_class_instructor(self):
        
        stevens: Repository = Repository(r"C:\\Users\\shlokkhetan\\Desktop\\Second_Sem\\SSW_810\\HW10\\Student_Repository\\Student_Repository")
        list1 = list()
        list2 = [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4], ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3], ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3], ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3], ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1], ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1], ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1], ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1], ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2], ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]]
        for instructor in stevens.Instructor.values():
            for row in instructor.pretty_instructor():
                list1.append(list(row))

        self.assertEqual(list1, list2)


    def test_class_student(self):
        
        stevens: Repository = Repository(r"C:\\Users\\shlokkhetan\\Desktop\\Second_Sem\\SSW_810\\HW10\\Student_Repository\\Student_Repository")
        list1 = list()
        list2 = [['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], '3.4'], ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [],'3.8'], ['10172', 'Forbes, I', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', 'CS 513', 'CS 545'], '3.9'], ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 513', 'CS 545'], '3.6'], ['10183', 'Chapman, O', ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545'], '4.0'], ['11399', 'Cordova, I', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], '3.0'], ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'], ['SSW 540', 'SSW 565', 'SSW 810'], '3.9'], ['11658', 'Kelly, P', [], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], 0.0], ['11714', 'Morton, A', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], '3.0'], ['11788', 'Fuller, E', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], '4.0']]
        for student in stevens.Student.values():
            list1.append(student.pretty_student())
        
        self.assertEqual(list1, list2)
    
    
    def test_file_not_found_error(self) -> None:
       
        with self.assertRaises(FileNotFoundError):
            Repository(r"C:\\Users\\shlokkhetan\\Desktop\\Second_Sem\\SSW_810\\HW09\\Nofile")

   
    
    def test_class_major(self):
       
        stevens: Repository = Repository(r"C:\\Users\\shlokkhetan\\Desktop\\Second_Sem\\SSW_810\\HW10\\Student_Repository\\Student_Repository")
        list1 = list()
        list2 = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']], ['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]]
        for major in stevens.Major.values():
            list1.append(major.pretty_major())
        # print(list1)
        self.assertEqual(list1, list2)
    
    def test_class_grade(self):
        db: sqlite3.Connection = sqlite3.connect("C:\\Users\\shlokkhetan\\Second_Sem\\SSW_810\\HW11\\Student_Repository\\HW11_Tables")
        list_1 = list()
        list_2 = [('Jobs, S', '10103', 'A-', 'SSW 810', 'Rowland, J'),('Jobs, S', '10103', 'B', 'CS 501', 'Hawking, S'),('Bezos, J', '10115', 'A', 'SSW 810', 'Rowland, J'), ('Bezos, J', '10115', 'F', 'CS 546', 'Hawking, S'),  ('Musk, E', '10183', 'A', 'SSW 555', 'Rowland, J'),  ('Musk, E', '10183', 'A', 'SSW 810', 'Rowland, J'),  ('Gates, B', '11714', 'B-', 'SSW 810', 'Rowland, J'),('Gates, B', '11714', 'A', 'CS 546', 'Cohen, R'),('Gates, B', '11714', 'A-', 'CS 570', 'Hawking, S')]
        for row in db.execute("SELECT (s.Name) as 'Student',(s.CWID) as 'CWID',(g.Grade) as 'Earned_grade',(g.Course) as 'In_Course',(i.Name) as 'Thought_by' from students as s inner join grades as g on s.CWID = g.StudentCWID inner join instructors i on g.InstructorCWID = i.CWID"):
            list_1.append(row)
        # print(list1)
        self.assertEqual(list_1, list_2)
        

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)