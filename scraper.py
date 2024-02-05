from colorama import Fore, Back, Style, init
import json
import requests
from bs4 import BeautifulSoup
import mysql.connector
from prettytable import PrettyTable
import argparse
import datetime

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='upboard'
)
cursor = conn.cursor()
def check_roll_number_exist(roll_number):
    cursor.execute("SELECT COUNT(*) FROM studentinfo10th WHERE rollno = %s", (roll_number,))
    result = cursor.fetchone()[0]
    return result > 0

def insert_student_info_and_subjects(roll_number, name, father, mother, dob, school, subjects):
    cursor.execute("INSERT INTO studentinfo10th (rollno, name, father, mother, dob, school) VALUES (%s, %s, %s, %s, %s, %s)",
                   (roll_number, name, father, mother, dob, school))

    for subject_info in subjects:
        subject = subject_info['subject']
        mark = subject_info['mark']
        practical = subject_info['practical']
        total = subject_info['total']
        grade = subject_info['grade']
        cursor.execute("INSERT INTO studentsubjects10th(rollno, subjects, mark, practical, total, grade) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (roll_number, subject, mark, practical, total, grade))

    conn.commit()
    print(f"{Fore.GREEN}{name} {roll_number} inserted successfully.{Style.RESET_ALL}")

def getstudent(cursor, rollno):
    rows=[]
    query = "SELECT * FROM studentinfo10th WHERE rollno = %s"
    cursor.execute(query, (rollno,))
    row = cursor.fetchone()
    rows.append(row)
    # query = "SELECT * FROM studentsubjects10th WHERE rollno = %s"
    # cursor.execute(query, (rollno,))
    # row = cursor.fetchone()
    # rows.append(row)
    if row:
        return row
    else:
        return None

def getmarks(cursor, rollno):
    query = "SELECT subjects,mark,practical,total,grade FROM studentsubjects10th WHERE rollno = %s"
    cursor.execute(query, (rollno,))
    row = cursor.fetchall()
    if row:
        return row
    else:
        return None

def validate_start_end_order(start, end):
    if start >= end:
        raise argparse.ArgumentTypeError("--start value must be lower than --end value")

def validate_std(value):
    if value not in ['10', '12']:
        raise argparse.ArgumentTypeError("--std must be '10' or '12'")
    else:
        return int(value)

def validate_dist(value):
    try:
        value = int(value)
        if not (0 < value < 100):
            raise argparse.ArgumentTypeError("--dist must be less than 100")
        return value  # Return the validated integer
    except ValueError:
        raise argparse.ArgumentTypeError("--dist must be an integer")

def find_name_by_dist(data, target_dist):
    for entry in data:
        name, code = entry
        if code == target_dist:
            return name
    return None  # Return None if no match is found

def validate_year(value):
    try:
        year = int(value)
        current_year = datetime.datetime.now().year
        if not (1921 <= year <= current_year):
            raise argparse.ArgumentTypeError(f"--year must be in the range 1921 to {current_year}")
        else:
            return year
    except ValueError:
        raise argparse.ArgumentTypeError("--year must be an integer")

def validate_int(value):
    try:
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} must be an integer")

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Uttar Pradesh Board Examination Result scraper.')

    # Add required command-line arguments
    parser.add_argument('--start', type=validate_int, required=True, help='First Roll no to Scrape')
    parser.add_argument('--end', type=validate_int, required=True, help='Last Roll Number to scrape in Range')
    parser.add_argument('--dist', type=validate_dist, required=True, help='District Code')
    parser.add_argument('--std', type=validate_std, required=True, help='Your Class 10[High School] 12[Intermediate]')
    parser.add_argument('--year', type=validate_year, required=True, help='Year [Board Exam Year]')

    data_array = [
    [
        "AGRA",
        1
    ],
    [
        "ALIGARH",
        6
    ],
    [
        "AMBEDKAR NAGAR",
        64
    ],
    [
        "AMETHI",
        65
    ],
    [
        "AMROHA",
        22
    ],
    [
        "AURIYA",
        43
    ],
    [
        "AYODHYA",
        62
    ],
    [
        "AZAMGARH",
        80
    ],
    [
        "BAGPAT",
        13
    ],
    [
        "BAHRAICH",
        66
    ],
    [
        "BALLIA",
        82
    ],
    [
        "BALRAMPUR",
        69
    ],
    [
        "BANDA",
        51
    ],
    [
        "BARABANKI",
        63
    ],
    [
        "BAREILLY",
        26
    ],
    [
        "BASTI",
        71
    ],
    [
        "BHADOHI",
        88
    ],
    [
        "BIJNOR",
        23
    ],
    [
        "BUDAUN",
        27
    ],
    [
        "BULANDSHAHR",
        9
    ],
    [
        "CHANDAULI",
        86
    ],
    [
        "CHITRAKOOT",
        52
    ],
    [
        "DEORIA",
        77
    ],
    [
        "ETAH",
        4
    ],
    [
        "ETAWAH",
        41
    ],
    [
        "FARRUKHABAD",
        40
    ],
    [
        "FATEHPUR",
        56
    ],
    [
        "FIROZABAD",
        2
    ],
    [
        "GAUTAM BUDH NAGAR",
        11
    ],
    [
        "GHAZIABAD",
        10
    ],
    [
        "GHAZIPUR",
        84
    ],
    [
        "GONDA",
        68
    ],
    [
        "GORAKHPUR",
        75
    ],
    [
        "HAMIRPUR",
        49
    ],
    [
        "HAPUR",
        14
    ],
    [
        "HARDOI",
        33
    ],
    [
        "HATHRAS",
        7
    ],
    [
        "JALAUN",
        45
    ],
    [
        "JAUNPUR",
        83
    ],
    [
        "JHANSI",
        47
    ],
    [
        "KANNAUJ",
        42
    ],
    [
        "KANPUR DEHAT",
        39
    ],
    [
        "KANPUR NAGAR",
        38
    ],
    [
        "KASGANJ",
        8
    ],
    [
        "KAUSHAMBI",
        57
    ],
    [
        "KUSHINAGAR",
        78
    ],
    [
        "LAKHIMPUR KHIRI",
        31
    ],
    [
        "LALITPUR",
        48
    ],
    [
        "LUCKNOW",
        34
    ],
    [
        "MAHARAJGANJ",
        76
    ],
    [
        "MAHOBA",
        50
    ],
    [
        "MAINPURI",
        3
    ],
    [
        "MATHURA",
        5
    ],
    [
        "MAU",
        81
    ],
    [
        "MEERUT",
        12
    ],
    [
        "MIRZAPUR",
        89
    ],
    [
        "MORADABAD",
        21
    ],
    [
        "MUZAFFAR NAGAR",
        15
    ],
    [
        "PILIBHIT",
        29
    ],
    [
        "PRATAPGARH",
        54
    ],
    [
        "PRAYAGRAJ",
        55
    ],
    [
        "RAE BARAILI",
        36
    ],
    [
        "RAMPUR",
        24
    ],
    [
        "SAMBHAL",
        25
    ],
    [
        "SANT KABIR NAGAR",
        72
    ],
    [
        "SHAHARANPUR",
        16
    ],
    [
        "SHAHJAHANPUR",
        28
    ],
    [
        "SHAMLI",
        17
    ],
    [
        "SHRAWASTI",
        67
    ],
    [
        "SIDDHARTA NAGAR",
        73
    ],
    [
        "SITAPUR",
        32
    ],
    [
        "SONBHADRA",
        90
    ],
    [
        "SULTANPUR",
        61
    ],
    [
        "UNNAO",
        35
    ],
    [
        "VARANASI",
        85
    ]
]

    try:
        args = parser.parse_args()
        district=find_name_by_dist(data_array, args.dist)
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
                else:
                    if rollno is None:
                        raise ValueError("Parameter 'Roll Number' must be provided.")
                    form_url = 'https://results.upmsp.edu.in/ResultHighSchool_2022.aspx'
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
                    k.append("2022")
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
                            dob_element = table.find('span', id='ctl00_cphBody_lbl_DDMMYYYY')
                            school_element = table.find('span', id='ctl00_cphBody_lbl_SCHOOL_CD')
                            if name_element.text!="" and mother_element.text!="" and father_element.text!="" and dob_element.text!="":
                                name = name_element.text if name_element else None
                                mother = mother_element.text if mother_element else None
                                father = father_element.text if father_element else None
                                dob = dob_element.text if dob_element else None
                                school = school_element.text if dob_element else None
                                result = []
                                rows = table.find_all("tr")
                                ille=True
                                for row in rows:
                                    if ille:
                                        ille=False
                                        continue
                                    col = row.find_all("td")
                                    if len(col) == 5:
                                        sub = {
                                            "subject": col[0].find("span").text if col[0].find("span") else None,
                                            "mark": col[1].find("span").text if col[1].find("span") else None,
                                            "practical": col[2].find("span").text if col[2].find("span") else None,
                                            "total": col[3].find("span").text if col[3].find("span") else None,
                                            "grade": col[4].find("span").text if col[4].find("span") else None,
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

                                if rollno<1221294200:
                                    getresult(rollno+1)
                                formatted_json = json.dumps(student_data, indent=4)
                                # print(formatted_json)
                            else:
                                print(f"{Fore.RED}{rollno} is not a valid Roll Number.{Style.RESET_ALL}")
                            
                    else:
                        print(f"{Fore.RED}Error in Load.{Style.RESET_ALL}")
                    
                if rollno<args.end:
                    getresult(rollno+1)


            def validate_input(roll_no):
                try:
                    # Try to convert the input to an integer
                    roll_no = int(roll_no)
                    # Check if the length is exactly 10 digits
                    if len(str(roll_no)) == 10:
                        return roll_no
                    else:
                        print(f"{Fore.YELLOW}Roll number must be an integer of length 10.{Style.RESET_ALL}")
                        return None
                except ValueError:
                    print(f"{Fore.YELLOW}Roll number must be an integer.{Style.RESET_ALL}")
                    return None
                
            getresult(args.start)


        except KeyboardInterrupt:
            print(f"{Fore.BLUE}\nCtrl+C pressed. Exiting gracefully.{Style.RESET_ALL}")



    except argparse.ArgumentTypeError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
