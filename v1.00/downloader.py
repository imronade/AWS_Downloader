# September, 18 2020
# Created by Imron Ade

import requests
import csv
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import os
import calendar
from dateutil.relativedelta import relativedelta

# Welcoming Message
print("===========================================================")
print("AWS CENTER DOWNLOADER V.1.00")
print("September, 18 2020")
print("===========================================================")

# setting up output folder
# make folder based on current Date
currentDate = date.today()
currentDate = currentDate.strftime("%Y%m%d")

CHECK_FOLDER = os.path.isdir("output/"+currentDate)
# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs("output/"+currentDate)
    print("created folder : ", "output/"+currentDate)

else:
    print("output/"+currentDate, "folder already exists.")

# setting up the date
print("Pastikan isi dengan benar ya")
tahun = str(input("Masukkan tahun (Contoh: 2020): "))
bulan = str(input("Masukkan bulan (Contoh: 08): "))
tanggal = str(input("Masukkan tanggal mulai (Contoh: 01): "))

initialDate = tahun+"-"+bulan+"-"+tanggal
akhirbulan = calendar.monthrange(int(tahun), int(bulan))[1]

# processing to download data
i = int(tanggal)
while i <= akhirbulan:
    tanggal_i = i
    i = i + 10
    initialDate = tahun+"-"+bulan+"-"+str(tanggal_i)
    initialDate_obj = datetime.strptime(initialDate, '%Y-%m-%d')
    endDate_obj = initialDate_obj+timedelta(days=9)
    endDate = endDate_obj.strftime("%Y-%m-%d")
    
    if endDate_obj.month > initialDate_obj.month:
        endDate_obj = initialDate_obj + relativedelta(day=31)
        endDate = endDate_obj.strftime("%Y-%m-%d")

    if __name__ == "__main__":
        url = "http://202.90.198.206/aws/accessdata/show_data"
        body = {
            "tipe_alat": "AWS",
            "kota": "K00388",
            "provinsi": "PR026",
            "start": initialDate,
            "end": endDate,
            "station": "160018",
        }
        cookies = dict(ci_session="75b56c2034b85a392323545158eec281180df5cc")
        r = requests.post(url, cookies=cookies, data=body)

        raw_html = r.text

        soup = BeautifulSoup(raw_html, "lxml")

        headers = [th.string for th in soup.find_all('th')]
        trs = soup.find_all('tr')

        with open("output/"+currentDate+"/"+currentDate+"_"+initialDate+"_"+endDate+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for tr in trs:
                writer.writerow([td.string for td in tr.find_all('td')])

        print(currentDate+"_"+initialDate+"_"+endDate+".csv Downloaded")

    
