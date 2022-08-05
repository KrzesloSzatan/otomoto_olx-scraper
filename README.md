# otomoto-scraper

Orginates from https://github.com/vardecab/otomoto_olx-scraper

![](https://img.shields.io/badge/platform-Windows-blue)

>Scrape car offers from OTOMOTO․pl when new car(s) matching search criteria is found. With support for native Windows 10 notifications. In output folder you can find diff2... file which consists a change that happened, if there is new car it will show "+ url_to_new_car, price, VIN". If the car was sold it shows "- url_to_new_car, price, VIN". If there is a price change it will show both in one file with the same urls but different price. It will also create a screenshot of the car page so you can check which one exactly it is/was. Screenshot is taken only once, when the car appears for the first time to the script, so any changes to the price will not be screenshotted again. 

>This one was redone by me only for OTOMOTO. I havent touched OLX so it works (or not?) as in the source repo. 

<!-- Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cumanos sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. -->

## How to use
### Windows

Run it with parameters like below:

parser.add_argument('--url', '-u') -> This is the URL that you get after choosing all the filters on Otomoto site

parser.add_argument('--title', '-t') -> This is the title for Windows notifications

parser.add_argument('--icon', '-i') -> Icon name that has to be placed in .\otomoto\icons folder (folder can be created manually before first run or it will be created by script after first run. Then you have to put your icon inside this folder. Icons have to be in .png. For best look img has to be square. Ex: name.png -> --icon "name")

parser.add_argument('--prefix', '-p') -> Folder name for where all the scraped data will be stored for this search (Ex. --prefix "make" .\otomoto\make, --prefix "mazda" .\otomoto\mazda, --prefix "bmw" .\otomoto\bmw, etc. )

Ex:

python3 .\otomoto.py --url "https://www.otomoto.pl/osobowe/mazda/mx-5/od-2010?search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search%5Bfilter_enum_fuel_type%5D%5B1%5D=petrol-lpg&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_float_price%3Ato%5D=50000&search%5Border%5D=created_at_first%3Adesc&search%5Badvanced_search_expanded%5D=true" --title "Mazda MX-5" --icon "mazda" --prefix "mazda"


<!-- ## Roadmap

- lorem ipsum -->

## License

![](https://img.shields.io/github/license/vardecab/otomoto_olx-scraper)
<!-- GNU General Public License v3.0, see [LICENSE.md](https://github.com/vardecab/PROJECT/blob/master/LICENSE). -->

## Acknowledgements

### Modules
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [alive-progress](https://github.com/rsalmei/alive-progress)
- [win10toast](https://github.com/jithurjacob/Windows-10-Toast-Notifications)
- [win10toast-persist](https://github.com/tnthieding/Windows-10-Toast-Notifications)
- [win10toast-click](https://github.com/vardecab/win10toast-click)
- [pync](https://github.com/SeTeM/pync)
- [GD Shortener](https://github.com/torre76/gd_shortener)
<!-- - [termcolor](https://pypi.org/project/termcolor/) -->

### Stack Overflow
- [certificate issue fix](https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate)

### Other
- [IFTTT](https://ifttt.com/)
- [Connect a Python Script to IFTTT by Enrico Bergamini](https://medium.com/mai-piu-senza/connect-a-python-script-to-ifttt-8ee0240bb3aa)
- [Use IFTTT web requests to send email alerts by Anthony Hartup](https://anthscomputercave.com/tutorials/ifttt/using_ifttt_web_request_email.html)
