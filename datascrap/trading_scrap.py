from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

def intradingview(symbols):
    baseurl = "https://in.tradingview.com/symbols/"+symbols+"/technicals/"
    driver = webdriver.Chrome("/usr/local/bin/chromedriver",options=options)
    driver.get(baseurl)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    tabledata = soup.find_all('table', {'class': 'table-1YbYSTk8'})

    output_rows = []

    for i in tabledata:
        columns = i.find_all('td',{'class': 'cell-5XzWwbDG'})
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)

    n =3
    m=6
    if len(output_rows)!=0:
        oscilator = output_rows[0]
        moving_averages = output_rows[1]
        pivot = output_rows[2]

        oscilator_list = [oscilator[i:i + n] for i in range(0, len(oscilator), n)]
        moving_averages_list = [moving_averages[i:i + n] for i in range(0, len(moving_averages), n)]
        pivot_list = [pivot[i:i + m] for i in range(0, len(pivot), m)]

        oscilator_table = pd.DataFrame(np.array(oscilator_list),columns=['Name','Value','Action'])
        moving_averages_table = pd.DataFrame(np.array(moving_averages_list),columns=['Name','Value','Action'])
        pivot_table = pd.DataFrame(np.array(pivot_list),columns=['Pivot','Classic','Fibonacci','Camarilla','Woodie','DM'])

        output = {
            "oscilator":oscilator_table.to_dict('records'),
            "moving_average":moving_averages_table.to_dict('records'),
            "pivot":pivot_table.to_dict('records')
        }
    else:
        output = []

    return output




if __name__ == '__main__':
    print(intradingview(symbols='BSE-YESBANK'))
