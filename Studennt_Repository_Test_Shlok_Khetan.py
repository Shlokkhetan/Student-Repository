"""test cases for hw 09"""

import unittest
from HW09_Shlok_Khetan import Repository, Students , Instructors, file_reader

class testcases(unittest.TestCase):
    """test cases foir Repository repository"""

    def test_Repository_file_reader_students(self):
        """do these methods work properly?"""
        test1 = file_reader(r"C:/Users/shlokkhetan/Documents/SSW 810/810/homework 9/students.txt", 3, '\t')
        self.assertEqual(next(test1), ["10103", "Baldwin, C", "SFEN"])
        self.assertEqual(next(test1), ["10115",	"Wyatt, X",	"SFEN"])
        self.assertEqual(next(test1), ["10172",	"Forbes, I", "SFEN"])
        self.assertEqual(next(test1), ["10175",	"Erickson, D", "SFEN"])
        self.assertEqual(next(test1), ["10183",	"Chapman, O", "SFEN"])
        self.assertEqual(next(test1), ["11399", "Cordova, I", "SYEN"])
        self.assertEqual(next(test1), ["11461",	"Wright, U", "SYEN"])
        self.assertEqual(next(test1), ["11658", "Kelly, P", "SYEN"])
        self.assertEqual(next(test1), ["11714", "Morton, A", "SYEN"])
        self.assertNotEqual(next(test1), ["7254378654", "john, D", "arts"])

        with self.assertRaises(FileNotFoundError):
            for i in file_reader(r"C:/Users/shlokkhetan/Documents/SSW 810/810/homework 9/notstudents.txt", "3", "\t"):
                return i

    def test_Repository_file_reader_instructors(self):
        """do these methods work properly?"""
        test1 = file_reader(r"C:/Users/shlokkhetan/Documents/SSW 810/810/homework 9/instructors.txt", 3, '\t')
        self.assertEqual(next(test1), ["98765", "Einstein, A", "SFEN"])
        self.assertEqual(next(test1), ["98764", "Feynman, R", "SFEN"])
        self.assertEqual(next(test1), ["98763", "Newton, I", "SFEN"])
        self.assertEqual(next(test1), ["98762", "Hawking, S", "SYEN"])
        self.assertEqual(next(test1), ["98761", "Edison, A", "SYEN"])
        self.assertNotEqual(next(test1), ["435765", "foo, b", "commerce"])

        with self.assertRaises(FileNotFoundError):
            for i in file_reader(r"C:/Users/shlokkhetan/Documents/SSW 810/810/homework 9/notinstructors.txt", "4", "\t"):
                return i

    def test_Repository_file_reader_grades(self):
        """do these methods work properly?"""
        test1 = file_reader(r"C:/Users/shlokkhetan/Documents/SSW 810/810/homework 9/grades.txt", 4, '\t')
        self.assertEqual(next(test1), ["10103", "SSW 567", "A", "98765"])
        self.assertEqual(next(test1), ["10103", "SSW 564", "A-", "98764"])
        self.assertEqual(next(test1), ["10103", "SSW 687", "B", "98764"])
        self.assertEqual(next(test1), ["10103", "CS 501", "B", "98764"])
        self.assertEqual(next(test1), ["10115", "SSW 567", "A", "98765"])
        self.assertEqual(next(test1), ["10115", "SSW 564", "B+", "98764"])
        self.assertEqual(next(test1), ["10115", "SSW 687", "A", "98764"])
        self.assertEqual(next(test1), ["10115", "CS 545", "A", "98764"])
        self.assertEqual(next(test1), ["10172", "SSW 555", "A", "98763"])
        self.assertEqual(next(test1), ["10172", "SSW 567", "A-", "98765"])
        self.assertNotEqual(next(test1), ["1829126832", "MIS 810", "F", "862987263"])

        with self.assertRaises(FileNotFoundError):
            for i in file_reader(r"C:/Users/shlokkhetan/Documents/SSW 810/810/homework 9/notgrades.txt", "4", "\t"):
                return i

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)

if __name__ == '__main__':
    unittest.main()
