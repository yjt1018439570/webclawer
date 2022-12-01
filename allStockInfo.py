import csv
import traceback

import requests
from bs4 import BeautifulSoup

import sys

header = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'}

def getCode2():
    file = open('code2.csv')
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    # print(rows[1::])
    return rows[1::]


def sharesCrawl(shareCode, shareSymbol):
    url = 'https://www.futunn.com/stock/' + str(shareCode) + '-' + str(shareSymbol)
    html = requests.get(url, headers=header).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.findAll('div', {'class': 'stock-detail-li'})
    #print(table[6])

    csvRow = []
    for cell in table[6].findAll('div'):
        csvRow.append(cell.get_text().replace("\n", ""))
    #print(csvRow)
    return csvRow[1]

#sharesCrawl('000006', 'sz')

def writeCSV(shareCode, shareSymbol):
    csvFile = open('./data/marketValue.csv', 'a')
    writer = csv.writer(csvFile)
    try:
        csvrow = []
        csvrow.append(shareCode)
        csvrow.append(sharesCrawl(shareCode, shareSymbol))
        writer.writerow(csvrow)
        print(csvrow)
    except:
        print(traceback.format_exc())
        writer.writerow(shareCode)
    finally:
        csvFile.close()

#writeCSV

if __name__ == '__main__':
    code2=getCode2()
    for i in code2:
        writeCSV(i[0],i[1])




