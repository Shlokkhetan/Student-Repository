from HW08_Shlok_Khetan import file_reader
from collections import defaultdict
from prettytable import PrettyTable
from typing import DefaultDict,Dict,Tuple,Iterator,List
import os 
class Major:
    """R or E selective class"""
    def __init__(self,major: str):
        self.major: str = major
        self.required_crse = list()
        self.elective_crse = list()
   
    
    def add_major(self,course,R) -> None:
        """list of required and electives are seperated"""
        if R == 'R':
            self.required_crse.append(course) 
        elif R == 'E':zt
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
        return [self.major,sorted(self.required_crse),sorted(self.elective_crse)]


class Instructor:
    """ Instructor class"""

   
    def __init__(self,cwid:str , name:str, dept:str) -> None:
        self.cwid: str = cwid
        self.name: str = name
        self.dpt: str = dept
        self.stud: DefaultDict[str,int] = defaultdict(int)


    def add_student(self, course:str) -> None:
        """student dict in innstructors's class"""
      
       
        self.stud[course] +=1
    
    def pretty_instructor(self) -> Iterator[Tuple[str,str,str,str,int]]:
        """Returns the Tuple of values for the fields of the pretty table"""

        for course,count in self.stud.items():
            
            yield self.cwid,self.name,self.dpt,course,count

class Student:
    """ Contains the info of the student and stores the information present in the file"""

    def __init__(self,cwid:str ,name:str ,major:str, required:list, electives: list):
       
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.courselist:List[str] = list()
        self.remaining_req: List[str] = required
        self.remaining_elec: List[str] = electives
        self.grade:  Dict[str,float] = {'A':4.0, 'A-':3.75, 'B+':3.25, 'B':3.0, 'B-':2.75, 'C+':2.25, 'C':2.0}
        self.smry_st:  Dict[str,str] = dict()

    def student_course(self, course: str, grade: str):
        """Creates courses and grades dictionary"""
        
        self.smry_st[course] = grade
        
        if grade in self.grade.keys():
        
            self.courselist.append(course)    
             
        
        else:
        
            return self.courselist
    
    def pretty_student(self) -> Tuple[str, str, List[str]]:
        """calues for fields and tuples are returned"""
       
        return[self.cwid, self.name,self.major,sorted(self.courselist),sorted(self.calculate_required(self.smry_st)),sorted(self.calculate_electives(self.smry_st)),self.calculate_grade(self.smry_st)]
    
    def calculate_grade(self,dict:Dict[str,int]):
        """This functiton calculates the grades of the student and converts it into GPA"""
        
        sum: int 
        
        crse_grade :List[int]= list()
        for key, value in dict.items():
            
            if value == '':
                continue
            
            if value in self.grade:
                sum = sum + self.grade[value]
                crse_grade.append(value)
            
            else:
                return 0.0
        return format(sum/len(crse_grade),'.2f')
    
    def calculate_required(self,ls: Dict[str,str]):
        """calculates the required courses"""
        
        crse_std: List[str] = [] #courses per student
        
        for key, value in ls.items():
        
            if value in self.grade.keys():
                crse_std.append(key)
        
            else:
                continue

        
        return list(set(self.remaining_req) - set(crse_std))
    
    def calculate_electives(self,ls: Dict[str,str]):
        """electives are calculated"""
        
        crse_std: List[str] = []
        
        for key, value in ls.items():
        
            if value in self.grade.keys():
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
        self.student: Dict[str,Student] = dict()
        self.instructor: Dict[str,Instructor] = dict()
        self.major: Dict[str,Major] = dict()
 
       
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
        
            if major not in self.major:
                self.major[major] = Major(major)
            self.major[major].addmajor(crs,R_crs)
        
    def _getstud(self,directory: str) -> None:
        """student.txt file is read"""
        
        for cwid,name,major in file_reader(directory,3,sep=';',header=True):
        
            self.student[cwid] = Student(cwid,name,major,self.major[major].get_required(),self.major[major].get_electives())
    
    def _getinstructor(self,directory: str) -> None:
        """instructor.txt file is read"""
        
        for cwid,name,dept in file_reader(directory,3,sep='|',header=True):
           
            self.instructor[cwid] = Instructor(cwid,name,dept)
    
    def _getgrade(self,directory: str) -> None:
        """grade.txt file is read"""
        
        for stcwid,course,grade,inscwid in file_reader(directory,4,sep='|',header=True):
        
            if stcwid in self.student:
                self.student[stcwid].student_course(course,grade)
        
            else:
                print(f"unknown student grade '{stcwid}'")
        
            if inscwid in self.instructor:
                self.instructor[inscwid].addstudent(course)
        
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

       
        for student in self.student.values():
            
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

        
        for instructor in self.instructor.values():
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

        for majors in self.major.values():
            ptmajor.add_row(majors.prettymajor())

        print('\n')
        print("Major Summary")
        print(ptmajor)

if name__ == '__main__':
    r = Repository('C:\\Users\\shlokkhetan\\Desktop\\SSW_810\\HW10\\Student_Repository\\Student_Repository')
    r.pretty_printmajor()
    r.pretty_print_st()
    r.pretty_print_ins()