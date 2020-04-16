from HW08_Shlok_Khetan import file_reader
from collections import defaultdict
from prettytable import PrettyTable
from typing import DefaultDict,Dict,Tuple,Iterator,List
import os 
import sqlite3

class Major:
    """R or E selective class"""
    def __init__(self,major: str):
        self._major: str = major
        self.required_crse = list()
        self.elective_crse = list()
   
    
    def add_major(self,course,R) -> None:
        """list of required and electives are seperated"""
        if R == 'R':
            self.required_crse.append(course) 
        elif R == 'E':
            self.elective_crse.append(course)   
        else:
            print(f"ad data found.flag {R} is not working properly")

    def get_required(self) ->List[str]:
        """ Returns the required and electives list"""
        return list(self.required_crse)
    
    def get_electives(self) -> List[str]:
        """ electives are returned"""
        return list(self.elective_crse)
    
    def pretty_major(self) -> Tuple[str,str,str]:
        """pretty tale field is eeturned"""
        return [self._major,sorted(self.required_crse),sorted(self.elective_crse)]


class Instructor:
    """ Instructor class"""

   
    def __init__(self,cwid:str , name:str, dept:str) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self.dpt: str = dept
        self.stud: DefaultDict[str,int] = defaultdict(int)


    def add_student(self, course:str) -> None:
        """student dict in innstructors's class"""
      
       
        self.stud[course] +=1
    
    def pretty_instructor(self) -> Iterator[Tuple[str,str,str,str,int]]:
        """Returns the Tuple of values for the fields of the pretty table"""

        for course,count in self.stud.items():
            
            yield self._cwid,self._name,self.dpt,course,count

class Student:
    """ Contains the info of the student and stores the information present in the file"""

    def __init__(self,cwid:str ,name:str ,major:str, required:list, electives: list):
       
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self.courselist:List[str] = list()
        self.remaining_req: List[str] = required
        self.remaining_elec: List[str] = electives
        self._grade:  Dict[str,float] = {'A':4.0, 'A-':3.75, 'B+':3.25, 'B':3.0, 'B-':2.75, 'C+':2.25, 'C':2.0}
        self.smry_st:  Dict[str,str] = dict()

    def student_course(self, course: str, grade: str):
        """Creates courses and grades dictionary"""
        
        self.smry_st[course] = grade
        
        if grade in self._grade.keys():
        
            self.courselist.append(course)    
             
        
        else:
        
            return self.courselist
    
    def pretty_student(self) -> Tuple[str, str, List[str]]:
        """calues for fields and tuples are returned"""
       
        return[self._cwid, self._name,self._major,sorted(self.courselist),sorted(self.calculate_required(self.smry_st)),sorted(self.calculate_electives(self.smry_st)),self.calculate_grade(self.smry_st)]
    
    def calculate_grade(self,dict:Dict[str,int]):
        """This functiton calculates the grades of the student and converts it into GPA"""
        
        sum: int = 0
        
        crse_grade :List[int]= list()
        for key, value in dict.items():
            
            if value == '':
                continue
            
            if value in self._grade:
                sum = sum + self._grade[value]
                crse_grade.append(value)
            
            else:
                return 0.0
        return format(sum/len(crse_grade),'.2f')
    
    def calculate_required(self,ls: Dict[str,str]):
        """calculates the required courses"""
        
        crse_std: List[str] = [] #courses per student
        
        for key, value in ls.items():
        
            if value in self._grade.keys():
                crse_std.append(key)
        
            else:
                continue

        
        return list(set(self.remaining_req) - set(crse_std))
    
    def calculate_electives(self,ls: Dict[str,str]):
        """electives are calculated"""
        
        crse_std: List[str] = []
        
        for key, value in ls.items():
        
            if value in self._grade.keys():
                crse_std.append(key)
        
            else:
                return(self.remaining_elec)
        
        if set(self.remaining_elec).intersection(crse_std):
            return []
        
        else:
            return list(self.remaining_elec)
    

    



class Repository:
    """ info for student,major,instructors and grades"""

    def __init__(self,directory:str):
        self.directory: str = directory
        self._student: Dict[str,Student] = dict()
        self._Instructor: Dict[str,Instructor] = dict()
        self._major: Dict[str,Major] = dict()
 
       
        try:
            """Reading the files"""
       
            self._getmajors(os.path.join(directory,'major.txt'))
            self._getstud(os.path.join(directory,'students.txt'))
            self._getinstructor(os.path.join(directory,'instructors.txt'))
            self._getgrade(os.path.join(directory,'grades.txt'))

        except ValueError as verr:
            
            print("files are not matched by the number specified")
        
        except FileNotFoundError as fnerr:
            
            raise FileNotFoundError("file/directory not found")
    
    def _getmajors(self,directory: str) -> None:
        """ major.txt file is read """
        
        for  major,R_crs,crs in file_reader(directory,3,sep='\t',header=True):
        
            if major not in self._major:
                self._major[major] = Major(major)
            self._major[major].addmajor(crs,R_crs)
        
    def _getstud(self,directory: str) -> None:
        """student.txt file is read"""
        
        for cwid,name,major in file_reader(directory,3,sep=';',header=True):
        
            self._student[cwid] = Student(cwid,name,major,self._major[major].get_required(),self._major[major].get_electives())
    
    def _getinstructor(self,directory: str) -> None:
        """instructor.txt file is read"""
        
        for cwid,name,dept in file_reader(directory,3,sep='|',header=True):
           
            self._Instructor[cwid] = Instructor(cwid,name,dept)
    
    def _getgrade(self,directory: str) -> None:
        """grade.txt file is read"""
        
        for stcwid,course,grade,inscwid in file_reader(directory,4,sep='|',header=True):
        
            if stcwid in self._student:
                self._student[stcwid].student_course(course,grade)
        
            else:
                print(f"unknown student grade '{stcwid}'")
        
            if inscwid in self._Instructor:
                self._Instructor[inscwid].addstudent(course)
        
            else:
                print(f"unknown instructor grade'{inscwid}'")
    
    

    def pretty_print_st(self):
        """student tale printed"""

        ptstudent: PrettyTable = PrettyTable()
        ptstudent.fieldnames = [
            "CWID",
            "Name",
            "Major",
            "Completed Course",
            "Remaining Required",
            "Remaining Electives",
            "Grades"
        ]

       
        for student in self._student.values():
            
            ptstudent.add_row(student.prettystudent())

        print('\n')
        print("Student Summary")
        print(ptstudent)

    def pretty_print_ins(self):
        """istructor tale printed """

        ptinstructor: PrettyTable = PrettyTable()
        
        ptinstructor.fieldnames = [
            "CWID",
            "Name",
            "Dept",
            "Course",
            "Students"
        ]

        
        for instructor in self._Instructor.values():
            for row in instructor.prettyinstructor():
                ptinstructor.add_row(row)

        print('\n')
        print("Instructor Summary")
        print(ptinstructor)

    def pretty_printmajor(self):
        """major tale printed """

        ptmajor: PrettyTable = PrettyTable()
       
        ptmajor.fieldnames = [
            "Major",
            "Required Courses",
            "Electives"
        ]

        for majors in self._major.values():
            ptmajor.add_row(majors.prettymajor())

        print('\n')
        print("Major Summary")
        print(ptmajor)

    def student_grade_table_db(self,db_path):
        ptgrades: PrettyTable = PrettyTable()
        ptgrades.fieldnames = [
            "Name",
            "CWID",
            "Course",
            "Grade",
            "Instructor"
            ]
        db: sqlite3.Connection = sqlite3.connect(db_path)
        for row in db.execute("SELECT (s.Name) as 'Student',(s.CWID) as 'CWID',(g.Grade) as 'Earned_grade',(g.Course) as 'In_Course',(i.Name) as 'Thought_by' from students as s inner join grades as g on s.CWID = g.StudentCWID inner join instructors i on g.InstructorCWID = i.CWID ORDER BY s.Name"):
                    # print(row)
                ptgrades.add_row(row)
        
        print('\n')
        print("Grades Summary")
        print(ptgrades)

if __name__ == '__main__':
    r = Repository('C:\\Users\\shlokkhetan\\Desktop\\SSW_810\\HW10\\Student_Repository\\Student_Repository')
    r.pretty_printmajor()
    r.pretty_print_st()
    r.pretty_print_ins()
    r.student_grade_table_db("C:\\Users\\shlokkhetan\\Second_Sem\\SSW_810\\HW11\\Student_Repository\\HW11_Tables")