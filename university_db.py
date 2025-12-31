import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to SQLite!")
        return conn
    except Error as e:
        print(e)
        return None


def create_table(conn, create_table_sql):
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        print("Table created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_student(conn, student_name,PASSW):
    """
    Insert a new student into the 'students' table.

    Parameters:
        conn: SQLite3 Connection object.
        student_name: A string with the student's name.

    Returns:
        The SID of the newly inserted student.
    """
    sql = "INSERT INTO students (sname,PASSW) VALUES (?,?)"

    try:
        cursor = conn.cursor()
        cursor.execute(sql, (student_name,PASSW))
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Student inserted successfully with SID = {new_id}")

        return new_id

    except Error as e:
        print(f"Error inserting student: {e}")
        return None


def insert_enroll(conn,SID,CID): 
    sql = "INSERT INTO enroll (SID,CID) VALUES (?,?)"
    try:
         cursor = conn.cursor() 
         cursor.execute(sql,(SID,CID))
         conn.commit()
         new_enroll = cursor.lastrowid 
         print(f"enrolled successfully with CID = {new_enroll}")
         return new_enroll 
    except Error as e:
         print(f"error enrolling:{e}")
         return None


def insert_course(conn, course_name,credits):
    
    cur =conn.cursor()

    cur.execute(
        "SELECT CID FROM courses WHERE cname = ?", (course_name,)
    )
    row = cur.fetchone()

    if row:
        return row[0]
    
    cur.execute(
        "INSERT INTO courses (cname, credits) VALUES (?, ?)",
        (course_name, credits)
    )

    conn.commit()
    return cur.lastrowid

def enroll_student(conn, Sid):
    Cid = int(input("Enter course id: "))
    cur = conn.cursor()
    
    cur.execute("SELECT CID FROM courses WHERE CID = ?", (Cid,))
    if cur.fetchone() is None:
        print("Course does not exist in database.")
        return
    
    cur.execute("SELECT * FROM enroll WHERE SID = ? AND CID = ?",(Sid,Cid))
    if cur.fetchone() is not None:
        print("you are already enrolled")
        return
   
    try:
        cur.execute("INSERT INTO enroll (SID, CID) VALUES (?,?)",(Sid,Cid))
        conn.commit()
        print("enrolled in class succusfuly")
    except Error as e:
        print(f"Erorr: {e}") # this will make a huge output when runing the program more than once becuse it has alr enrolled berfore 


def withdraw_class(conn, Sid):
    Cid = int(input("Enter the course ID you want to withdraw: "))
    cur = conn.cursor()
   
   
    cur.execute("SELECT CID FROM enroll WHERE CID = ? AND SID = ?", (Cid,Sid))
    if cur.fetchone() is None:
        print("you're not enrolled in first place!")
        return
    try:
        cur.execute("DELETE FROM enroll WHERE SID = ? AND CID = ? ",(Sid,Cid))
        conn.commit()
        print("withdrawn succusfuly")
    except Error as e:
        print(f"Error: {e}")


def creat_new_student(conn,):
    name = input("whats your name: ")
    PASSW= input("enter password: ")
    sql = "INSERT INTO students (Sname,PASSW) VALUES (?,?)"
    try:
        cursor = conn.cursor()
        cursor.execute(sql,(name,PASSW))
        conn.commit()
        new_student_id = cursor.lastrowid
        print(f"added student succcesfully with id = {new_student_id}")
    except Error as e:
        print(f"Error: {e}")


def list_courses(conn,Sid):
    cur = conn.cursor()

    sql = """
    SELECT
        c.CID,
        c.cname,
        c.credits
    FROM courses c
    JOIN enroll e ON c.CID = e.CID
    where e.SID = ?
    """
    cur.execute(sql, (Sid,))
    rows = cur.fetchall()

    if not rows:
        print("you are not enrolled in any classes")
        return
    
    print("\nYour Enrolled Courses:")
    for cid, cname, credits in rows:
        print(f"CID: {cid} | cname: {cname} | credits: {credits}")


def list_all_courses(conn):
    cur = conn.cursor()

    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def search_courses(conn):
    substring = input("enter a part of the course name: ")
    cur = conn.cursor()

    cur.execute("SELECT * FROM courses WHERE cname LIKE ?", ('%' + substring + '%',))
    results = cur.fetchall()

    if results:
        print("matched courses: ")
        for course in results:
            print(f"Course ID: {course[0]}, Name: {course[1]}, credits: {course[2]}")
    else:
        print("no matching courses")        

def start_UI(conn):
    cur = conn.cursor()

    while True:
        try:
            Sid = int(input("Enter your student ID (press -1 to create new one): "))
        except ValueError:
            print("student ID must be an integer.")
            continue

        if Sid == -1:
            creat_new_student(conn)
            continue
        PASSW = input("Enter your password: ")
                             
        cur.execute("SELECT * FROM students WHERE SID = ? AND PASSW = ?", (Sid,PASSW))
        student = cur.fetchone()

        if student:
            print(f"welcome , student #{Sid}!")
            break
        else:
            print("student witht this ID don't exist")
        
    while True:
        print("\n===STUDENT MENU===")
        print("C- Create new student record")
        print("M - List my classes")
        print("A - List all available courses")
        print("E - enroll in a course")
        print("W - withdraw from a course")
        print("S - search courses by name")
        print("X - Exit")

        choice = input("Select a command(in upper case): ")
        
        if choice == "C":
            creat_new_student(conn)
        elif choice == "M":
            list_courses(conn,Sid)
        elif choice == "A":
            list_all_courses(conn)
        elif choice == "E":
            enroll_student(conn,Sid)
        elif choice == "W":
            withdraw_class(conn, Sid)
        elif choice =="S":
            search_courses(conn)
        elif choice =="X":
            print("goodbye!")
            exit()
        else:
            print("command don't exist try again")
            1


def main():
    database = "new_sqlite.db"

    SQL_CREATE_STUDENTS_TABLE = """
        CREATE TABLE IF NOT EXISTS students (
            SID INTEGER PRIMARY KEY AUTOINCREMENT,
            sname TEXT NOT NULL,
            PASSW TEXT NOT NULL
        );
    """

    SQL_CREATE_COURSES_TABLE = """
        CREATE TABLE IF NOT EXISTS courses (
            CID INTEGER PRIMARY KEY AUTOINCREMENT,
            cname TEXT NOT NULL UNIQUE,
            credits INTEGER
        );
    """

    SQL_CREATE_ENROLL_TABLE = """
        CREATE TABLE IF NOT EXISTS enroll (
            enroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
            SID INTEGER,
            CID INTEGER,
            FOREIGN KEY (SID) REFERENCES students(SID),
            FOREIGN KEY (CID) REFERENCES courses(CID),
            UNIQUE (SID, CID)  
        );

    """

    # connect to DB
    conn = create_connection(database)

    if conn is not None:
        
        create_table(conn, SQL_CREATE_STUDENTS_TABLE)
        create_table(conn, SQL_CREATE_COURSES_TABLE)
        create_table(conn, SQL_CREATE_ENROLL_TABLE)
        """
        insert_student(conn,"issa","WHATEVER")
        insert_student(conn,"moe","WHATEVER")
        insert_student(conn,"jake","WHATEVER")
        insert_student(conn,"emma","WHATEVER")
        insert_student(conn, "mil","WHATEVER")

        insert_course(conn,"CSIT 355",3)
        insert_course(conn,"CSIT 460",3)
        insert_course(conn,"CSIT 345",4)
        insert_course(conn,"BIO 112",4)
        insert_course(conn,"BIO 113",4)
        
        insert_enroll(conn,1,1)
        insert_enroll(conn,2,2)
        insert_enroll(conn,3,3)
        insert_enroll(conn,4,4)
        insert_enroll(conn,5,5)
        insert_enroll(conn,1,2)
        insert_enroll(conn,2,3)
        insert_enroll(conn,3,4)
        insert_enroll(conn,4,5)
        insert_enroll(conn,5,1)
        """
        start_UI(conn)

        conn.close()
    else:
        print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()

