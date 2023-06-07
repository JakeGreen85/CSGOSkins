import requests
from bs4 import BeautifulSoup
import time

def scrape_csgo_skin_prices():
    url = "https://steamcommunity.com/market/search/render/"
    app_id = 730  # CS:GO App ID
    start = 0  # Starting index of the items
    count = 10  # Number of items per request

    while True:
        params = {
            "appid": app_id,
            "start": start,
            "count": count
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            soup = BeautifulSoup(data["results_html"], "html.parser")
            item_listings = soup.find_all("a", class_="market_listing_row_link")

            for listing in item_listings:
                item_name_element = listing.find("span", class_="market_listing_item_name")
                item_name = item_name_element.text

                # Split item name and exterior
                print(item_name)

                item_price = listing.find("span", class_="normal_price").text.strip()

                # Get item picture
                item_picture = listing.find("img", class_="market_listing_item_img")
                item_picture_url = item_picture["src"]

                # Get quantity
                item_quantity = listing.find("span", class_="market_listing_num_listings_qty")
                item_quantity_value = item_quantity.text.strip()

                print(f"Name: {item_name}\nPrice: {item_price}\nQuantity: {item_quantity_value}\nPicture URL: {item_picture_url}\n")

            total_count = data["total_count"]
            start += count

            if start >= total_count:
                break

            time.sleep(1)

        else:
            print(f"Error: Request failed with status code {response.status_code}.")

scrape_csgo_skin_prices()
