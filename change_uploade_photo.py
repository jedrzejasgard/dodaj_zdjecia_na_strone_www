#-*- coding: utf-8 -*-

""" Skrypt zamienia nazwy plików z 19061-00a.jpg na 19061-00_a.jpg """

import pysftp
import os
import re
from selenium import webdriver
import configparser

config = configparser.ConfigParser()
config.read('setings.ini')

ftp_pswd = config.get('ftp_asgard','ftp_pswd')
ftp_login = config.get('ftp_asgard','ftp_login')
ftp_ip = config.get('ftp_asgard','ftp_ip')
ftp_port = config.get('ftp_asgard','ftp_port')
local_path = r"C:/Users/asgard_48/Pictures/dodać_na_strone/"
ftp_path = "/home/asgard/public_html/tmp/zdjecia/"
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
# re.split('(^[0-9]*[-,0-9,A]*)','19061-00Aa.jpg')

#print (os.getcwd())

LISTA_PLIKOW = os.listdir(os.getcwd())
"""
Zmiana nazw plików
"""
for plik in LISTA_PLIKOW:
    if plik.endswith('.jpg'):
        #if '_' in plik:
        #    continue
        search_result = re.split(r'([a-z].*\.jpg)$', plik)
        if len(search_result[:-1]) > 0: 
            plik_after = "_".join(search_result[:-1])
            print ("{0} --> {1}".format(plik, plik_after))
            try:
                os.rename(plik,plik_after)
            except:
                print ("problem z plikiem --> {0}".format(plik))
                continue
"""
Wysyłka na FTP skąd import na sklep się odbywa
"""
LISTA_PLIKOW = os.listdir(os.getcwd())
with pysftp.Connection(ftp_ip, username=ftp_login, password=ftp_pswd, port=ftp_port, cnopts=cnopts) as sftp:
    for plik in LISTA_PLIKOW:
        if plik.endswith('.jpg'):
            sftp.put(
                "".join([local_path, plik]), 
                "".join([ftp_path, plik]))
"""
Selenium loguje się na Evolve i klika import zdjęć na stronę a potem zamuka przeglądarke
"""

l = config.get('evolve','user')
h = config.get('evolve','pass')
evolve_url = 'https://asgard.gifts/admin/'
admin_vendo_url = 'https://asgard.gifts/admin/VENDO'
d = webdriver.Chrome(r'C:\Users\asgard_48\Documents\chromedriver_win32\chromedriver.exe')
d.get(evolve_url)
d.maximize_window()
d.find_element_by_name('uLogin').send_keys(l)
d.find_element_by_name('uPasswd').send_keys(h)
d.find_element_by_xpath('/html/body/div[2]/div[1]/form/button').click()
d.get(admin_vendo_url)