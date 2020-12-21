import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

company_url = []
company_list = {}


iban=requests.get(alba_url)

soup = BeautifulSoup(iban.text, "html.parser")
super_brand = soup.find("div",{"id":"MainSuperBrand"})
company = super_brand.find_all("li",{"class":"impact"})
for link in company:
    c_link = link.find("a")['href']
    c_title = link.find("a").find("span",{"class":"company"})
    company_list['title'] = c_title.string
    company_list['url'] = c_link
    company_url.append(company_list)
    company_list = {}

# print(company_url)

def save_csv(title, jobs):
  file = open(f'{title}.csv', mode='w')
  writer = csv.writer(file)
  writer.writerow(["place","title","time","pay","date"])
  for i in jobs:
    writer.writerow(list(i.values()))

def get_jobs(title, url):
  jobs = []
  row = {}
  request = requests.get(url)
  soup = BeautifulSoup(request.text, "html.parser")
  job_list = soup.find("div", {"id":"NormalInfo"}).find("tbody")
  detail = job_list.find_all("tr",{"class":""})
  # print(detail)
  for i in detail:
    # print(i, "\n\n\n\n")
    # if i:
    if (i.find('td',{"class":"local"})) is not None:
      job_temp = i.find('td',{"class":"local"}).text
      job_place = job_temp.replace("\\xa0"," ")

      job_title = i.find('td',{"class":"title"}).find('span',{"class":"company"}).text

      if (i.find('td',{"class":"data"}).find('span',{"class":"time"})) is not None:
        job_time = i.find('td',{"class":"data"}).find('span',{"class":"time"}).text
      else:
        job_time = " "

      if (i.find('td',{"class":"pay"}).find('span',{"class":"number"})) is not None:
        job_pay = i.find('td',{"class":"pay"}).find('span',{"class":"number"}).text
      else:
        job_pay = " "

      job_date = i.find('td',{"class":"regDate"}).text
      
      row['place'] = job_place
      row['title'] = job_title
      row['time'] = job_time
      row['pay'] = job_pay
      row['date'] = job_date
      # print(row)
      jobs.append(row)
      row={}
      save_csv(title,jobs)

for com_link in company_url:
  title = com_link['title']
  url = com_link['url']
  get_jobs(title, url)

    # save_csv(title, url)
  # print(title, url)
  # def save_csv(title, url):
  
# print(detail)
