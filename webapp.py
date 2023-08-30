import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
import matplotlib.pyplot as plt
import pandas as pd
from pandas.errors import EmptyDataError 
import streamlit as st

st.image("CMAbg.png")
st.markdown("<h1 style='font-family: Montserrat Semi-Bold; text-align: center; color: white;'>CAREER MARKET ANALYZER</h1>", unsafe_allow_html=True)


if st.button("Press to Scrape Data"):

    driver = webdriver.Chrome()
    jobs={"roles":[],
        "companies":[],
        "locations":[],
        "experience":[],
        "skills":[]}
    for i in range(1):
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
                pass
                break
            except NameError:
                pass
            except NoSuchWindowException:
                pass

    DS_jobs_df=pd.DataFrame(jobs)
    DS_jobs_df.to_csv("final.csv")
    st.write("Scraping Done")
    



data=pd.read_csv("final.csv")


loc=data["locations"]
comp=data["skills"]
nameor=data["roles"]
nameoc=data["companies"]




res,res2,user,uskill,cskill,newx=[],[],[],[],[],[]
resloc,res2loc,userloc,uloc,cloc=[],[],[],[],[]
fin,finloc,chos=[],[],[]


for i in comp:
    res2.append(i.strip('][').split(', '))
for i in res2:
    for j in range(len(i)):
        i[j]=i[j].replace("'", "")
    x=set(i)
    cskill.append(x)
for i in cskill:
    for j in i:
        chos.append(j)
uskill=st.multiselect("Select your skill",set(chos))

if st.button("Compute Probability"):
    for i in cskill:
        match=len(i.intersection(uskill))
        c = round(match / len(i), 2)
        newx.append(float(c))
        fin.append((str(round(float(c),2)*100)+'%'))


probab=pd.DataFrame({"Company":nameoc,"Position":nameor,"Probability":fin})
st.dataframe(probab)

