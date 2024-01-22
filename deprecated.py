from ast import AugAssign, FormattedValue
from enum import auto
from selenium import webdriver
import time
import math
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from operator import attrgetter
from bs4 import BeautifulSoup

semNo=input("Enter semester number: ")

resultFile=open(f"{semNo}_Final.txt","a+")
driver=webdriver.Safari(executable_path='/usr/bin/safaridriver')



class Student:
    def __init__(self,roll,name,whitePad,cgpa):
        self.roll = roll
        self.name=name
        self.whitePad=whitePad
        self.cgpa=cgpa

def floatConvert(cgpa):
	num=0
	deciFlag=False
	count=0
	for l in cgpa:
		if l=='.':
			deciFlag=True
		else:
			if deciFlag==False:
				num=num*10+int(l)
			else:
				count+=1
				num+=int(l)*(1/(10**count))
	return round(num,2)

studentInfo=[]
#abhay shukla 12620001001
#zeeshar shakel 12620001181
#autonomy_roll_range=(12620001001,12620001181+1)
#autonomy_roll_range=(12621010001,12621001163+1)

#autonomy_roll_range=(12618001001,12618001186+1)
#autonomy_roll_range=(12619001114,12619001186+1)

# autonomy_roll_range=(12622001001,12622001181)
autonomy_roll_range=(12620001001,12620001181)#CSE
# autonomy_roll_range=(12620017002,12620017061)#CSBS
# autonomy_roll_range=(12621001164,12621001187+1)#CSE_Lateral
# autonomy_roll_range=(12620002001,12620002062+1)#IT 
# autonomy_roll_range=(12620003001,12620003179+1)#ECE
# autonomy_roll_range=(12620004000,12620004060)#BT
# autonomy_roll_range=(12620005001,12620005061)#AEIE
# autonomy_roll_range=(12620006001,12620006053)#CHEM
# autonomy_roll_range=(12620007001,12620007105)#ME
# autonomy_roll_range=(12620016001,12620016060)#EE
# autonomy_roll_range=(12620013001,12620013104)#CE






#range ends on the second last roll, ---warning and error----
for roll in range(*autonomy_roll_range):  
    driver.get("http://136.232.2.202:8084/stud22o.aspx")
   
    inputRoll=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='form1']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/input")))
    inputSemOpt=driver.find_element_by_name("sem")


    inputRoll.send_keys(roll)
    inputSemOpt.send_keys(f"{semNo}")#semester number
    
    
    showResultBtn=driver.find_element_by_name("Button1")
    showResultBtn.click()
  
    name=""
    autonomy_roll=""
    cgpa=""
    
    try:
        name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='lblname']"))).text
        autonomy_roll = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='lblroll']"))).text
        cgpa = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='lblbottom3']"))).text
    except:
        continue
    else:
        name=name[6:len(name)+1]
        autonomy_roll=autonomy_roll[10:21]
        cgpa=cgpa[22:len(cgpa)+1]#31,22
        whitePad=" "*(30-len(name))
    
        
        


        studentObj=Student(autonomy_roll,name,whitePad,float(cgpa))
        # studentObj=Student(autonomy_roll,name,whitePad,10.00)
        
        studentInfo.append(studentObj)
        print(studentObj.name)
        print(studentObj.roll)
        print(studentObj.cgpa)

studentInfo=sorted(studentInfo, key=lambda x: x.cgpa, reverse=True)

rank=0
globalCgpa=0
for student in studentInfo:
    if(globalCgpa!=student.cgpa):
        rank+=1
    resultFile.write(f"{rank}       {student.roll}        {student.name}{student.whitePad}     {student.cgpa}\n")
    
    globalCgpa=student.cgpa
driver.quit()
resultFile.close
