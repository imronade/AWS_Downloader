# Importing libraries
import requests                         #pip install requests
from bs4 import BeautifulSoup as bs     #pip install bs4
from PIL import Image                   #pip install pillow
import pytesseract                      #pip install pytesseract
from io import BytesIO
import csv
import json
import glob
import pandas as pd
from datetime import date, timedelta, datetime
import os
import calendar
from dateutil.relativedelta import relativedelta

# Kindly to watch
# https://www.youtube.com/watch?v=4DrCIVS5U3Y

# Welcoming Message
print("===========================================================")
print("AWS CENTER DOWNLOADER V.2.1")
print("June, 02 2021")
print("Created by Imron Ade")
print("===========================================================")

# setting up output folder
# make folder based on current Date
print("Checking folder..")
currentDate = date.today()
currentDate = currentDate.strftime("%Y%m%d")

CHECK_FOLDER = os.path.isdir("output/stand_alone/"+currentDate)
# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs("output/stand_alone/"+currentDate)
    print("created folder : ", "output/stand_alone/"+currentDate)
else:
    print("output/stand_alone/"+currentDate, "folder already exists.")

CHECK_FOLDER2 = os.path.isdir("output/merged/"+currentDate)
# If folder doesn't exist, then create it.
if not CHECK_FOLDER2:
    os.makedirs("output/merged/"+currentDate)
    print("created folder : ", "output/merged/"+currentDate)
else:
    print("output/merged/"+currentDate, "folder already exists.")

# Login session
print("Login Session")
pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe' # PATH tesseract.exe yang sudah diinstall
ses = requests.session()

# user and password sesuai dengan akun 
user = "user"
passwd = "password"

def bypass_captcha(url):
    res = ses.get(url)
    cap = bs(res.text, 'html.parser').findAll('img')[1]['src'] # Looking for the captcha image link
    
    # Downloading captcha.png
    unduh = ses.get(cap)
    im = Image.open(BytesIO(unduh.content))
    im.save("captcha.png")  # Downloading captcha images
        
    # Bypass captcha and login
    img1 = Image.open('captcha.png')
    
    text = pytesseract.image_to_string(img1)

    tanda = text[1]
    hasil = 0
    if tanda == 'x':
        hasil += int(text[0]) * int(text[2])
    elif tanda == '+':
        hasil += int(text[0]) + int(text[2])
    elif tanda == '-':
        hasil += int(text[0]) - int(text[2])
    return hasil


while True:
    url1 = 'http://202.90.198.206/aws/base'
    # Process of searching for captcha answer
    try:
        hasil = bypass_captcha(url1)

        url2 = 'http://202.90.198.206/aws/base/verify'
        data = {
            'username':user,
            'password':passwd,
            'captcha':hasil
        }
        res2 = ses.post(url2, data=data)

        if "Welcome" not in res2.text:
            print("Login tidak berhasil!")
            print("Sedang mencoba kembali untuk login")
            continue
    except:
        print("Login tidak berhasil!")
        print("Sedang mencoba kembali untuk login")
        continue
    break


print("Berhasil Login")

# Get ci_session 
ses_cookies = ses.cookies
cookies_dictionary = ses_cookies.get_dict()

# Load all list data
def list_data(iact, KodeProvinsi = None, KodeKota = None, TipeAlat = None):
    url = "http://202.90.198.206/aws/base/autocomplete"  # url post host
    list_act = ["data_type", "data_provinsi", "data_kota", "data_stasiun_prov", "data_stasiun"]
    act = list_act[iact]
    body = {}
    for variable in ["act"]:
        body[variable] = eval(variable)

    # list json data by category
    if iact == 0 or iact == 1:
        pass
    elif iact == 2:
        body["provinsi"] = str(KodeProvinsi)
    elif iact == 3:
        cookies_dictionary["PHPSESSID"] = "de90a49e35e0a897ed905b930ccee33c"
        body["provinsi"] = str(KodeProvinsi)
        body["kota"] = ""
        body["type"] = str(TipeAlat)
    elif iact == 4:        
        body["kota"] = str(KodeKota)
        body["type"] = str(TipeAlat)
    else:
        print("Menu Perintah Tidak Ada")

    # Method 
    index_metode = [0,1,2,4] 
    if iact in index_metode:
        r = requests.post(url, json= body)
    else:
        r = requests.post(url, cookies=cookies_dictionary ,json=body)
    # print(r.content)
    my_json = r.content.decode('utf8').replace("'", '"')
    # print(my_json)
    # print('- ' * 20)
    data = json.loads(my_json)
    s = json.dumps(data, indent=2, sort_keys=True)
    # print(s)
    data_json = data
    data_json_dumps = s
    return data_json, data_json_dumps

# get label from json data
def get_label(data_json):
    label_data_json = []
    for label in data_json:
        label_data_json.append(label["label"])
    return label_data_json

# print list from get_label
def print_list(listdata):
    for i in listdata:
        print(listdata.index(i),". ",i,sep="")
    # features select everything (under develop)
    print(listdata.index(i)+1,". ","Semuanya",sep="")

# Find code from list data
def find_list_code(data_list_json, nama_list_data):
    for listing in data_list_json:
        kode_list = listing["value"]
        nama_list = listing["label"]
        if nama_list == nama_list_data:
            return kode_list
    return "Not Found"    

# Get list data from menu except all function
def get_main_menu_choice(listdata):
    while True:    
        try:
            number = int(input('Aku memilih: '))
            if 0 <= number < len(listdata):
                return number
            elif number == len(listdata):
                print("Menu Dalam Pengembangan")
                pass
            elif number > len(listdata):
                print("Input Tidak Ada Dalam List Menu")
                pass
        except (ValueError, TypeError):
            print("Input Tidak Diketahui")
            print("Silahkan Coba Lagi")
            pass

# processing to get data
def data_alat(TipeAlat = None, KodeProvinsi = None, NamaProvinsi = None, KodeKota = None, \
    KodeAlat = None, NamaAlat = None, initialDate = None, akhirbulan = None, tanggal = None):
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

        url = "http://202.90.198.206/aws/accessdata/show_data"
        body = {
            "tipe_alat": TipeAlat,
            "kota": KodeKota,
            "provinsi": KodeProvinsi,
            "start": initialDate,
            "end": endDate,
            "station": KodeAlat,
        }
        cookies = cookies_dictionary
        r = requests.post(url, cookies=cookies, data=body)
        raw_html = r.text
        soup = bs(raw_html, "lxml")
        headers = [th.string for th in soup.find_all('th')]
        trs = soup.find_all('tr')
        with open("output/stand_alone/"+currentDate+"/"+TipeAlat+"_"+NamaProvinsi+"_"+NamaAlat+"_"+initialDate+"_"+endDate+".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for tr in trs:
                writer.writerow([td.string for td in tr.find_all('td')])
        
        waktu += [TipeAlat+"_"+NamaProvinsi+"_"+NamaAlat+"_"+initialDate+"_"+endDate+".csv"]
        print(TipeAlat+"_"+NamaProvinsi+"_"+NamaAlat+"_"+initialDate+"_"+endDate+".csv Downloaded")
    
    # combining stand alone data
    path = os.getcwd()
    path_data = path+"\\output\\stand_alone\\"+currentDate+"\\"
    path_simpan = path+"\\output\\merged\\"+currentDate+"\\"

    filenames = []
    for t in waktu:
        filename = glob.glob(os.path.join(path_data, t))
        filenames += filename
    # filenames = glob.glob(os.path.join(path_data,"*.csv"))
    df_from_each_file = (pd.read_csv(f, sep=',') for f in filenames)
    df_merged   = pd.concat(df_from_each_file, ignore_index=True)
    df_merged.to_csv(path_simpan+TipeAlat+"_"+NamaProvinsi+"_"+NamaAlat+"_start_data_"+tahun+bulan+tanggal+"_merged.csv")
    print("Files merged")

while True:
    # setting up the date
    print("Pastikan isi dengan benar ya")
    tahun = str(input("Masukkan tahun (Contoh: 2021): "))
    bulan = str(input("Masukkan bulan (Contoh: 03): "))
    tanggal = str(input("Masukkan tanggal mulai (Contoh: 01): "))

    initialDate = tahun+"-"+bulan+"-"+tanggal
    akhirbulan = calendar.monthrange(int(tahun), int(bulan))[1]

    # print list tipe alat
    data_json, data_json_dumps = list_data(0)
    label_data_json = get_label(data_json)
    print("List Tipe Alat:")
    print_list(label_data_json)
    number = get_main_menu_choice(label_data_json)
    iTipeAlat = number
    TipeAlat = label_data_json[iTipeAlat]

    # print list provinsi
    data_json, data_json_dumps = list_data(1)
    list_provinsi = data_json
    label_data_json = get_label(data_json)
    print("List Provinsi:")
    print_list(label_data_json)
    number = get_main_menu_choice(label_data_json)
    inama_provinsi = number
    NamaProvinsi = label_data_json[inama_provinsi]
    KodeProvinsi = find_list_code(list_provinsi, NamaProvinsi)

    # print list kota in provinsi
    data_json, data_json_dumps = list_data(2, KodeProvinsi)
    list_kota = data_json
    label_data_json = get_label(data_json)
    print("List Kota:")
    print_list(label_data_json)
    max_kota = len(label_data_json)
    inama_kota = int(input("Aku memilih kota: "))
    if inama_kota < max_kota:
        NamaKota = label_data_json[inama_kota]
        KodeKota = find_list_code(list_kota, NamaKota)

        # print list alat in city
        data_json, data_json_dumps = list_data(4, KodeKota=KodeKota, TipeAlat=TipeAlat)
        list_alat_kota = data_json
        label_data_json = get_label(data_json)
        label_alat_kota = label_data_json
        print("List Alat Dalam Kota:")
        print_list(label_data_json)
        inama_alat = int(input("Aku memilih: "))
        max_alat = len(label_data_json)
        if inama_alat < max_alat:
            NamaAlat = label_data_json[inama_alat]
            KodeAlat = find_list_code(list_alat_kota, NamaAlat)

            # download data
            print("Proses download data")
            data_alat(TipeAlat=TipeAlat, KodeProvinsi=KodeProvinsi, NamaProvinsi=NamaProvinsi,
                KodeKota=KodeKota, KodeAlat=KodeAlat, NamaAlat=NamaAlat, initialDate=initialDate,
                akhirbulan=akhirbulan, tanggal=tanggal)
        
        elif inama_alat == max_alat:
            print("Proses download data")
            for i in label_alat_kota:
                NamaAlat = i
                KodeAlat = find_list_code(list_alat_kota, NamaAlat)
                data_alat(TipeAlat=TipeAlat, KodeProvinsi=KodeProvinsi, NamaProvinsi=NamaProvinsi,
                        KodeKota="", KodeAlat=KodeAlat, NamaAlat=NamaAlat, initialDate=initialDate,
                        akhirbulan=akhirbulan, tanggal=tanggal)


    elif inama_kota == max_kota:
        data_json, data_json_dumps = list_data(3, KodeProvinsi=KodeProvinsi, TipeAlat=TipeAlat)
        list_alat_prov = data_json
        label_data_json = get_label(data_json)
        label_all_alat_provinsi = label_data_json
        print("List alat yang akan didownload sebagai berikut:")
        for i in label_data_json:
            print(label_data_json.index(i),". ",i,sep="")

        # download data
        print("Proses download data")
        for i in label_all_alat_provinsi:
            NamaAlat = i
            KodeAlat = find_list_code(list_alat_prov, NamaAlat)
            data_alat(TipeAlat=TipeAlat, KodeProvinsi=KodeProvinsi, NamaProvinsi=NamaProvinsi,
                    KodeKota="", KodeAlat=KodeAlat, NamaAlat=NamaAlat, initialDate=initialDate,
                    akhirbulan=akhirbulan, tanggal=tanggal)

    while True:
        answer = str(input('Mau download lagi? (y/n): '))
        if answer in ('y', 'n', 'Y', 'N'):
            break
        print("Invalid Input")
    if answer == 'y':
        continue
    else:
        print("Semoga Bermanfaat")
        break
