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
print("AWS CENTER DOWNLOADER V.1.20")
print("March, 01 2021")
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

# list stations
alats = ["AAWS","ARG","AWS"]
stations = ["AAWS0327","AAWS0326","AAWS0328", "AAWS0341",
            "150349","150350","150090","150210","150091","150211","150351",
            "STA0096","14032789","14032788", "150212","STAL271","STAL272","STAL273",
            "160037","STA2096","160018", "14063120","160038"]
names = ["AAWS Luwuk Banggai","AAWS Donggala","AAWS Parigi Moutong","AAWS Sidondo",
        "ARG Tanamea","ARG Karyamukti","ARG Dolo Barat","ARG Palolo","Arg Kulawi","ARG Kilo","ARG Ratolindo",
        "ARG Poso","ARG Petasia","ARG Bungku Tengah","ARG Bahodopi","ARG BPBD Donggala","ARG UPTD Ampibabo","ARG BPP Simpang Raya",
         "AWS Lalundu","AWS Labuan","AWS GAW Bariri","AWS Lore Piore","AWS Dolago"]
#%% Starting download files
# processing to download data
kuki = "a20d4a2a2f37c7afcf66c3dcce0028f6eb6dfb3d"
for alat in alats:
    if alat == "AAWS":
        id_station = stations[0:4]
        nama_station = names[0:4]   
        for station,nama_stasiun in zip(id_station, nama_station):
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
                        "tipe_alat": alat,
                        "provinsi": "PR026",
                        "start": initialDate,
                        "end": endDate,
                        "station": station,
                    }
                    cookies = dict(ci_session= kuki)
                    r = requests.post(url, cookies=cookies, data=body)
            
                    raw_html = r.text
            
                    soup = BeautifulSoup(raw_html, "lxml")
            
                    headers = [th.string for th in soup.find_all('th')]
                    trs = soup.find_all('tr')
            
                    with open("output/stand_alone/"+currentDate+"/"+station+"_"+currentDate+"_"+initialDate+"_"+endDate+".csv", 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(headers)
                        for tr in trs:
                            writer.writerow([td.string for td in tr.find_all('td')])
                    
                    waktu += [station+"_"+currentDate+"_"+initialDate+"_"+endDate+".csv"]
                    print(station+"_"+nama_stasiun+"_"+currentDate+"_"+initialDate+"_"+endDate+".csv Downloaded")
            
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
            df_merged.to_csv(path_simpan+nama_stasiun+"_"+station+"_"+currentDate+"_start_data_"+tahun+bulan+tanggal+"_merged.csv")
            print("Files merged")

    elif alat =="ARG":
        id_station = stations[4:18]
        nama_station = names[4:18]
        for station,nama_stasiun in zip(id_station, nama_station):
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
                        "tipe_alat": alat,
                        "provinsi": "PR026",
                        "start": initialDate,
                        "end": endDate,
                        "station": station,
                    }
                    cookies = dict(ci_session= kuki)
                    r = requests.post(url, cookies=cookies, data=body)
            
                    raw_html = r.text
            
                    soup = BeautifulSoup(raw_html, "lxml")
            
                    headers = [th.string for th in soup.find_all('th')]
                    trs = soup.find_all('tr')
            
                    with open("output/stand_alone/"+currentDate+"/"+station+"_"+currentDate+"_"+initialDate+"_"+endDate+".csv", 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(headers)
                        for tr in trs:
                            writer.writerow([td.string for td in tr.find_all('td')])
                    
                    waktu += [station+"_"+currentDate+"_"+initialDate+"_"+endDate+".csv"]
                    print(station+"_"+nama_stasiun+"_"+currentDate+"_"+initialDate+"_"+endDate+".csv Downloaded")
            
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
            df_merged.to_csv(path_simpan+nama_stasiun+"_"+station+"_"+currentDate+"_start_data_"+tahun+bulan+tanggal+"_merged.csv")
            print("Files merged")

    else:
        id_station = stations[18:23]
        nama_station = names[18:23]
        for station,nama_stasiun in zip(id_station, nama_station):
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
                        "tipe_alat": alat,
                        "provinsi": "PR026",
                        "start": initialDate,
                        "end": endDate,
                        "station": station,
                    }
                    cookies = dict(ci_session= kuki)
                    r = requests.post(url, cookies=cookies, data=body)
            
                    raw_html = r.text
            
                    soup = BeautifulSoup(raw_html, "lxml")
            
                    headers = [th.string for th in soup.find_all('th')]
                    trs = soup.find_all('tr')
            
                    with open("output/stand_alone/"+currentDate+"/"+station+"_"+currentDate+"_"+initialDate+"_"+endDate+".csv", 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(headers)
                        for tr in trs:
                            writer.writerow([td.string for td in tr.find_all('td')])
                    
                    waktu += [station+"_"+currentDate+"_"+initialDate+"_"+endDate+".csv"]
                    print(station+"_"+nama_stasiun+"_"+currentDate+"_"+initialDate+"_"+endDate+".csv Downloaded")
            
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
            df_merged.to_csv(path_simpan+nama_stasiun+"_"+station+"_"+currentDate+"_start_data_"+tahun+bulan+tanggal+"_merged.csv")
            print("Files merged")
