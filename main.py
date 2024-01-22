# Interpreter: Python 3.9.7 (conda)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os

semNo=input("Enter semester number: ")
directory_path = f"./SEM {semNo} 2020-2024"
os.makedirs(directory_path)

driver=webdriver.Safari(executable_path='/usr/bin/safaridriver')

class Student:
    def __init__(self,roll,name,whitePad,cgpa):
        self.roll = roll
        self.name=name
        self.whitePad=whitePad
        self.cgpa=cgpa

# Assuming you have a list of department names corresponding to each range
departments = ["CSE", "CSBS", "CSE_Lateral", "IT", "ECE", "BT", "AEIE", "CHEM", "ME", "EE", "CE"]
i=0
for autonomy_roll_range in [(12620001001,  12620001182), (12620017002, 12620017062), (12621001164, 12621001188),
                            (12620002001, 12620002063), (12620003001, 12620003180), (12620004000, 12620004061),
                            (12620005001, 12620005062), (12620006001, 12620006054), (12620007001, 12620007106),
                            (12620016001, 12620016061), (12620013001, 12620013105)]:

    start, end = autonomy_roll_range
    studentInfo=[]

    for current_autonomy_roll in range(start, end):

        driver.get("http://136.232.2.202:8084/stud24o.aspx")

        inputRoll=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='form1']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/input")))
        inputSemOpt=driver.find_element_by_name("sem")

        inputRoll.send_keys(current_autonomy_roll)
        inputSemOpt.send_keys(f"{semNo}")#semester number
        
        
        # Wait for the presence of the showResultBtn element
        showResultBtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Button1")))
        showResultBtn.click()
    
        name=""
        autonomy_roll=""
        cgpaText=""
        cgpa=-1
        try:
            name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='lblname']"))).text
            autonomy_roll = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='lblroll']"))).text
            cgpaText = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='lblbottom1']"))).text
        except:
            continue
        else:
            name=name[6:len(name)+1]
            autonomy_roll=autonomy_roll[10:21]

            # Define a regular expression pattern to match decimal values
            pattern = r'\b\d+\.?\d*'

            # Use re.findall to find all matches in the text
            matches = re.findall(pattern,cgpaText)

            if matches:
                cgpa = float(matches[-1])
                #print(cgpa)
            else:
                print("No decimal value found.")
                
            whitePad=" "*(30-len(name))
        
            studentObj=Student(autonomy_roll,name,whitePad,cgpa)
            
            studentInfo.append(studentObj)
            print(studentObj.name)
            print(studentObj.roll)
            print(studentObj.cgpa)
            print()

    studentInfo=sorted(studentInfo, key=lambda x: x.cgpa, reverse=True)

    dept_name = departments[i]

    # Assuming you want to store files with the department name in the filename
    filename = f"./{directory_path}/{dept_name}.txt"

    # Write your logic to store the files or perform any other actions
    with open(filename, 'a+') as file:
        file.write(f"This file is for {dept_name} department with roll range {start} to {end}\n")

        rank=0
        globalCgpa=0
        for student in studentInfo:
            if(globalCgpa!=student.cgpa):
                rank+=1
            file.write(f"{rank}       {student.roll}        {student.name}{student.whitePad}     {student.cgpa}\n")
            
            globalCgpa=student.cgpa
    studentInfo=[]
    file.close
    i+=1

driver.quit()