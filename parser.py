#import required libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime

# GLOBAL VARIABLES
avg_price_data = []

'''
This function scrap all the data from the URL, based on the year provided
And return text form of data
'''
def fetch_data_by_year(year: int):
    BASEURL = "https://www.teaboard.gov.in/WEEKLYPRICES"    
    response = requests.get(f"{BASEURL}/{year}") 
    return response.text


'''
This function processes data yearly,
It fetches data, parse it and retreive required information a
Post that it adds data of every row in global variable
'''
def fetch_tea_avg_price_per_year(year: int) -> list:
    data = fetch_data_by_year(year)
    soup = BeautifulSoup(data)
    headers = [header.b.text for header in soup.find(id="contn_GridView2").find_all('tr')[0].find_all('th')]
    for row in soup.find(id="contn_GridView2").find_all('tr')[1:]:
        row_data = [cell.span.text for cell in row.find_all('td')]
        formatted_date = row_data[0].replace('/', '-')
        for index, price in enumerate(row_data[1:]):
            avg_price_data.append([formatted_date, headers[index + 1], price])


'''
Main function iterate on each year from 2008 to current year 
Make a call to other function in order to process information for that year
In last it create pandas dataframe from global data and convert it to CSV
'''
def main() -> None:
    start_year = 2008
    cur_year = int(datetime.date.today().strftime("%Y"))
    for year in range(start_year, cur_year + 1):
        fetch_tea_avg_price_per_year(year) 
    dataframe = pd.DataFrame(avg_price_data, columns=["week", "location", "avg_price"])
    dataframe.to_csv("result.csv", index=False)

if __name__ == "__main__":         
    main()