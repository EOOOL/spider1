import requests
from bs4 import BeautifulSoup
import csv
import datetime

url = 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action?xmlname=1462259560614'

class pm_spider():
    def __init__(self,city,year):
        self.city = city
        self.year = year
        self.date = year+'-10-21'
        with open(self.city+"-"+self.year+".csv", "w", newline='') as excel_file:
            data_file = csv.writer(excel_file)
            data_file.writerow(['城市','日期','AQI指数','空气质量级别'])

    def date_add(self):
        now_date = datetime.datetime.strptime(self.date,'%Y-%m-%d')
        next_date = now_date + datetime.timedelta(days = 1)
        self.date = next_date.strftime('%Y-%m-%d')

    def get_content(self, url):
        response = requests.post(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'},
                                data={'CITY':self.city,'V_DATE':self.date,"E_DATE":self.date})
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
                data_file.writerow([i[0],i[2],i[1],i[3]])

    def start(self):
        print(url)
        for i in range(365):
            print("*" * 50)
            print("正在下载"+self.city+"第" + str(i + 1) + "天PM2.5数据")
            self.date_add()
            content = self.get_content(url)
            data = self.get_data(content)
            self.save_data(data)
            print(self.city + "第" + str(i + 1) + "天PM2.5数据下載完成")

if __name__=='__main__':
    spider = pm_spider('上海','2016')
    spider.start()