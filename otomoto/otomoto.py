# === libs ===

from os import walk
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import difflib
from winotify import Notification
from random import randrange
import gdshortener  # shorten URLs using is.gd e
import requests  # for IFTTT integration to send webhook
import pickle  # store data
import os  # create new folders
from urllib.request import urlopen  # open URLs
from bs4 import BeautifulSoup  # BeautifulSoup; parsing HTML
import re  # regex; extract substrings
import time  # delay execution; calculate script's run time
from datetime import datetime  # add IDs to files/folders' names
from alive_progress import alive_bar  # progress bar
import webbrowser  # open browser
import ssl  # certificate issue fix: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
import certifi  # certificate issue fix: https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate
import sys
from sys import platform  # check platform (Windows/Linux/macOS)
import argparse
from pathlib import Path
import random
from twilio.rest import Client

# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


self_path = Path(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--url', '-u')
parser.add_argument('--title', '-t')
parser.add_argument('--icon', '-i')
parser.add_argument('--prefix', '-p')
args = parser.parse_args()

# === start + run time ===

start = time.time()  # run time start
print("Starting...")

# === create folders tree ===

print("Checking folders tree....")
if not os.path.isdir(args.prefix):
    os.mkdir(args.prefix)
    print("Folder ./" + args.prefix + " created")
if not os.path.isdir(args.prefix + "/data"):
    os.mkdir(args.prefix + "/data")
    print("Folder ./" + args.prefix + "/data created")
if not os.path.isdir(args.prefix + "/output"):
    os.mkdir(args.prefix + "/output")
    print("Folder ./" + args.prefix + "/output created")
if not os.path.isdir(args.prefix + "/output/diff"):
    os.mkdir(args.prefix + "/output/diff")
    print("Folder ./" + args.prefix + "/output/diff created")
if not os.path.isdir(args.prefix + "/screens"):
    os.mkdir(args.prefix + "/screens")
    print("Folder ./" + args.prefix + "/screens created")
print("All folders are present.")

# === have current date & time in exported files' names ===

# https://www.w3schools.com/python/python_datetime.asp
this_run_datetime = datetime.strftime(
    datetime.now(), '%y%m%d-%H%M%S')  # eg 210120-173112

file_saved_date = args.prefix + '/data/date.pk'
try:  # might crash on first run
    # load your data back to memory so we can save new value; NOTE: b = binary
    with open(file_saved_date, 'rb') as file:
        # keep previous_run_datetime (last time the script ran) in a file so we can retrieve it later and compare / diff files
        previous_run_datetime = pickle.load(file)
        print("Previous run:", previous_run_datetime)
except IOError as e:
    # if it's the first time script is running we won't have the file created so we skip
    #print("First run - no file exists.")
    print(e)

try:
    with open(file_saved_date, 'wb') as file:  # open pickle file
        # dump this_run_datetime (the time script is running) into the file so then we can use it to compare / diff files
        pickle.dump(this_run_datetime, file)
        print("This run:", this_run_datetime)
except IOError:
    print("File doesn't exist.")

# create new folder
if not os.path.isdir(args.prefix + "/output/" + this_run_datetime):
    os.mkdir(args.prefix + "/output/" + this_run_datetime)  # eg 210120-173112
    print("Folder created:", this_run_datetime)

# === URL to scrape ===

# BMW 1, 140+ KM, AC, Pb/On, 2002+, 5k-20k PLN, Wrocław + 50 km, sort: newest
page_url = args.url
location = ""

# === shorten the URL ===

isgd = gdshortener.ISGDShortener()  # initialize
page_url_shortened = isgd.shorten(page_url)  # shorten URL; result is in tuple
# [0] to get the first element from tuple
print("Page URL:", page_url_shortened[0])

# === IFTTT automation ===

#file_saved_imk = '../data/imk.pk'
# try:  # might crash on first run
#    # load your data back to memory so we can save new value; NOTE: b = binary
#    with open(file_saved_imk, 'rb') as file:
#        ifttt_maker_key = pickle.load(file)
# except IOError as e:
#    #print("First run - no file exists.")
#    print(e)

#event_name = 'new-car'
#webhook_url = 'https://maker.ifttt.com/trigger/{event_name}/with/key/{ifttt_maker_key}'


# def run_ifttt_automation(url, date, location):
#    report = {}
#    report["value1"] = url
#    report["value2"] = date
#    report["value3"] = location
#    requests.post(webhook_url, data=report)

# === Function to open url after search ===

def open_url():
    try:
        webbrowser.open_new(page_url)
        print('Opening search results...')
    except:
        print('Failed to open search results. Unsupported variable type.')

# === function to scrape data ===


page = urlopen(page_url, context=ssl.create_default_context(
    cafile=certifi.where()))  # fix certificate issue
time.sleep(10)
soup = BeautifulSoup(page, 'html.parser')  # parse the page

# def pullData(page_url):

number_of_pages_to_crawl = ([item.get_text(strip=True) for item in soup.find_all(
    'a', {'class': 'ooa-g4wbjr'})])  # get page numbers from the bottom of the page

if len(number_of_pages_to_crawl) > 0:
    # get the last element from the list ^ to get the the max page # and convert to int
    number_of_pages_to_crawl = int(number_of_pages_to_crawl[-1])
else:
    number_of_pages_to_crawl = 1
print('How many pages are there to crawl?', number_of_pages_to_crawl)

page_prefix = '&page='
page_number = 1  # begin at page=1
# for page in range(1, number_of_pages_to_crawl+1):

lista = []

while lista == [] or lista == None or lista == [None]:
    while page_number <= number_of_pages_to_crawl:
        print("Page number:", page_number, "/",
              number_of_pages_to_crawl)
        full_page_url = f"{page_url}{page_prefix}{page_number}"
        # pullData(full_page_url)  # throw URL to function

        page = urlopen(full_page_url, context=ssl.create_default_context(
            cafile=certifi.where()))  # fix certificate issue
        soup = BeautifulSoup(page, 'html.parser')  # parse the page

        # can't crawl too often? works better with OTOMOTO limits perhaps
        pause_duration = 5  # seconds to wait
        print("Waiting for", pause_duration, "seconds before opening URL...")
        with alive_bar(pause_duration, bar="circles", spinner="dots_waves") as bar:
            for second in range(0, pause_duration):
                time.sleep(1)
                bar()
        print("Scraping page...")

        urls = []
        #vins = []

        hrefy = soup.find_all('a', href=re.compile('oferta'))
        ceny = soup.find_all('span', {'class': 'ooa-1bmnxg7'})

        for url in hrefy:
            if url.get('href') not in urls:
                urls.append(url.get('href'))  # Add clean URLs to the list

        # === Scraping VINs === Doesnt work anymore since Otomoto has changed autodna link to javascript generated

        # with alive_bar(bar="classic2", spinner="classic") as bar:

        #     for url in urls:
        #         try:
        #             print('Scraping VIN of ' + url)
        #             time.sleep(2)
        #             page_vin = urlopen(url, context=ssl.create_default_context(
        #                 cafile=certifi.where()))  # fix certificate issue
        #             soup_vin = BeautifulSoup(page_vin, 'html.parser')
        #             #print(str(soup_vin.find('div', {'class': 'carfax-wrapper'})))
        #             vin = re.findall(
        #                 r'(?<=vin=)(.*?)(?=\")', str(soup_vin.find('div', {'class': 'carfax-wrapper'})))
        #             if vin == []:
        #                 vin = ['No VIN Found.']
        #             vins.append(vin[0])
        #         except Exception as e:
        #             with open(args.prefix + "/output/" + str(this_run_datetime) + "/1-output-error.txt", "a", encoding="utf-8") as bs_output4:

        #                 bs_output4.write(
        #                     'ERROR: ' + str(e) + 'occurred.\n' + url + '\n\n' + str(vin))
        #                 bs_output4.close()
        #                 print('ERROR: ', str(e), 'occurred.', url, str(vin))

        countrys = []
        for url_car in urls:
            page_car = urlopen(url_car, context=ssl.create_default_context(
                cafile=certifi.where()))  # fix certificate issue
            time.sleep(1)
            soup_car = BeautifulSoup(page_car, 'html.parser')  # parse the page
            country_href = soup_car.find_all(
                'a', href=re.compile('country_origin'))
            # country = country_href[0].get('title')
            if country_href:
                countrys.append(country_href[0].get('title'))
            elif country_href == []:
                countrys.append("Nie podano kraju pochodzenia")

        lista = list(zip(urls, soup.find_all(
            'span', {'class': 'ooa-1bmnxg7'}), countrys))

        # print(lista)

        # DEBUG vvvvvvvvvvvvvvvvvvvvv

        with open(args.prefix + "/output/" + str(this_run_datetime) + "/1-output-debug.txt", "a", encoding="utf-8") as bs_output3:
            # find all links with 'oferta' in the href

            bs_output3.write(str(type(lista)) + ', ' + str(lista) + '\n\n')
            bs_output3.write(str(type(hrefy)) + ', ' + str(hrefy) + '\n\n')
            bs_output3.write(str(type(ceny)) + ', ' + str(ceny) + '\n\n')
            bs_output3.write(str(type(countrys)) + ', ' +
                             str(countrys) + '\n\n')
            #bs_output3.write(str(type(vins)) + ', ' + str(vins) + '\n\n')

            # for link, price, vin in lista:
            #     # Write URL and price to file
            #     bs_output3.write(link + ', ' +
            #                      price.text + ', ' + vin + '\n')
            for link, price, country in lista:
                # Write URL and price to file
                bs_output3.write(link + ', ' +
                                 price.text + ', ' + country + '\n')
        bs_output3.close()

        # DEBUG ^^^^^^^^^^^^^^^^^^^^^

        # === Writing scraped data to files ===

        with open(args.prefix + "/output/" + str(this_run_datetime) + "/1-output-prices.txt", "a", encoding="utf-8") as bs_output2:

            for link, price, country in lista:
                # Write URL and price to file
                bs_output2.write(link + ', ' +
                                 price.text + ', ' + country + '\n')

        bs_output2.close()

        # 'a' (append) to add lines to existing file vs overwriting
        with open(args.prefix + "/output/" + str(this_run_datetime) + "/1-output.txt", "a", encoding="utf-8") as bs_output:
            # print (colored("Creating local file to store URLs...", 'green')) # colored text on Windows
            counter = 0  # counter to get # of URLs/cars
            with alive_bar(bar="classic2", spinner="classic") as bar:  # progress bar
                # find all links with 'oferta' in the href

                for link in hrefy:
                    # write to file just the clean URL
                    bs_output.write(link.get('href'))
                    counter += 1  # counter ++
                    bar()  # progress bar ++
                    # print ("Adding", counter, "URL to file...")
            print("Successfully added", counter, "cars to file.")

        # === Taking screenshots ===

        with alive_bar(bar="classic2", spinner="classic") as bar:
            mypath = args.prefix + "/screens"  # Path to screens folder

            filenames = next(walk(mypath), (None, None, []))[
                2]  # [] if no file
            filenames = list(map(lambda x: x.replace('.png', ''),
                                 filenames))  # Get filenames onlyF

            screenAble = [url for url in urls if not any(
                urls in url for urls in filenames)]  # Compare files with URLs and find only those URLs that are not already screanshotted

        # actual screenshot:

            for link in screenAble:
                print('Making a screenshot of ' + link)
                options = Options()
                options.headless = True
                name = link.replace('https://www.otomoto.pl/oferta/', '')
                png = name.replace('.html', '.png')
                driver = Firefox(options=options)
                driver.set_window_position(0, 0)
                driver.set_window_size(1500, 1200)
                driver.get(link)
                screenshot = driver.save_screenshot(
                    '.\\' + args.prefix + '/screens\\' + png)
                driver.quit()
                bar()

        page_number += 1  # go to next page
    # === get the number# of search results pages & run URLs in function ^ ===

try:
    file_previous_run = open(args.prefix +
                             '/output/' + previous_run_datetime + '/1-output-prices.txt', 'r')  # 1st file
    file_current_run = open(args.prefix +
                            '/output/' + this_run_datetime + '/1-output-prices.txt', 'r')  # 2nd file

    with open(args.prefix + '/output/' + previous_run_datetime + '/1-output-prices.txt') as file_1:
        file_1_text = file_1.readlines()

    with open(args.prefix + '/output/' + this_run_datetime + '/1-output-prices.txt') as file_2:
        file_2_text = file_2.readlines()

    # Find and print the diff:
    changes = [line for line in difflib.ndiff(
        file_1_text, file_2_text) if line.startswith('+ ') or line.startswith('- ')]

    # print(changes)

    if len(changes) != 0:
        with alive_bar(bar="circles", spinner="dots_waves") as bar:
            try:
                msg = MIMEMultipart()
                msg['Subject'] = "OTOMOTO POJAWIŁO SIĘ NOWE AUTO " + args.title
                msg_from = formataddr(
                    ("NOWE AUTO " + args.title, 'your_sender@email.com'))
                msg_to = ['your_receiver1@email.com',
                            'your_receiver2@email.com']
                msg['From'] = msg_from
                msg['To'] = ', '.join(msg_to)
                msg.preamble = 'test'

                # Assume we know that the image files are all in PNG format

                send_mail = ""
                for url in changes:
                    if url.startswith('+ ') and (len(re.findall(re.findall(r'(?<=\+ |\- )(.*?)(?=\,)', url)[0], str(changes))) % 2 != 0):
                        clean_url = re.findall(
                            r'(?<=\+ |\- )(.*?)(?=\,)', str(url))
                        #text_msg = "Pojawiło się nowe auto: " + re.sub(r'\.html\,', '.html\n\nCena: ', url.replace('+ ', '')) + '\n\n'
                        text_msg = "Pojawiło się nowe auto: " + \
                            re.sub(r'\.html\,', '.html\n\nCena: ',
                                   url.replace('+ ', '')) + '\n\n'
                        name = url.replace(
                            '+ https://www.otomoto.pl/oferta/', '')
                        #png = name.replace('.html', '.png')
                        png = re.sub(r'\.html.+\n', '.png', name)
                        with open(mypath + "/" + png, 'rb') as fp:
                            img = MIMEImage(fp.read())
                        msg.attach(img)
                        msg.attach(MIMEText(text_msg))
                        send_mail = True

                if send_mail == True:
                    # smtp.mail.yaoo.com is an example. Put your smtp server here.
                    s = smtplib.SMTP('smtp.mail.yahoo.com', 587)
                    s.starttls()
                    # credentials are setup in env variables (this case windows)
                    s.login(os.environ.get('OTOMOTO_SMTP_USERNAME'), os.environ.get(
                        'OTOMOTO_SMTP_PASSWORD'))
                    try:
                        print("Sending email about new cars")
                        s.sendmail(msg_from, msg_to,
                                   msg.as_string())
                    finally:
                        s.quit()
            except IOError as e:
                print(e)
            with open(args.prefix + '/output/diff/diff2-' + this_run_datetime + '.txt', 'w') as w:
                for url in changes:  # go piece by piece through the differences
                    w.write(url)  # write to file
                    time.sleep(1)
                    if url.startswith('- ') and (len(re.findall(re.findall(r'(?<=\+ |\- )(.*?)(?=\,)', url)[0], str(changes))) % 2 == 0):
                        clean_url = re.findall(
                            r'(?<=\+ |\- )(.*?)(?=\,)', str(url))
                        # toast = Notification(app_id=f'{random.randint(0,100)}',
                        toast = Notification(app_id='Zmiana ceny',
                                             title="OTOMOTO " + args.title,
                                             msg=f'Zmieniła się cena auta.',
                                             icon=str(self_path.parent.absolute()) + "\\icons\\" + args.icon + ".png")
                        toast.add_actions(label="Idz do auta",
                                          launch=clean_url[0])
                        toast.show()
                        bar()
                    if url.startswith('+ ') and (len(re.findall(re.findall(r'(?<=\+ |\- )(.*?)(?=\,)', url)[0], str(changes))) % 2 != 0):
                        clean_url = re.findall(
                            r'(?<=\+ |\- )(.*?)(?=\,)', str(url))

                            # app_id is a random number because while multiple notifications they seem to overwrite itself. 
                            # Other notifications are not that important for me but you can set this up like this for all of them.
                            
                        toast = Notification(app_id='Nowe auto' + ' ' + f'{random.randint(0,100)}',
                                             # toast = Notification(app_id='Nowe auto',
                                             title="OTOMOTO " + args.title,
                                             msg=f'Pojawiło się nowe auto !\n\n' + \
                                                 re.findall(
                                                     r'(?<=\,\s).*', str(url))[0],
                                             icon=str(self_path.parent.absolute()) + "\\icons\\" + args.icon + ".png")
                        toast.add_actions(label="Idz do auta",
                                          launch=clean_url[0])
                        toast.show()

                        bar()
                    if url.startswith('- ') and (len(re.findall(re.findall(r'(?<=\+ |\- )(.*?)(?=\,)', url)[0], str(changes))) % 2 != 0):
                        clean_url = re.findall(
                            r'(?<=\+ |\- )(.*?)(?=\,)', str(url))
                        # toast = Notification(app_id=f'{random.randint(0,100)}',
                        toast = Notification(app_id='Sprzedane auto',
                                             title="OTOMOTO " + args.title,
                                             msg=f'Auto zostało wycofane ze sprzedaży. W sumie jest {len(urls)}.',
                                             icon=str(self_path.parent.absolute()) + "\\icons\\" + args.icon + ".png")
                        toast.add_actions(
                            label="Zobacz pozostałe auta", launch=page_url_shortened[0])
                        toast.show()
                        bar()
except IOError:
    print("No previous data - can't diff.")

# === run time ===

# run_time = datetime.now()-start
end = time.time()  # run time end
run_time = round(end-start, 2)
print("Script run time:", run_time, "seconds.")
