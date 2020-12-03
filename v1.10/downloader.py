# December, 02 2020
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
print("AWS CENTER DOWNLOADER V.1.10")
print("December, 02 2020")
print("===========================================================")

#%% Preparing data
# setting up output folder
# make folder based on current Date
currentDate = date.today()
currentDate = currentDate.strftime("%Y%m%d")

CHECK_FOLDER = os.path.isdir("output/stand_alone/"+currentDate)
# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs("output/stand_alone/"+currentDate)
    print("created folder : ", "output/stand_alone/"+currentDate)

else:
    print("output/stand_alone/"+currentDate, "folder already exists.")

# setting up the date
print("Pastikan isi dengan benar ya")
tahun = str(input("Masukkan tahun (Contoh: 2020): "))
bulan = str(input("Masukkan bulan (Contoh: 08): "))
tanggal = str(input("Masukkan tanggal mulai (Contoh: 01): "))

initialDate = tahun+"-"+bulan+"-"+tanggal
akhirbulan = calendar.monthrange(int(tahun), int(bulan))[1]

#%% Starting download files
# processing to download data
waktu = []
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
        cookies = dict(ci_session="935d11dee9c0ea6a933bb9365430f27d2dd0a0a2")
        r = requests.post(url, cookies=cookies, data=body)

        raw_html = r.text

        soup = BeautifulSoup(raw_html, "lxml")

        headers = [th.string for th in soup.find_all('th')]
        trs = soup.find_all('tr')

        with open("output/stand_alone/"+currentDate+"/"+currentDate+"_"+initialDate+"_"+endDate+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for tr in trs:
                writer.writerow([td.string for td in tr.find_all('td')])
        
        waktu += [currentDate+"_"+initialDate+"_"+endDate+".csv"]
        print(currentDate+"_"+initialDate+"_"+endDate+".csv Downloaded")

#%% Merging csv files
# import libraries
import glob
import pandas as pd

# setting up folder
path = os.getcwd()
path_data = path+"\\output\\stand_alone\\"+currentDate+"\\"
path_simpan = path+"\\output\\merged\\"+currentDate+"\\"

CHECK_FOLDER = os.path.isdir("output/merged/"+currentDate)
# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs("output/merged/"+currentDate)
    print("created folder : ", "output/merged/"+currentDate)

else:
    print("output/merged/"+currentDate, "folder already exists.")

filenames = []
for t in waktu:
    filename = glob.glob(os.path.join(path_data, t))
    filenames += filename

# filenames = glob.glob(os.path.join(path_data,"*.csv"))
df_from_each_file = (pd.read_csv(f, sep=',') for f in filenames)
df_merged   = pd.concat(df_from_each_file, ignore_index=True)
df_merged.to_csv(path_simpan+currentDate+"_start_data_"+tahun+bulan+tanggal+"_merged.csv")
print("Files merged")
