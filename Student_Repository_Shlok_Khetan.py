from HW08_Shlok_Khetan import file_reader
import os 
from collections import defaultdict
from prettytable import PrettyTable
from typing import DefaultDict,Dict,Tuple,Iterator,List

class Major:
    """Major class for adding the majors based on 'R' or 'E' in the majors.txt"""
    def __init__(self,major: str):
        self._major: str = major
        self._required_course = list()
        self._elective_course = list()
   
    
    def add_major(self,course,RE) -> None:
        """This function seprates the list of required and elective courses"""
        if RE == 'R':
            self._required_course.append(course) 
        elif RE == 'E':
            self._elective_course.append(course)   
        else:
            print(f"Your File Contains a bad Data.This flag {RE} is not proper")

    def get_required(self) ->List[str]:
        """ Returns the list of required courses of the major"""
        return list(self._required_course)
    
    def get_electives(self) -> List[str]:
        """ Returns the list of elective courses of the major"""
        return list(self._elective_course)
    
    def pretty_major(self) -> Tuple[str,str,str]:
        """Returns the filed for pretty table """
        return [self._major,sorted(self._required_course),sorted(self._elective_course)]

class Student:
    """ Contains the info of the student and stores the information present in the file"""

    def __init__(self,cwid:str ,name:str ,major:str, required:list, electives: list):
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._coursel:List[str] = list()
        self._remaining_required:List[str] = required
        self._remaining_eletives:List[str] = electives
        self._grades: Dict[str,float] = {'A':4.0, 'A-':3.75, 'B+':3.25, 'B':3.0, 'B-':2.75, 'C+':2.25, 'C':2.0}
        self._summary_st: Dict[str,str] = dict()

    def student_course(self, course: str, grade: str):
        """Creates courses and grades dictionary"""
        self._summary_st[course] = grade
        if grade in self._grades.keys():
            self._coursel.append(course)    
             
        else:
            return self._coursel
    
    def pretty_student(self) -> Tuple[str,str,List[str]]:
        """Returns the tuples of the values for the fields of the pretty table"""
       
        return[self._cwid, self._name,self._major,sorted(self._coursel),sorted(self.calculate_required(self._summary_st)),sorted(self.calculate_electives(self._summary_st)),self.calculate_grade(self._summary_st)]
    
    def calculate_grade(self,dict:Dict[str,int]):
        """This functiton calculates the grades of the student and converts it into GPA"""
        sum: int = 0
        
        courses_grade :List[int]= list()
        for key, value in dict.items():
            if value == '':
                continue
            if value in self._grades:
                sum = sum + self._grades[value]
                courses_grade.append(value)
            else:
                return 0.0
        return format(sum/len(courses_grade),'.2f')
    
    def calculate_required(self,ls: Dict[str,str]):
        """This function calculates the list of required courses for the student in the major"""
        course_per_student: List[str] = []
        for key, value in ls.items():
            if value in self._grades.keys():
                course_per_student.append(key)
            else:
                continue

        return list(set(self._remaining_required) - set(course_per_student))
    
    def calculate_electives(self,ls: Dict[str,str]):
        """This function calculates the list of elective courses for the student in the major"""
        course_per_student: List[str] = []
        for key, value in ls.items():
            if value in self._grades.keys():
                course_per_student.append(key)
            else:
                return(self._remaining_eletives)
        if set(self._remaining_eletives).intersection(course_per_student):
            return []
        else:
            return list(self._remaining_eletives)
    
class Instructor:
    """ Contains the info of the Instructor and stores the information present in the file"""

    def __init__(self,cwid:str , name:str, dept:str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._students: DefaultDict[str,int] = defaultdict(int)
       

    def add_student(self, course:str) -> None:
        """Creates the dictionary of the students in the class of the instructor"""
      
        self._students[course] +=1
    
    def pretty_instructor(self) -> Iterator[Tuple[str,str,str,str,int]]:
        """Returns the Tuple of values for the fields of the pretty table"""

        for course,count in self._students.items():
            yield self._cwid,self._name,self._dept,course,count
    

class Repository:
    """ Repository class which contins the info of student,major,instructors and grades"""

    def __init__(self,directory:str):
        self.directory: str = directory
        self._Student: Dict[str,Student] = dict()
        self._Instructor: Dict[str,Instructor] = dict()
        self._Major: Dict[str,Major] = dict()
 
        try:
            """Reading the files"""
            self._get_majors(os.path.join(directory,'major.txt'))
            self._get_students(os.path.join(directory,'students.txt'))
            self._get_instructor(os.path.join(directory,'instructors.txt'))
            self._get_grades(os.path.join(directory,'grades.txt'))

        except ValueError as ver:
            print("The specified field number does not match the files")
        except FileNotFoundError as fne:
            raise FileNotFoundError("Specified file or directory is unavialable ")
    
    def _get_majors(self,directory: str) -> None:
        """Reads the major.txt file"""
        for  major,RE_courses,courses in file_reader(directory,3,sep='\t',header=True):
            if major not in self._Major:
                self._Major[major] = Major(major)
            self._Major[major].add_major(courses,RE_courses)
        
    def _get_students(self,directory: str) -> None:
        """Reads student.txt file"""
        for cwid,name,major in file_reader(directory,3,sep=';',header=True):
            self._Student[cwid] = Student(cwid,name,major,self._Major[major].get_required(),self._Major[major].get_electives())
    
    def _get_instructor(self,directory: str) -> None:
        """Reads instructor.txt file"""
        for cwid,name,dept in file_reader(directory,3,sep='|',header=True):
            self._Instructor[cwid] = Instructor(cwid,name,dept)
    
    def _get_grades(self,directory: str) -> None:
        """Reads grades.txt file"""
        for st_cwid,course,grade,ins_cwid in file_reader(directory,4,sep='|',header=True):
            if st_cwid in self._Student:
                self._Student[st_cwid].student_course(course,grade)
            else:
                print(f"Found grade for unknown student '{st_cwid}'")
            if ins_cwid in self._Instructor:
                self._Instructor[ins_cwid].add_student(course)
            else:
                print(f"Found grade for unknown instructor'{ins_cwid}'")
    
    

    def pretty_print_st(self):
        """Prints the summary of the instructor and grades file by the field 'CWID','Name','Course' and 'No of student' """

        pt_student: PrettyTable = PrettyTable()
        pt_student.field_names = [
            "CWID",
            "Name",
            "Major",
            "Completed Course",
            "Remaining Required",
            "Remaining Electives",
            "Grades"
        ]

        # print(self.summary)
        for student in self._Student.values():
            pt_student.add_row(student.pretty_student())

        print('\n')
        print("Student Summary")
        print(pt_student)

    def pretty_print_ins(self):
        """Prints the summary of the instructor and grades file by the field 'CWID','Name','Course' and 'No of student' """

        pt_instructor: PrettyTable = PrettyTable()
        pt_instructor.field_names = [
            "CWID",
            "Name",
            "Dept",
            "Course",
            "Students"
        ]

        # print(self.summary)
        for instructor in self._Instructor.values():
            for row in instructor.pretty_instructor():
                pt_instructor.add_row(row)

        print('\n')
        print("Instructor Summary")
        print(pt_instructor)

    def pretty_print_major(self):
        """Prints the summary of the Majors by the field 'Major','Name','Required courses' and 'Electives' """

        pt_major: PrettyTable = PrettyTable()
        pt_major.field_names = [
            "Major",
            "Required Courses",
            "Electives"
        ]

        for majors in self._Major.values():
            pt_major.add_row(majors.pretty_major())

        print('\n')
        print("Major Summary")
        print(pt_major)

if __name__ == '__main__':
    r = Repository('C:\\Users\\samee\\Desktop\\Second_Sem\\SSW_810\\HW10\\Student_Repository\\Student_Repository')
    # r.Student.pretty_print()
    r.pretty_print_major()
    r.pretty_print_st()
    r.pretty_print_ins()
