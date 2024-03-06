import requests
from bs4 import BeautifulSoup
import re
import mysql.connector

baseurl = 'https://www.jumia.co.ke/'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

#MYSQL server connection
connection = mysql.connector.connect(
     host = 'localhost',
     user = 'root',
     port = 3306,
     password = 'qwerty',
     database = 'jumia'
)

#Create a cursor
cursor = connection.cursor()


product_links = []
for x in range(1,4):
    response = requests.get(f'https://www.jumia.co.ke/mlp-black-friday-h-stay-connected/smartphones/?price=10000-14999&page={x}#catalog-listing')
    print(response.status_code)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        product_list = soup.find_all('article', class_="prd _fb col c-prd")

        for item in product_list:
            for link in item.find_all('a', class_ = 'core', href = True):
                    product_links.append(baseurl+link['href'])

for link in product_links:
    response = requests.get(link,headers=headers)
    # print(response.status_code)

    soup = BeautifulSoup(response.content, 'lxml')
    name = soup.find('h1', class_ = "-fs20 -pts -pbxs").text.strip()

    rating_text = soup.find('div', class_ = 'stars _m _al').text
    rating_extract = re.search(r'(\d+(\.\d+)?)\s*(out\s*of)?\s*5', rating_text).group(1)

    price_text = soup.find('span', class_ = '-b -ubpt -tal -fs24 -prxs').text
    price_extract = int(re.search(r'(\d[\d,]*)', price_text).group(1).replace(',', ''))

    review_count = soup.find('a', class_ ='-plxs _more').text
    if review_count == '(No ratings available)':
         review_count_extract = 0
    else:
         review_count_extract = re.search(r'(\d+)', review_count).group(1)


    print(f'Saving: {name} to database')

    #Save data to MYSQL database
    values = (name,price_extract,rating_extract,review_count_extract,)
    sql = f'INSERT INTO phones (name, price, rating, rating_count) VALUES (%s,%s,%s,%s)'
    cursor.execute(sql, values)
    connection.commit()
    
    
    