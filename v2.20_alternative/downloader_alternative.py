# Importing libraries
import requests                         #pip install requests
from bs4 import BeautifulSoup as bs     #pip install bs4
from PIL import Image                   #pip install pillow
import pytesseract                      #pip install pytesseract
from io import BytesIO
import csv
import json
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import os

# Kindly to watch
# https://www.youtube.com/watch?v=4DrCIVS5U3Y

# Welcoming Message
print("===========================================================")
print("AWS CENTER DOWNLOADER Alternative")
print("March, 14 2023")
print("Created by Imron Ade")
print("===========================================================")

# ===========================================================
# Functions
# ===========================================================
def bypass_captcha(url):
    res = ses.get(url)
    cap = bs(res.text, 'html.parser').findAll('img')[2]['src'] # Looking for the captcha image link
    
    # Downloading captcha.png
    unduh = ses.get(cap)
    im = Image.open(BytesIO(unduh.content))
    im.save("captcha.png")  # Downloading captcha images
        
    # Bypass captcha and login
    img1 = Image.open('captcha.png')
    
    text = pytesseract.image_to_string(img1, config='--psm 7 -c tessedit_char_whitelist=0123456789+-/x=?.%')

    tanda = text[1]
    hasil = 0
    if tanda == 'x':
        hasil += int(text[0]) * int(text[2])
    elif tanda == '+':
        hasil += int(text[0]) + int(text[2])
    elif tanda == '-':
        hasil += int(text[0]) - int(text[2])
    return hasil

# get label from json data
def get_label(data_json):
    label_data_json = []
    for label in data_json:
        label_data_json.append(label["label"])
    return label_data_json

# get code from label
# Find code from list data
def find_list_code(data_list_json, nama_list_data):
    for listing in data_list_json:
        kode_list = listing["value"]
        nama_list = listing["label"]
        if nama_list == nama_list_data:
            return kode_list
    return "Not Found"  

# make folder based on current date
def checkFolder(oFolder,tahun=None,bulan=None):
    check_folder = os.path.isdir(f'output/monthly/{oFolder}/{tahun}/{bulan}/')
    # If folder doesn't exist, then create it.
    if not check_folder:
        os.makedirs(f'output/monthly/{oFolder}/{tahun}/{bulan}/')
        print(f'created folder : output/monthly/{oFolder}/{tahun}/{bulan}/')
    else:
        print(f'output/monthly/{oFolder}/{tahun}/{bulan}/, folder already exists.')

# ===========================================================
# preparation
# ===========================================================

# user and password 
user = "user"
passwd = "password"

# setting up date
bulan = date.today() - relativedelta(months=1)
bulanDate = bulan.replace(day=1)
awal = bulanDate.strftime('%d')
last_month = date.today().replace(day=1) - datetime.timedelta(days=1)
akhir = last_month.strftime('%d')
tahun = bulanDate.strftime('%Y')
bulan = bulanDate.strftime('%m')

tanggalAwal = f'{tahun}-{bulan}-{awal}'
tanggalAkhir = f'{tahun}-{bulan}-{akhir}'

# ===========================================================
# processing
# ===========================================================

# Login session
print("Login Session")
pytesseract.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe' # PATH tesseract.exe yang sudah diinstall
ses = requests.session()

# loggin session
while True:
    url1 = 'https://awscenter.bmkg.go.id/base'
    # Process of searching for captcha answer
    try:
        hasil = bypass_captcha(url1)

        url2 = 'https://awscenter.bmkg.go.id/base/verify'
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

# Load list of type
url = "https://awscenter.bmkg.go.id/base/autocomplete"
body = {
    "act":"data_type"
    }
r = requests.post(url, cookies=cookies_dictionary ,json=body)
my_json = r.content.decode('utf8').replace("'", '"')
data = json.loads(my_json)
s = json.dumps(data, indent=2, sort_keys=True)
# print(s)
data_json = data

tipeAlat = {}
labelAlat = get_label(data_json)
for i in labelAlat:
    kodeAlat = find_list_code(data_json, i)
    tipeAlat[i] = kodeAlat

# Get type of sites that we want to download
mustType = ['AWS','AAWS','ARG']
listTipe = {}
for i in mustType:
    kode = tipeAlat[i]
    listTipe[i] = kode

# create ouput folders
for i in list(listTipe.keys()):
    checkFolder(i,tahun=tahun,bulan=bulan)

# Load list of ID Sites based on type
for i in listTipe:
    tipe = listTipe[i]
    url = 'https://awscenter.bmkg.go.id/base/autocomplete'
    body = {
        "act":"data_stasiun_assigned_bytype",
        "type": tipe
        }
    r = requests.post(url, cookies=cookies_dictionary ,json=body)
    my_json = r.content.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    # Get code based on type of sites
    labelAlat = get_label(data)
    kodeAlat = {}
    for label in labelAlat:
        kode = find_list_code(data, label)
        kodeAlat[label] = kode
    
    # list out keys and values separately
    key_kodeAlat = list(kodeAlat.keys())
    val_kodeAlat = list(kodeAlat.values())
    
    # Get data based on code of site
    for kode in list(kodeAlat.values()):
        position = val_kodeAlat.index(kode)
        namaAlat = key_kodeAlat[position]
        
        print(f'Download {namaAlat} data')
        
        url = 'https://awscenter.bmkg.go.id/accessdata/bridge_to_api'
        body = {
            'tipe_alat': tipe,
            'start': tanggalAwal,
            'end': tanggalAkhir,
            'station': kode
            }
        r = requests.post(url, cookies=cookies_dictionary ,data=body)
        raw_html = r.text
        soup = bs(raw_html, "lxml")
        headers = [th.string for th in soup.find_all('th')]
        trs = soup.find_all('tr')
        with open(f'output/monthly/{i}/{tahun}/{bulan}/{tahun}_{bulan}_{namaAlat}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for tr in trs:
                writer.writerow([td.string for td in tr.find_all('td')])
        print(f'Downloaded {namaAlat} data')
        

