from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
from datetime import date
import pandas as pd
import time

def Premarket(stock):
    url = "https://stockanalysis.com/stocks/"+stock+"/"
    req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    page = urlopen(req)
    html_doc = page.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    price = str(soup.select('[class*="mt-1.5 block text-sm xs:text-base"]'))
    fprice = str(str(re.sub('<[^>]+>', '', price)).replace("[","")).replace("]","")
    print(stock + ": " + fprice)

from datetime import date, timedelta

yesterday = str(date.today()-timedelta(1))
data = pd.read_csv(yesterday+".csv")

for i in dict(data)["Symbol"]:
    time.sleep(0.4)
    Premarket(i)

print("done")
