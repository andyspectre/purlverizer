# scrape https://www.scoutdns.com/100-most-popular-tlds-by-google-index/ and find content of the second table
# print the content of the table to the console

import requests
from bs4 import BeautifulSoup

url = 'https://www.scoutdns.com/100-most-popular-tlds-by-google-index/'
response = requests.get(url)

#Parse the HTML as a string
soup = BeautifulSoup(response.text, 'html.parser')

#Find the table with attribute of width="320"
table = soup.find('table', attrs={'width':'320'})

#Find just the first <td> tag for each row
for row in table.find_all('tr'):
    col = row.find('td')
    print(col.text)

    