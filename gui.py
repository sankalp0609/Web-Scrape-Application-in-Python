# from tkinter import *
# from tkinter import ttk
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()


import tkinter as tk
from functools import partial
from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import openpyxl


def call_result(label_result, n1, n2):
    num1 = str((n1.get()))
    num2 = str((n2.get()))
    result = (num1+" "+num2)
    data = []
    driver = webdriver.Chrome(
        "F:\sankalp\PROJS\PyCharm Projs\chromedriver.exe")
    driver.get("https://clutch.co/")
    time.sleep(2)
    searchBox = driver.find_element(by.ID, "services")
    locBox = driver.find_element(by.ID, "location")
    submitBtn = driver.find_element(by.ID, "submit")
    time.sleep(1)
    searchBox.click()
    time.sleep(1)
    searchBox.send_keys(num1)
    time.sleep(3)
    locBox.click()
    time.sleep(1)
    locBox.send_keys(num2)
    time.sleep(1)
    submitBtn.click()
    time.sleep(3)
    if loc != "":
        # fileName= f"{num}_{loc}.xlsx"
        fileName = f'''{num1}_{num2}.xlsx'''
        innerLocBox = driver.find_element(by.ID, "location_input")
        time.sleep(1)
        innerLocBox.click()
        time.sleep(1)
        innerLocBox.send_keys(num2)
        time.sleep(1)
        innerLocBox.send_keys(Keys.ENTER)
        time.sleep(1)
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
                salary = job.find('div', class_="list-item block_tag custom_popover").text.strip().replace('$', '')
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
                item = {"Company Name": comp_name, "Salary in $": salary, "Hourly Wage": perHour, "Rating": rating,
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
                    item = {"Company Name": comp_name, "Salary in $": salary, "Hourly Wage": perHour, "Rating": rating,
                        "Number of Employees": employeeNum, "Location": location}
                    data.append(item)


    else:
        # time.sleep(3)
        fileName = f"{num1}_AllLocation.xlsx"
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
                item = {"Company Name": comp_name, "Salary in $": salary, "Hourly Wage": perHour, "Rating": rating,
                    "Number of Employees": employeeNum, "Location": location}
                data.append(item)

    p = pd.DataFrame(data)
    p.to_excel(fileName)
    label_result.config(text="file created")
    return


root = tk.Tk()
root.geometry('400x400')
root.title('Clutch Scraper')
search = tk.StringVar()
loc = tk.StringVar()
searchLable = tk.Label(root, text="Search Field: ").place(x=105, y=80)
NoteLable = tk.Label(root, text="(For all Location press spacebar and Enter)").place(x=105, y=140)
locLable = tk.Label(root, text="Location:").place(x=105, y=160)
labelResult = tk.Label(root)
labelResult.place(x=105, y=255)
searchEntry = tk.Entry(root,width=30, textvariable=search).place(x=108, y=102)
locEntry = tk.Entry(root,width=30, textvariable=loc).place(x=108,y=182)
call_result = partial(call_result, labelResult, search, loc)
buttonCal = tk.Button(root, text="scrape",width=13,command=call_result).place(x=183,y=225)
root.mainloop()
