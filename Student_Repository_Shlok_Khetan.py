"""Repository for stevens , author: Shlok Arun Khetan"""

import os
import unittest
from collections import defaultdict
from prettytable import PrettyTable

class Repository(object):
    """ Repository objects"""

    def __init__(self, direct):
        """init method for Repository"""

        self.directory = direct
        os.chdir(self.directory)
        self.student_dict = dict()
        self.instructor_dict = dict()
        self.majors_dict = defaultdict(lambda: defaultdict(list))


        student_path = "students.txt"
        instructor_path = "instructors.txt"
        grades_path = "grades.txt"
        majors_path = "majors.txt"

        valid_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

        for cwid, name, major in file_reader(student_path, 3, "\t"):
            self.new_student(cwid, name, major)

        for cwid, name, dept in file_reader(instructor_path, 3, "\t"):
            self.new_instructor(cwid, name, dept)

        for student_cwid, subject, grade, instructor_cwid in file_reader(grades_path, 4, "\t"):
            for key, value in self.student_dict.items():
                if student_cwid == key and grade in valid_grades:
                    value.courses.append(subject)

            for key, value in self.instructor_dict.items():
                if instructor_cwid == key:
                    value.courses[subject] += 1
       
        for major, re, course in file_reader(majors_path, 3, "\t", header=True):
            self.majors_dict[major][re].append(course)

    def new_student(self, cwid: int, name : str, major: str)-> None:
        """add new student"""

        self.student_dict[cwid] = Students(cwid, name, major)

    def new_instructor(self, cwid: int, name: str, dept: str):
        """add new instructor"""  
        self.instructor_dict[cwid] = Instructors(cwid, name, dept)

    def pretty_print_students(self):
        """printing student data"""

        student_table = PrettyTable()
        student_table.field_names = ['CWID', 'Name', 'Completed Courses', 'Remaining Required', 'Remaining Elective']

        for item in self.student_dict.values():
            student_table.add_row([item.cwid, item.name, sorted(item.courses)])

        print(student_table)

    def pretty_print_instructors(self):
        """printing instructor data"""

        instructor_table = PrettyTable()
        instructor_table.field_names = ['CWID', 'Name', 'Dept', 'course', 'students']

        for item in self.instructor_dict.values():
            for course, stu in item.courses.items():
                instructor_table.add_row([item.cwid, item.name, item.dept, course, stu])

        print(instructor_table)

class Students(object):
    """class for student"""

    def __init__(self, cwid, name, major):
        """init method for students"""

        self.cwid: int = cwid
        self.name: str = name
        self.major: str = major
        self.courses: str = list()


class Instructors(object):
    """class for instructor"""

    def __init__(self, cwid, name, dept):
        """init method for instructors"""

        self.cwid: int = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses: str = defaultdict(int)

def file_reader(path : str, fields: int, sep: str, header=False):
    """File Reader Function to clean a field separated file"""

    if not os.path.exists(path):
        raise FileNotFoundError

    fp = open(path, 'r')

    with open(path, 'r') as fp:
        if header:
            next(fp)

        for n, line in enumerate(fp, 1):
            line = line.strip()

            if line.count(sep) == fields - 1:
                yield list(line.split(sep))

            else:
                raise ValueError(f"expected {fields} fields"+
                                 f"got {line.count(sep) + 1} on line {n}")



def main()-> None:
    """ Main Function to interact with the user """

    Stevens = Repository(r'C:/Users/shlokkhetan/Documents/SSW 810/810/homework 9')

    Stevens.pretty_print_students()

    print("\n\n")

    Stevens.pretty_print_instructors()

    print(Stevens.instructor_dict)

if __name__ == '__main__':
    main()
