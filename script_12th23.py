from colorama import Fore, Back, Style, init
import os
import json
import requests
from bs4 import BeautifulSoup
import mysql.connector
from prettytable import PrettyTable
from pyfiglet import Figlet


conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='upboard'
)
cursor = conn.cursor()
def create_banner(text, font='standard'):
    fig = Figlet(font=font)
    banner = fig.renderText(text)
    return banner
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    if __name__ == "__main__":
        banner_text = "Vijay Singh"
        banner = create_banner(banner_text)
        print(banner)
        init()
        print(Back.RED + ' ' * 20 + "Finding Result......" + ' ' * 20)
        print(Style.RESET_ALL + '')

def startagain():
    roll_input = input(f"Roll No {Fore.RED}[CTRL+C to Exit]{Style.RESET_ALL}: ")
    validated_roll = validate_input(roll_input)

    if validated_roll is not None:
        clear_terminal()
        getresult(validated_roll)
    else:
        print(f"{Fore.RED}Please provide a valid roll number.{Style.RESET_ALL}")

def check_roll_number_exist(roll_number):
    cursor.execute("SELECT COUNT(*) FROM studentinfo12th2023 WHERE rollno = %s", (roll_number,))
    result = cursor.fetchone()[0]
    return result > 0

def insert_student_info_and_subjects(roll_number, name, father, mother, dob, school, subjects):
    cursor.execute("INSERT INTO studentinfo12th2023 (rollno, name, father, mother, dob, school) VALUES (%s, %s, %s, %s, %s, %s)",
                   (roll_number, name, father, mother, dob, school))
    
    table = PrettyTable([Fore.YELLOW + 'Roll Number' + Style.RESET_ALL,
                        Fore.YELLOW + 'Name' + Style.RESET_ALL,
                        Fore.YELLOW + 'Father' + Style.RESET_ALL,
                        Fore.YELLOW + 'Mother' + Style.RESET_ALL,
                        Fore.YELLOW + 'DOB' + Style.RESET_ALL,
                        Fore.YELLOW + 'School' + Style.RESET_ALL])
    colored_data = [Fore.WHITE + str(data) + Style.RESET_ALL for data in (roll_number, name, father, mother, dob, school)]
    table.add_row(colored_data)
    print(table)

    table = PrettyTable([Fore.GREEN + 'Subject' + Style.RESET_ALL,
                Fore.GREEN + 'Subjective' + Style.RESET_ALL,
                Fore.GREEN + 'Practical' + Style.RESET_ALL,
                Fore.GREEN + 'Total' + Style.RESET_ALL,
                Fore.GREEN + 'Grade' + Style.RESET_ALL])
    
    for subject_info in subjects:
        daj=[]
        subject = subject_info['subject']
        mark = subject_info['mark']
        practical = subject_info['practical']
        total = subject_info['total']
        grade = subject_info['grade']
        
        daj.append(subject)
        daj.append(mark)
        daj.append(practical)
        daj.append(total)
        daj.append(grade)
        cursor.execute("INSERT INTO studentsubjects12th2023(rollno, subjects, mark, practical, total, grade) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (roll_number, subject, mark, practical, total, grade))

        table.add_row(daj)
    print(table)
    conn.commit()
    
    startagain()

def getstudent(cursor, rollno):
    rows=[]
    query = "SELECT * FROM studentinfo12th2023 WHERE rollno = %s"
    cursor.execute(query, (rollno,))
    row = cursor.fetchone()
    rows.append(row)
    if row:
        return row
    else:
        return None

def getmarks(cursor, rollno):
    query = "SELECT subjects,mark,practical,total,grade FROM studentsubjects12th2023 WHERE rollno = %s"
    cursor.execute(query, (rollno,))
    row = cursor.fetchall()
    if row:
        return row
    else:
        return None


try:
    def getresult(rollno):
        if check_roll_number_exist(rollno):
            studentdata=getstudent(cursor,rollno)
            table = PrettyTable([Fore.YELLOW + 'Roll Number' + Style.RESET_ALL,
                                Fore.YELLOW + 'Name' + Style.RESET_ALL,
                                Fore.YELLOW + 'Father' + Style.RESET_ALL,
                                Fore.YELLOW + 'Mother' + Style.RESET_ALL,
                                Fore.YELLOW + 'DOB' + Style.RESET_ALL,
                                Fore.YELLOW + 'School' + Style.RESET_ALL])
            colored_data = [Fore.WHITE + str(data) + Style.RESET_ALL for data in studentdata]
            table.add_row(colored_data)
            print(table)

            studentmarks=getmarks(cursor,rollno)
            table = PrettyTable([Fore.GREEN + 'Subject' + Style.RESET_ALL,
                     Fore.GREEN + 'Subjective' + Style.RESET_ALL,
                     Fore.GREEN + 'Practical' + Style.RESET_ALL,
                     Fore.GREEN + 'Total' + Style.RESET_ALL,
                     Fore.GREEN + 'Grade' + Style.RESET_ALL])
            for studentmark in studentmarks:
                table.add_row(studentmark)
            print(table)
            startagain()


        else:
            if rollno is None:
                raise ValueError("Parameter 'Roll Number' must be provided.")
            # form_url = 'https://results.upmsp.edu.in/ResultHighSchool_2022.aspx'
            form_url='https://results.upmsp.edu.in/ResultIntermediate.aspx'
            response = requests.get(form_url)
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')
            inputs=soup.find_all("input")
            dataa=[]
            for inpu in inputs:
                name=inpu.get("name")
                value=inpu.get("value")
                d=[]
                if name:
                    if name=="ctl00$cphBody$txt_RollNumber":
                        value=rollno
                    d.append(name)
                    d.append(value)
                    dataa.append(d)
            k=[]
            k.append("ctl00$cphBody$ddl_ExamYear")
            k.append("2023")
            dataa.append(k)
            k=[]
            k.append("ctl00$cphBody$ddl_districtCode")
            k.append("45")
            dataa.append(k)
            payload=dict(dataa)

            response = requests.post(form_url, data=payload)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find("table")
                if table:
                    name_element = table.find('span', id='ctl00_cphBody_lbl_C_NAME')
                    mother_element = table.find('span', id='ctl00_cphBody_lbl_M_NAME')
                    father_element = table.find('span', id='ctl00_cphBody_lbl_F_NAME')
                    # dob_element = table.find('span', id='ctl00_cphBody_lbl_DDMMYYYY')
                    school_element = table.find('span', id='ctl00_cphBody_lbl_SCHOOL_CD')
                    if name_element.text!="" and mother_element.text!="" and father_element.text!="":
                        name = name_element.text if name_element else None
                        mother = mother_element.text if mother_element else None
                        father = father_element.text if father_element else None
                        # dob = dob_element.text if dob_element else None
                        school = school_element.text if school_element else None
                        dob="Not Find"
                        result = []
                        rows = table.find_all("tr")
                        ille=True
                        for row in rows:
                            if ille:
                                ille=False
                                continue
                            col = row.find_all("td")
                            if len(col) == 8:
                                sub = {
                                    "subject": col[0].find("span").text if col[0].find("span") else None,
                                    "mark": col[1].find("span").text if col[1].find("span") else None,
                                    "practical": col[6].find("span").text if col[6].find("span") else None,
                                    "total": col[7].find("span").text if col[7].find("span") else None,
                                    "grade": "N/A",
                                }
                                if all(value is not None for value in sub.values()):
                                    result.append(sub)
                        stude={
                            "name": name,
                            "mother": mother,
                            "father": father,
                            "dob": dob,
                            "school": school,
                        }
                        student_data = {
                            "student": stude,
                            "results": result
                        }

                        if not check_roll_number_exist(rollno):
                            insert_student_info_and_subjects(rollno, **stude, subjects=result)
                        else:
                            print(f"{Fore.RED}{name} {rollno} [already exists]{Style.RESET_ALL}")
                        formatted_json = json.dumps(student_data, indent=4)
                        # print(formatted_json)
                    else:
                        print(f"{Fore.RED}{rollno} is not a valid Roll Number.{Style.RESET_ALL}")
                    
            else:
                print(f"{Fore.RED}Error in Load.{Style.RESET_ALL}")


    def validate_input(roll_no):
        try:
            roll_no = int(roll_no)
            if len(str(roll_no)) == 10:
                return roll_no
            else:
                print(f"{Fore.YELLOW}Roll number must be an integer of length 10.{Style.RESET_ALL}")
                return None
        except ValueError:
            print(f"{Fore.YELLOW}Roll number must be an integer.{Style.RESET_ALL}")
            return None
        
    startagain()



except KeyboardInterrupt:
    print(f"{Fore.BLUE}\nCtrl+C pressed. Exiting gracefully.{Style.RESET_ALL}")
