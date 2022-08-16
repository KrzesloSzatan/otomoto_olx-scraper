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

# === pimp Windows 10 notification ===

# https://stackoverflow.com/questions/63867448/interactive-notification-windows-10-using-python

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


# # *NOTE 1/2: perhaps no longer needed as of 0.10?
# try:
#     open(r"output/" + this_run_datetime + "/1-output.txt",
#          "w").close()  # clean main file at start
# except:  # crashes on 1st run when file is not yet created
#     print("Nothing to clean, moving on...")
# # *NOTE 2/2: ^

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
    vins = []

    hrefy = soup.find_all('a', href=re.compile('oferta'))
    ceny = soup.find_all('span', {'class': 'ooa-epvm6'})

    for url in hrefy:
        if url.get('href') not in urls:
            urls.append(url.get('href'))  # Add clean URLs to the list

    # === Scraping VINs ===

    with alive_bar(bar="classic2", spinner="classic") as bar:

        for url in urls:
            try:
                print('Scraping VIN of ' + url)
                time.sleep(2)
                page_vin = urlopen(url, context=ssl.create_default_context(
                    cafile=certifi.where()))  # fix certificate issue
                soup_vin = BeautifulSoup(page_vin, 'html.parser')
                #print(str(soup_vin.find('div', {'class': 'carfax-wrapper'})))
                vin = re.findall(
                    r'(?<=vin=)(.*?)(?=\")', str(soup_vin.find('div', {'class': 'carfax-wrapper'})))
                if vin == []:
                    vin = ['No VIN Found.']
                vins.append(vin[0])
            except Exception as e:
                with open(args.prefix + "/output/" + str(this_run_datetime) + "/1-output-error.txt", "a", encoding="utf-8") as bs_output4:

                    bs_output4.write(
                        'ERROR: ' + str(e) + 'occurred.\n' + url + '\n\n' + str(vin))
                    bs_output4.close()
                    print('ERROR: ', str(e), 'occurred.', url, str(vin))

    lista = list(zip(urls, soup.find_all(
        'span', {'class': 'ooa-epvm6'}), vins))

    # DEBUG vvvvvvvvvvvvvvvvvvvvv

    with open(args.prefix + "/output/" + str(this_run_datetime) + "/1-output-debug.txt", "a", encoding="utf-8") as bs_output3:
        # find all links with 'oferta' in the href

        bs_output3.write(str(type(lista)) + ', ' + str(lista) + '\n\n')
        bs_output3.write(str(type(hrefy)) + ', ' + str(hrefy) + '\n\n')
        bs_output3.write(str(type(ceny)) + ', ' + str(ceny) + '\n\n')
        bs_output3.write(str(type(vins)) + ', ' + str(vins) + '\n\n')

        for link, price, vin in lista:
            # Write URL and price to file
            bs_output3.write(link + ', ' +
                             price.text + ', ' + vin + '\n')
    bs_output3.close()

    # DEBUG ^^^^^^^^^^^^^^^^^^^^^

    # === Writing scraped data to files ===

    with open(args.prefix + "/output/" + str(this_run_datetime) + "/1-output-prices.txt", "a", encoding="utf-8") as bs_output2:
        # find all links with 'oferta' in the href
        for link, price, vin in lista:
            # Write URL and price to file
            bs_output2.write(link + ', ' +
                             price.text + ', ' + vin + '\n')
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

        filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
        filenames = list(map(lambda x: x.replace('.png', ''),
                             filenames))  # Get filenames only

        screenAble = [url for url in urls if not any(
            urls in url for urls in filenames)]  # Compare files with URLs and find only those URLs that are not already screanshotted

    # actual screenshot:

        for link in screenAble:
            print('Making a screenshot of ' + link)
            options = Options()
            options.headless = True
            name = link.replace('https://www.otomoto.pl/oferta/', '')
            png = name.replace('.html', '.png')
            driver = webdriver.Firefox(options=options)
            driver.set_window_position(0, 0)
            driver.set_window_size(1500, 1200)
            driver.get(link)
            screenshot = driver.save_screenshot(
                '.\\' + args.prefix + '/screens\\' + png)
            driver.quit()
            bar()

    page_number += 1  # go to next page
# === get the number# of search results pages & run URLs in function ^ ===


# === tailor the results by using a keyword: brand, model (possibly also engine size etc) ===
# TODO: mostly broken as of 0.9; core works

# regex_user_input = input("Jak chcesz zawęzić wyniki? Możesz wpisać markę (np. BMW) albo model (np. E39) >>> ") # for now using brand as quesion but user can put any one-word keyword
# regex_user_input = ""
# if len(regex_user_input) == 0:
#     print("Keyword wasn't provided - not searching.")
# else:
#     regex_user_input = regex_user_input.strip()  # strip front & back
#     print("Opening file to search for keyword:", regex_user_input)
#     reg = re.compile(regex_user_input)  # matches "KEYWORD" in lines
#     counter2 = 0  # another counter to get the # of search results
#     with open(r'output/' + this_run_datetime + '/3-search_keyword.txt', 'w') as output:  # open file for writing
#         print("Searching for keyword...")
#         # look for keyword in the clean file without empty lines and duplicates
#         with open(r'output/' + this_run_datetime + '/2-clean.txt', 'r', encoding='UTF-8') as clean_no_dupes_file:
#             with alive_bar(bar="circles", spinner="dots_waves") as bar:
#                 for line in clean_no_dupes_file:  # read file line by line
#                     if reg.search(line):  # if there is a match anywhere in a line
#                         output.write(line)  # write the line into the new file
#                         counter2 += 1  # counter ++
#                         bar()  # progress bar ++
#                         # print ("Progress:", counter2)
#             if counter2 == 1:
#                 print("Found", counter2, "result.")
#                 # if platform == "win32":

#                 toast = Notification(app_id=f"Nowe Auta",
#                                      title="OTOMOTO Mazda MX-5",
#                                      msg=f'Znaleziono {str(counter2)} Auto.  W sumie jest {len(urls)}. ',
#                                      icon=r"C:\Users\Franz\otomoto\otomoto4\icons\mazda.png")
#                 toast.add_actions(label="Idz do strony",
#                                   launch=page_url_shortened[0])
#                 toast.show()
#                 open_url()

#             else:
#                 print("Found", counter2, "results.")
#                 # if platform == "win32":

#                 toast = Notification(app_id=f"Nowe Auta",
#                                      title="OTOMOTO Mazda MX-5",
#                                      msg=f'Znaleziono {str(counter2)} Auta.  W sumie jest {len(urls)}. ',
#                                      icon=r"C:\Users\Franz\otomoto\otomoto4\icons\mazda.png")
#                 toast.add_actions(label="Idz do strony",
#                                   launch=page_url_shortened[0])
#                 toast.show()
#                 open_url()

# === open keyword/search results ^ in browser ===

    # if counter2 != 0:
    #     # user_choice_open_urls = input("Chcesz otworzyć linki w przeglądarce? [y/n] >>> ")
    #     user_choice_open_urls = 'n'
    #     if user_choice_open_urls == 'y':
    #         with open("output/" + this_run_datetime + "/3-search_keyword.txt", 'r', encoding='UTF-8') as search_results:
    #             counter3 = 0
    #             print("Opening URLs in browser...")
    #             with alive_bar(bar="circles", spinner="dots_waves") as bar:
    #                 for line in search_results:  # go through the file
    #                     webbrowser.open(line)  # open URL in browser
    #                     counter3 += 1
    #                     bar()
    #         # correct grammar for multiple (URLs; them; they)
    #         if counter3 != 1:
    #             print("Opened ", str(counter3),
    #                   " URLs in the browser. Go and check them before they go 404 ;)")
    #             # if platform == "win32":
    #             # toaster.show_toast("otomoto-scraper", "Opened " + str(counter3) +
    #             #                    " URLs.",  icon_path="icons/www.ico", duration=None)
    #         else:  # correct grammar for 1 (URL; it)
    #             print("Opened", counter3,
    #                   "URL in the browser. Go and check it before it goes 404 ;)")
    #             # if platform == "win32":
    #             # toaster.show_toast("otomoto-scraper", "Opened " + str(counter3) +
    #             #                    " URL.",  icon_path="icons/www.ico", duration=None)
    #     else:
    #         # print ("Ok - URLs saved in 'output/search/output.txt' anyway.")
    #         print("Ok - URLs saved to a file.")
    #         # print("Script run time:", datetime.now()-start)
    #         # sys.exit()
    # else:
    #     print("No search results found.")

# === compare files ===

# try:
#     counter2
# except NameError:
#     print("Variable not defined. Keyword wasn't provided.")

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

    if len(changes) != 0:
        with open(args.prefix + '/output/diff/diff2-' + this_run_datetime + '.txt', 'w') as w:
            # counter4 = 0  # counter
            with alive_bar(bar="circles", spinner="dots_waves") as bar:
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
                        # toast = Notification(app_id=f'{random.randint(0,100)}',
                        toast = Notification(app_id='Nowe auto',
                                             title="OTOMOTO " + args.title,
                                             msg=f'Pojawiło się nowe auto !',
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
    else:
        toast = Notification(app_id="Nie ma nowych aut",
                             title="OTOMOTO " + args.title,
                             msg=f'Nie ma nowych aut. W sumie jest {len(urls)}.',
                             icon=str(self_path.parent.absolute()) + "\\icons\\" + args.icon + ".png")
        toast.add_actions(label="Idz do strony",
                          launch=page_url_shortened[0])
        toast.show()
        bar()

    # # set with lines from 1st file
    # f1 = [x for x in file_previous_run.readlines()]
    # # print("previous", len(f1)) #debug
    # # print(*f1, sep = "\n") #debug
    # # set with lines from 2nd file
    # f2 = [x for x in file_current_run.readlines()]
    # # print("present", len(f2)) #debug
    # # print(*f2, sep = "\n") #debug

    # # lines present only in 1st file
    # diff = [line for line in f1 if line not in f2]
    # # print("previous_diff", len(diff)) #debug
    # # lines present only in 2nd file
    # diff1 = [line for line in f2 if line not in f1]
    # # print("present_diff", len(diff1)) #debug
    # # *NOTE file2 must be > file1

    # if len(diff1) == 0:  # check if set is empty - if it is then there are no differences between files
    #     print('Files are the same.')

    #     toast = Notification(app_id="Nie ma nowych aut",
    #                          title="OTOMOTO " + args.title,
    #                          msg=f'Nie ma nowych aut. W sumie jest {len(f2)}.',
    #                          icon=str(self_path.parent.absolute()) + "\\icons\\" + args.icon + ".png")
    #     toast.add_actions(label="Idz do strony",
    #                       launch=page_url_shortened[0])
    #     toast.show()

    # else:
    #     with open(args.prefix + '/output/diff/diff-' + this_run_datetime + '.txt', 'w') as w:
    #         counter4 = 0  # counter
    #         with alive_bar(bar="circles", spinner="dots_waves") as bar:
    #             for url in diff1:  # go piece by piece through the differences
    #                 w.write(url)  # write to file
    #                 # run IFTTT automation with URL
    #                 #run_ifttt_automation(url, this_run_datetime, location)
    #                 # print('Running IFTTT automation...')
    #                 bar()
    #                 counter4 += 1  # counter++
    #     if counter4 <= 0:  # should not fire
    #         print('No new cars since last run.')

    #         # toast = Notification(app_id="Nie ma nowych aut",
    #         #                      title="OTOMOTO " + args.title,
    #         #                      msg=f'Nie ma nowych aut. W sumie jest {len(f2)}.',
    #         #                      icon=str(self_path.parent.absolute()) + "\\icons\\" + args.icon + ".png")
    #         # toast.add_actions(label="Idz do strony",
    #         #                   launch=page_url_shortened[0])
    #         # toast.show()

    #     else:
    #         print(counter4, "new cars found since last run! Go check them now!")

    #         # toast = Notification(app_id="Nowe Auta",
    #         #                      title="OTOMOTO " + args.title,
    #         #                      msg=f'Są nowe auta: {counter4}. W sumie jest {len(f2)}.',
    #         #                      icon=str(self_path.parent.absolute()) + "\\icons\\" + args.icon + ".png")
    #         # toast.add_actions(label="Idz do strony",
    #         #                   launch=page_url_shortened[0])
    #         # toast.show()

    #         time.sleep(5)
    #         # webbrowser.open(page_url)
    #         open_url()

except IOError:
    print("No previous data - can't diff.")

# === run time ===

# run_time = datetime.now()-start
end = time.time()  # run time end
run_time = round(end-start, 2)
print("Script run time:", run_time, "seconds.")
