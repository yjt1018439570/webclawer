# coding: utf8

import csv
import requests
from bs4 import BeautifulSoup

import traceback
import sys
import _mysql_connector

header = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52'}


def getCode():
    file = open('code.csv')
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    #print(rows[1::])
    return rows[1::]

#getCode()

def sharesCrawl(shareCode, year, season):
    url = 'http://quotes.money.163.com/trade/lsjysj_' + str(shareCode) + '.html?year=' + str(year) + '&season=' + str(season)
    html = requests.get(url, headers=header).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', {'class': 'table_bg001 border_box limit_sale'})
    rows = table.findAll('tr')[1:]
    #print(rows[::-1])

    return rows[::-1]
#sharesCrawl('000001', 2022, 4)


def writeCSV(shareCode, beginYear, endYear):
    csvFile = open('./data/market1.csv', 'a')
    #csvFile = open('./data/market.csv', 'a')
    writer = csv.writer(csvFile)

    try:
        for i in range(beginYear, endYear + 1):
            print(shareCode + ' is going')
            for j in range(1, 5):
                rows = sharesCrawl(shareCode, i, j)
                #print(j)
                for row in rows:
                    csvRow = []
                    # 判断是否有数据
                    if row.findAll('td') != []:
                        csvRow.append(shareCode)
                        for cell in row.findAll('td'):
                            csvRow.append(cell.get_text().replace(',', ''))
                        if csvRow != []:
                            writer.writerow(csvRow)
                            print(csvRow)
                #print(shareCode + ' ' + str(j) + '季度 done')

    except:
        print(traceback.format_exc())
        writer.writerow(str(shareCode))
    finally:
        csvFile.close()


if __name__ == '__main__':

    """
    csvFile = open('./data/market.csv', 'a')
    writer = csv.writer(csvFile)
    writer.writerow(('shareCode', 'Date', 'Opening Price', 'Highest Price', 'Lowing Price', 'Closing Price',
                 'Price Difference', 'Price Difference Percentage', 'Trading Volume', 'Amount', 'Stock Amplitude',
                 'Turnover Rate'))
    """

code=getCode()
for i in code:
    writeCSV(i[0], 2022, 2022)





