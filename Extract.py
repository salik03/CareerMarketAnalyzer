#web scraping

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import matplotlib.pyplot as plt
driver = webdriver.Chrome()
jobs={"roles":[],
     "companies":[],
     "locations":[],
     "experience":[],
     "skills":[]}
for i in range(5):
        driver.get("https://www.naukri.com/jobs-in-india-{}".format(i))
        time.sleep(3)
        lst=driver.find_elements(By.CSS_SELECTOR, '.jobTuple.bgWhite.br4.mb-8')
        for job in lst:
            try:
                driver.implicitly_wait(3)
                role=job.find_element(By.CSS_SELECTOR,"a.title.fw500.ellipsis").text
                company=job.find_element(By.CSS_SELECTOR, "a.subTitle.ellipsis.fleft").text
                location=job.find_element(By.CSS_SELECTOR, ".fleft.grey-text.br2.placeHolderLi.location").text
                exp=job.find_element(By.CSS_SELECTOR, ".fleft.grey-text.br2.placeHolderLi.experience").text
                skills=job.find_element(By.CSS_SELECTOR, ".tags.has-description").text
                jobs["roles"].append(role)
                jobs["companies"].append(company)
#                 jobs["locations"].append(location)
                jobs["experience"].append(exp)
#                 jobs["skills"].append(skills)

                month,day=[],[]
                month.append(skills.lower())
                day.append(location.lower())

                for i in month:
                    x=(i.split('\n'))
                    jobs["skills"].append(x)
                    
                for j in day:
                    y=(j.split(','))
                    jobs["locations"].append(y)

            except NoSuchElementException:
                print("Scraping Done")
                break
            except NameError:
                pass
print("Scraping Done")
#CSV implementation
DS_jobs_df=pd.DataFrame(jobs)
DS_jobs_df.to_csv("final.csv")

data=pd.read_csv("final.csv")

#Manipulating the csv

loc = data["locations"]
comp=data["skills"]
nameor=data["roles"]
nameoc=data["companies"]
res,res2,user,uskill,cskill=[],[],[],[],[]
a = 'y'
while (a):
    user.append("'"+input("Enter Skill: ")+"'")
    a = input("Do you want to continue? (y/n)")
    print("\n")
    if (a=='y'):
        continue
    else:
        break
    
# for i in range(5):
#     user.append("'"+input("Enter Skill: ")+"'")
# print("\n")
       
for i in user:
    res.append(i.strip('][').split(', '))
for i in res:
    uskill.append(i[0])
uskill=set(uskill)


for i in comp:
    res2.append(i.strip('][').split(', '))
for i in res2:
    x=set(i)
    cskill.append(x)
    
fin=[]

for i in cskill:
    match=len(i.intersection(uskill))
    c = round(match / len(i), 2)
    fin.append(float(c))

    
    
    
for i in range(len(nameoc)):
    print(nameoc[i]," : ",nameor[i]," : ",fin[i]*100, "%")