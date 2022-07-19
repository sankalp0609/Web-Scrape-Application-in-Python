# Created by Yashvi Bhatt and Sankalp Chhunchha
# Date created: 13/07/2022
# It was fun making this project.
# This is a Gui application that can scrape data from
# LinkedIn and Clutch
# IF YOU WANT TO GET ALL LOCATION DATA FROM SCRAPE JUST PRESS ENTER
#

import tkinter as tk
from tkinter import *
from functools import partial
from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import openpyxl

data=[]
def call_result(label_result,n1,n2,n3):
    search = str(n1.get())
    loc = str(n2.get())
    platform = n3.get()
    print(platform)
    driver = webdriver.Chrome("YOUR CHROME EXE PATH HERE")
    if (search=="" and loc==""):
        label_result.config(text="Please Enter Field and Location!")
        return
    elif(search=="" and loc!=""):
        label_result.config(text="Please Enter search Field")
        return
    else:
        # label_result.config(text="Please enter search Field and location")
        if platform == "LinkedIn":
            if loc=="":
                label_result.config(text="Please enter Location for LinkedIn")
                return
            else:
                username = "YOUR LINKEDIN EMAIL HERE"
                password = "YOUR LINKEDIN PASSWORD HERE"
                driver.get("https://www.linkedin.com/")
                emailField = driver.find_element(by.NAME, "session_key")
                passField = driver.find_element(by.NAME, "session_password")
                signInBtn = driver.find_element(by.XPATH, "//*[@id='main-content']/section[1]/div/div/form/button")
                time.sleep(2)
                emailField.send_keys(username)
                passField.send_keys(password)
                time.sleep(1)
                signInBtn.click()
                time.sleep(3)
                searchBox = driver.find_element(by.XPATH, "/html/body/div[6]/header/div/div/div/div[1]/input")
                time.sleep(2)
                searchBox.click()
                time.sleep(1)
                searchBox.send_keys(search)
                time.sleep(2)
                searchBox.send_keys(Keys.ENTER)
                time.sleep(3)
                inJobs = driver.find_element(by.XPATH,"/html/body/div[6]/div[3]/div[2]/section/div/nav/div/ul/li[4]/button")
                time.sleep(1)
                inJobs.click()
                time.sleep(2)
                locBox = driver.find_element(by.XPATH,"/html/body/div[6]/header/div/div/div/div[2]/div[2]/div/div/input[1]")
                finalClick = driver.find_element(by.XPATH, "/html/body/div[6]/header/div/div/div/div[2]/button[1]")
                locBox.click()
                time.sleep(2)
                locBox.clear()
                time.sleep(2)
                locBox.send_keys(loc)
                time.sleep(2)
                finalClick.send_keys(Keys.ENTER)
                time.sleep(3)
                pSource = BeautifulSoup(driver.page_source, 'lxml')
                maxPageLen = pSource.find('ul', class_='artdeco-pagination__pages artdeco-pagination__pages--number').findAll('li',class_='artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view')
                maxNum = int(maxPageLen[8].span.text)
                maxRange = range(1, maxNum + 1)
                fileName = f'''LinkedIn_{search}_{loc}.xlsx'''
                for i in maxRange:
                    if i <=9:
                        try:
                            pagination = driver.find_element(by.XPATH,
                                                             "/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[7]/ul/li[{}]/button".format(
                                                                 i))
                            time.sleep(2)
                            print(i)
                            pagination.click()
                            time.sleep(2)
                            for j in range(1, 26):
                                time.sleep(2)
                                # Scrapping the data
                                try:
                                    allLiElem = driver.find_element(by.XPATH,
                                                                    "/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{}]/div/div[1]/div[1]/div[2]/div[1]".format(
                                                                        j))
                                except:
                                    pass
                                time.sleep(1)
                                allLiElem.click()
                                time.sleep(2)
                                soup = BeautifulSoup(driver.page_source, 'lxml')
                                rightSection = soup.find('section', class_="jobs-search__right-rail")
                                time.sleep(2)
                                try:
                                    # compName = leftSection.find('a',class_='job-card-container__link job-card-container__company-name ember-view').text.strip()
                                    compName = rightSection.find('span',
                                                                 class_='jobs-unified-top-card__company-name').a.text.strip()
                                except:
                                    compName = None
                                try:
                                    # compLoc = leftSection.find('li', class_='job-card-container__metadata-item').text.strip()
                                    compLoc = rightSection.find('span',
                                                                class_='jobs-unified-top-card__bullet').text.strip()
                                except:
                                    compLoc = None
                                try:
                                    items = rightSection.findAll('li', class_="jobs-unified-top-card__job-insight")
                                except:
                                    items = None
                                try:
                                    jobType = items[0].span.text.strip()
                                except:
                                    jobType = None
                                try:
                                    employeeNum = items[1].span.text.strip()
                                except:
                                    employeeNum = None
                                item = {"Company Name": compName, "Location": compLoc, "Job Type": jobType,
                                        "Number of Employees": employeeNum}
                                data.append(item)
                        except:
                            print("Failed")

                    elif i>1:
                        pagination = driver.find_element(by.XPATH,
                                                         '/html/body/div[6]/div[3]/div[4]/div/div/main/div/section[1]/div/div[7]/ul/li[{}]/button'.format(
                                                             i))
                        time.sleep(1)
                        print(maxNum)
                        pagination.click()
                        time.sleep(1)
                    elif i > 9 and i <= (maxNum - 7):
                        pagination = driver.find_element(by.XPATH,'/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/div[6]/ul/li[7]/button')
                        time.sleep(1)
                        pagination.click()
                        time.sleep(1)
                        for j in range(1, 26):
                            # Scrapping the data
                            allLiElem = driver.find_element(by.XPATH,
                                                            "/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{}]/div/div[1]/div[1]/div[2]/div[1]/a".format(
                                                                j))
                            time.sleep(1)
                            allLiElem.click()
                            time.sleep(2)
                            soup = BeautifulSoup(driver.page_source, 'lxml')
                            # leftSection = soup.findAll('li', class_="jobs-search-results__list-item occludable-update p0 relative ember-view")
                            compName = rightSection.find('a', class_='ember-view t-black t-normal').text.strip()
                            compLoc = rightSection.find('span', class_='jobs-unified-top-card__bullet').text.strip()
                            items = rightSection.findAll('li', class_="jobs-unified-top-card__job-insight")
                            jobType = items[0].span.text.strip()
                            employeeNum = items[1].span.text.strip()
                            item = {"Company Name": compName, "Location": compLoc, "Job Type": jobType,
                                    "Number of Employees": employeeNum}
                            data.append(item)
                            time.sleep(2)
                    elif i > (maxNum - 7) and i <= maxNum:
                        k = range(4, 11)
                        for a in k:
                            pagination = driver.find_element(by.XPATH,
                                                             "/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/div[7]/ul/li[{}]/button".format(
                                                                 a))
                            time.sleep(1)
                            pagination.click()
                            time.sleep(2)
                            for b in range(1, 26):
                                # Scrapping the data
                                allLiElem = driver.find_element(by.XPATH,
                                                                "/html/body/div[5]/div[3]/div[4]/div/div/main/div/section[1]/div/ul/li[{}]/div/div[1]/div[1]/div[2]/div[1]/a".format(
                                                                    b))
                                time.sleep(1)
                                allLiElem.click()
                                time.sleep(2)
                                soup = BeautifulSoup(driver.page_source, 'lxml')
                                # leftSection = soup.findAll('li', class_="jobs-search-results__list-item occludable-update p0 relative ember-view")
                                try:
                                    rightSection = soup.find('section', class_="jobs-search__right-rail")
                                except:
                                    pass
                                try:
                                    compName = rightSection.find('a', class_='ember-view t-black t-normal').text.strip()
                                except:
                                    pass
                                try:
                                    compLoc = rightSection.find('span',
                                                                class_='jobs-unified-top-card__bullet').text.strip()
                                except:
                                    pass
                                try:
                                    items = rightSection.findAll('li', class_="jobs-unified-top-card__job-insight")
                                except:
                                    pass
                                try:
                                    jobType = items[0].span.text.strip()
                                except:
                                    pass
                                try:
                                    employeeNum = items[1].span.text.strip()
                                except:
                                    pass
                                item = {"Company Name": compName, "Location": compLoc, "Job Type": jobType,
                                        "Number of Employees": employeeNum}
                                data.append(item)
                                time.sleep(2)
                p = pd.DataFrame(data)
                p.to_excel(fileName)
                label_result.config(text=f'''LinkedIn_{search}_{loc}.xlsx file created''')
        elif platform == "Clutch":
            driver.get("https://clutch.co/")
            searchBox = driver.find_element(by.ID, "services")
            locBox = driver.find_element(by.ID, "location")
            submitBtn = driver.find_element(by.ID, "submit")
            time.sleep(1)
            searchBox.click()
            time.sleep(1)
            searchBox.send_keys(search)
            time.sleep(3)
            locBox.click()
            time.sleep(1)
            locBox.send_keys(loc)
            time.sleep(1)
            submitBtn.click()
            time.sleep(3)
            if loc=="":
                fileName = f'''Clutch_{search}_AllLocation.xlsx'''
                url = str(driver.current_url)
                url += "?page={}"
                soup = BeautifulSoup(driver.page_source, 'lxml')
                lastLi = soup.find('li', class_="page-item last")
                lastPageNum = int(lastLi.a['data-page'])
                lastPage = range(0, lastPageNum + 1)
                for i in lastPage:
                    text = requests.get(url.format(i)).text
                    soup = BeautifulSoup(text, 'lxml')
                    jobs = soup.findAll(
                        'div', class_="provider-info col-md-10 secondary-bar")
                    for job in jobs:
                        comp_name = job.find('a', class_="company_title").text.strip()
                        salary = job.find(
                            'div', class_="list-item block_tag custom_popover").text.strip().replace('$', '')
                        try:
                            employees = job.findAll(
                                'div', class_="list-item custom_popover")
                        except:
                            employees = None
                        try:
                            rating = job.find(
                                'span', class_='rating sg-rating__number').text.strip()
                        except:
                            rating = None
                        try:
                            perHour = employees[0].span.text.replace(' ', '')
                        except:
                            perHour = None
                        try:
                            employeeNum = employees[1].span.text.replace(' ', '')
                        except:
                            employeeNum = None
                        try:
                            location = employees[2].span.text.replace(' ', '')
                        except:
                            location = None
                        item = {"Company Name": comp_name, "Salary in $": salary, "Hourly Wage": perHour,
                                "Rating": rating,
                                "Number of Employees": employeeNum, "Location": location}
                        data.append(item)
                p = pd.DataFrame(data)
                p.to_excel(fileName)
                label_result.config(text=f'''Clutch_{search}_AllLocations.xlsx file created''')
                return
            else:
                fileName = f'''Clutch_{search}_{loc}.xlsx'''
                innerLocBox = driver.find_element(by.ID, "location_input")
                time.sleep(1)
                innerLocBox.click()
                time.sleep(1)
                innerLocBox.send_keys(loc)
                time.sleep(1)
                innerLocBox.send_keys(Keys.ENTER)
                url = str(driver.current_url)
                url += "?page={}"
                soup = BeautifulSoup(driver.page_source, 'lxml')
                try:
                    lastLi = soup.find('li', class_="page-item last")
                    lastPageNum = int(lastLi.a['data-page'])
                    lastPage = range(0, lastPageNum + 1)
                except:
                    lastLi = None
                if lastLi == None:
                    text = requests.get(driver.current_url).text
                    soup = BeautifulSoup(text, 'lxml')
                    jobs = soup.findAll('div', class_="provider-info col-md-10 secondary-bar")
                    for job in jobs:
                        comp_name = job.find('a', class_="company_title").text.strip()
                        salary = job.find('div', class_="list-item block_tag custom_popover").text.strip().replace('$',
                                                                                                                   '')
                        try:
                            employees = job.findAll('div', class_="list-item custom_popover")
                        except:
                            employees = None
                        try:
                            rating = job.find('span', class_='rating sg-rating__number').text.strip()
                        except:
                            rating = None
                        try:
                            perHour = employees[0].span.text.replace(' ', '')
                        except:
                            perHour = None
                        try:
                            employeeNum = employees[1].span.text.replace(' ', '')
                        except:
                            employeeNum = None
                        try:
                            location = employees[2].span.text.replace(' ', '')
                        except:
                            location = None
                        item = {"Company Name": comp_name, "Salary in $": salary, "Hourly Wage": perHour,
                                "Rating": rating,
                                "Number of Employees": employeeNum, "Location": location}
                        data.append(item)
                else:
                    for i in lastPage:
                        text = requests.get(url.format(i)).text
                        soup = BeautifulSoup(text, 'lxml')
                        jobs = soup.findAll(
                            'div', class_="provider-info col-md-10 secondary-bar")
                        for job in jobs:
                            comp_name = job.find('a', class_="company_title").text.strip()
                            salary = job.find(
                                'div', class_="list-item block_tag custom_popover").text.strip().replace('$', '')
                            try:
                                employees = job.findAll(
                                    'div', class_="list-item custom_popover")
                            except:
                                employees = None
                            try:
                                rating = job.find(
                                    'span', class_='rating sg-rating__number').text.strip()
                            except:
                                rating = None
                            try:
                                perHour = employees[0].span.text.replace(' ', '')
                            except:
                                perHour = None
                            try:
                                employeeNum = employees[1].span.text.replace(' ', '')
                            except:
                                employeeNum = None
                            try:
                                location = employees[2].span.text.replace(' ', '')
                            except:
                                location = None
                            item = {"Company Name": comp_name, "Salary in $": salary, "Hourly Wage": perHour,
                                    "Rating": rating,
                                    "Number of Employees": employeeNum, "Location": location}
                            data.append(item)
                p = pd.DataFrame(data)
                p.to_excel(fileName)
                label_result.config(text=f'''Clutch_{search}_{loc}.xlsx file created''')
                return
        else:
            label_result.config(text="Please select a platform!")
            return
        return

root = tk.Tk()
root.geometry("400x400")
root.title("Scraper")
root.resizable(False,False)
searchType = tk.StringVar()
locType = tk.StringVar()
clicked = StringVar()
clicked.set("Platform")
searchLable = tk.Label(root,text="Search Field: ").place(x=105, y=80)
NoteLable = tk.Label(root, text="(Clutch: For all Location leave location field empty)").place(x=90, y=140)
locLable = tk.Label(root, text="Location:").place(x=105, y=160)
labelResult = tk.Label(root)
labelResult.place(x=75, y=295)
searchEntry = tk.Entry(root, width=30, textvariable=searchType).place(x=108, y=102)
locEntry = tk.Entry(root, width=30, textvariable=locType).place(x=108, y=182)
drop = OptionMenu(root,clicked,"LinkedIn","Clutch").place(x=105,y=210)
call_result = partial(call_result,labelResult,searchType,locType,clicked)
buttonS = Button(root,text="Scrape", width=13,command=call_result).place(x=153,y=255)
root.mainloop()
