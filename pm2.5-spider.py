import requests
import csv
from bs4 import BeautifulSoup
import datetime
from http import cookiejar

url = 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action?xmlname=1462259560614'

session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
try:
        session.cookies.load(ignore_discard=True)
except :
        print("load cookies failed")
class pm_spider():
    def __init__(self,city,year):
        self.city = city
        self.year = year
        self.date = year+'-01-01'
        with open(self.city+"-"+self.year+".csv", "w", newline='') as excel_file:
            data_file = csv.writer(excel_file)
            data_file.writerow(['城市','AQI指数','空气质量级别','日期'])

    def date_plus(self):
        now_date = datetime.datetime.strptime(self.date,'%Y-%m-%d')
        next_date = now_date + datetime.timedelta(days = 1)
        self.date = next_date.strftime('%Y-%m-%d')

    def get_content(self, url):
        response = session.post(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'},
                                data={'CITY':self.city,'V_DATE':self.date,"E_DATE":self.date})
        session.cookies.save()
        return response.text

    def get_data(self, content):
        data_list = []
        soup = BeautifulSoup(content, 'lxml')
        soup = soup.find_all('tr', onmouseover="this.style.backgroundColor='#FFFDD7'")
        for i in soup:
            temp_list = []
            soup_list = i.find_all('td')
            temp_list.append(soup_list[2].get_text())
            temp_list.append(soup_list[3].get_text())
            temp_list.append(soup_list[6].get_text())
            temp_list.append(soup_list[8].get_text())
            data_list.append(temp_list)
        return data_list

    def save_data(self, data_list):
        with open(self.city+'-'+self.year+'.csv','a', newline='') as csv_file:
            data_file = csv.writer(csv_file)
            for i in data_list:
                data_file.writerow([i[0],i[1],i[3],i[2]])

    def start(self):
        print(url)
        for i in range(365):
            print("*" * 50)
            print("正在下载" + self.city + self.year + "年第" + str(i + 1) + "天数据")
            self.date_plus()
            content = self.get_content(url)
            data = self.get_data(content)
            print(data)
            self.save_data(data)
            print(self.city + self.year + "年" +"第" + str(i + 1) + "天数据下載完成")

if __name__=='__main__':
    spider = pm_spider('上海','2016')
    spider.start()