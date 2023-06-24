import urllib.request
from html_table_parser.parser import HTMLTableParser
import pandas as pd
import csv
import time
from datetime import date

#https://www.zacks.com/earnings/earnings-calendar
#name it z.csv
#paste the sector performace into the csv file

def stock_list():
    with open('z.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        stock_l = []
        for row in csv_reader:
            if row[3] == "bmo":
                stock_l.append(row[0])
        return stock_l

def stockA(stock):
    try:
        url = "https://finviz.com/quote.ashx?t="+stock
        req = urllib.request.Request(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        f = urllib.request.urlopen(req)
        xhtml = f.read().decode('utf-8')
        p = HTMLTableParser()
        p.feed(xhtml)
        values = {"Symbol": stock,
                  "Sector": pd.DataFrame(p.tables[5])[0][1],
                  "SM20": pd.DataFrame(p.tables[7])[3][11],
                  "SM50": pd.DataFrame(p.tables[7])[5][11],
                  "Avg. Volume": pd.DataFrame(p.tables[7])[9][10],
                  "EPS TR": RR(stock)}
        return values
    except Exception as ex:
        template = "An exception of type {0} occurred."
        message = template.format(type(ex).__name__)
        print(message)

def RR(stock):
    url = "https://www.alphaquery.com/stock/"+stock+"/earnings-history"
    req = urllib.request.Request(url=url,headers={'User-Agent': 'Mozilla/5.0'})
    f = urllib.request.urlopen(req)
    xhtml = f.read().decode('utf-8')
    p = HTMLTableParser()
    p.feed(xhtml)
    try:
        Estimated = getsum(pd.DataFrame(p.tables[0])[2][1:5])
        Actual = getsum(pd.DataFrame(p.tables[0])[3][1:5])
        rr = (Actual / Estimated).__round__(3)
        return EPS_result(rr)
    except:
        return "N/A"

def EPS_result(num):
    if num >= 1.2:
        return "Perfect"
    elif num >= 1.1:
        return "Good"
    elif num >= 1:
        return "Ok"
    elif num <= 1 and num >= 0.7:
        return "Bad"
    else:
        return num

url = "https://www.barchart.com/stocks/market-performance"
req = urllib.request.Request(
    url=url,
    headers={'User-Agent': 'Mozilla/5.0'}
)
f = urllib.request.urlopen(req)
xhtml = f.read().decode('utf-8')
p = HTMLTableParser()
p.feed(xhtml)
table = pd.DataFrame(p.tables[0])[3]

def createSectorPerformace():
    url = "https://www.barchart.com/stocks/market-performance"
    req = urllib.request.Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    f = urllib.request.urlopen(req)
    xhtml = f.read().decode('utf-8')
    p = HTMLTableParser()
    p.feed(xhtml)
    table = pd.DataFrame(p.tables[0])[3]
    print("Technology: " + table[8])
    print("Health: " + table[6])
    print("Consumer Cyclical: " + table[2])
    print("Consumer Defensive: " + table[3])
    print("Basic Materials: " + table[9])
    print("Industrials: " + table[7])
    print("Real Estate: " + table[10])
    print("Communication Services: " + table[11])
    print("Financial: " + table[5])
    print("Energy: " + table[4])
    print("Utilities: " + table[12])

def getsum(list):
    mylst = map(lambda each: each.strip("$"), list)
    try:
        newlist = [eval(i) for i in mylst]
        return sum(newlist).__round__(3)
    except:
        return "N/A"


cd = str(date.today())
with open(cd+'.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

stockinfo = []
fields = ["Symbol", "Sector", "SM20", "SM50", "Avg. Volume", "EPS TR"]

for i in stock_list():
    time.sleep(0.25)
    if stockA(i) != "None":
        stockinfo.append(stockA(i))
        print(stockA(i))

finalStock = [i for i in stockinfo if i is not None]

with open(cd+'.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(finalStock)

createSectorPerformace()
print("\ndone")
