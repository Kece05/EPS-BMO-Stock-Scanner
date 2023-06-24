import urllib.request
from html_table_parser.parser import HTMLTableParser
import time

def getPercentChanng(stock):
    url = "https://finviz.com/quote.ashx?t="+str(stock)
    req = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    f = urllib.request.urlopen(req)
    xhtml = f.read().decode('utf-8')
    p = HTMLTableParser()
    p.feed(xhtml)
    return pd.DataFrame(p.tables[7])[11][11]

import pandas as pd
from datetime import date, timedelta

yesterday = str(date.today()-timedelta(1))
data = pd.read_csv(yesterday+'.csv')
pc = []

for i in dict(data)["Symbol"]:
    time.sleep(0.2)
    pc.append(getPercentChanng(i))

data_new = data.copy()
data_new['Price Change'] = pc
data_new.to_csv(yesterday+'.csv', index=False, header=True)

print("done")


