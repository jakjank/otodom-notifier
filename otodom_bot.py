import requests
from bs4 import BeautifulSoup
import time
import smtplib, ssl
from email.message import EmailMessage

# URL = "https://www.otodom.pl/"
URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0'}
# otodom requiers headers, those are just exemplary 

email_sender   = "your address"
email_password = "your password"
email_receiver = "your address"
port = 465

criteria = {
    "priceMin" : 100_000,   #
    "priceMax" : 500_000,   #
    "areaMin" : 20,         #
    "areaMax" : 100,        # set your criterias
    "by" : "LATEST"
}

response = requests.get(URL, headers=headers, params=criteria)

def email_notify(link):
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = "New offer added"
    em.set_content("Something new for you " + link)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, em.as_string())

def get_latest_offer():
    soup = BeautifulSoup(response.text, "html.parser")
    listing_items = soup.find('div', attrs={'data-cy': 'search.listing.organic'})
    latest_offer = listing_items.find('li')
    return latest_offer

def get_offer_link(tag):
    return 'https://www.otodom.pl/' + tag.find('a')['href']

print(response.url)

# latest_offer= get_latest_offer()
latest_offer = ''
while True:
    try:
        current_offer = get_latest_offer()
    except Exception as e:
        print('Error with getting an offer: ' + e)
        break
    if latest_offer != current_offer:
        latest_offer = current_offer
        try:
            email_notify(get_offer_link(latest_offer))
        except Exception as e:
            print('Error with mail notify: ' + e)
            break
    # refresh every X seconds    
    time.sleep(300)