from flask import Flask,render_template
from typing import List
import sqlite3

app = Flask(__name__)

@app.route('/')
def table():
    """ returnns a table from database and renders the template"""

    data:List = list()
    try: 
        db: sqlite3.Connection = sqlite3.connect("C:\\Users\\shlokkhetan\\Desktop\\Second_Sem\\SSW_810\\HW12\\HW11_Tables")
    except sqlite3.DatabaseError as de:
        print(de)
        return
    data = [[name,cwid,grade,course,instructor]for name,cwid,grade,course,instructor in db.execute("SELECT (s.Name) as 'Student',(s.CWID) as 'CWID',(g.Grade) as 'Earned_grade',(g.Course) as 'In_Course',(i.Name) as 'Thought_by' from students as s inner join grades as g on s.CWID = g.StudentCWID inner join instructors i on g.InstructorCWID = i.CWID ORDER BY s.Name")]
        
    return render_template(
        'instructor_summary.htm',
        title="Stevens Repository",
        table_title="Student, Courses and Instructor Summary",
        table_temp=data)
    
app.run(debug=False)