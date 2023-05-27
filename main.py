import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd

# Function to search for products and extract their details
def search_products(product_query):
    search_url = 'https://www.finn.no/bap/forsale/search.html?q=' + urllib.parse.quote(product_query) + '&sort=RELEVANCE'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_list = soup.find_all('article', class_='ads__unit')  # Adjust the selector to find the appropriate product elements
    products = []

    for product in product_list:
        product_name = product.find('a', class_='ads__unit__link').text.strip()

        product_location_elem = product.find('div', class_='ads__unit__content__details')
        product_location = product_location_elem.find_all('div')[-1].text.strip() if product_location_elem else 'Location not found'

        product_price_elem = product.find('div', class_='ads__unit__img__ratio__price')
        product_price = product_price_elem.text.strip() if product_price_elem else 'Price not found'

        product_link = 'https://www.finn.no' + product.find('a', class_='ads__unit__link')['href']

        products.append({
            'Name': product_name,
            'Location': product_location,
            'Price': product_price,
            'Link': product_link
        })

    return products

# Prompt the user for the product name
product_name = input('Enter the product name: ')

# Search for the products and extract their details
products = search_products(product_name)

# Display the results
if products:
    for product in products:
        print('Name:', product['Name'])
        print('Location:', product['Location'])
        print('Price:', product['Price'])
        print('Link:', product['Link'])
        print('-' * 50)
else:
    print('No products found.')

# Export the results to an Excel sheet
df = pd.DataFrame(products)
df.to_excel('product_results.xlsx', index=False)
print('Results exported to product_results.xlsx')
