import requests
import urllib.parse
import csv
from bs4 import BeautifulSoup
import datetime
import gzip
from io import StringIO

url = 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action?xmlname=1462259560614'

class pm_spider():
    def __init__(self,city,year):
        self.city = city
        self.year = year
        self.date = year+'-01-01'
        with open(self.city+"-"+self.year+".csv", "w", newline='') as excel_file:
            data_file = csv.writer(excel_file)
            data_file.writerow(['城市','AQI指数','首要污染物','日期','空气质量级别'])

    def date_plus(self):
        now_date = datetime.datetime.strptime(self.date,'%Y-%m-%d')
        next_date = now_date + datetime.timedelta(days = 1)
        self.date = next_date.strftime('%Y-%m-%d')

    def get_content(self, url):
        response = requests.post(url,data={'CITY':self.city,'V_DATE':self.date,"E_DATE":self.date,'Accept-Encoding': gzip})
        response = gzip.GzipFile(fileobj=StringIO(response.text), mode="r").read()
        return response

    def get_data(self, content):
        data_list = []
        soup = BeautifulSoup(content, 'lxml')
        soup = soup.find_all('tr', style="background-color:rgb(255,253,215);")
        for i in soup:
            temp_list = []
            soup_list = i.find_all('td')
            temp_list.append(soup_list[1].get_text())
            temp_list.append(soup_list[3].get_text())
            temp_list.append(soup_list[4].get_text())
            temp_list.append(soup_list[5].get_text())
            data_list.append(temp_list)
        data_list.pop(0)
        return data_list

    def save_data(self, data_list):
        with open(self.city+'-'+self.year+'.csv','a', newline='') as csv_file:
            data_file = csv.writer(csv_file)
            for i in data_list:
                data_file.writerow([self.city,i[0],i[1],i[2],i[3]])

    def start(self):
        print(url)
        for i in range(20):
            print("*" * 50)
            print("正在下载" + self.city + self.year + "年" + str(i + 1) + "月数据")
            self.date_plus()
            content = self.get_content(url)
            data = self.get_data(content)
            self.save_data(data)
            print(self.city + self.year + "年" +"第" + str(i + 1) + "天数据下載完成")

spider = pm_spider('上海','2016')
spider.start()