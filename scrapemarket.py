import requests
from bs4 import BeautifulSoup
import time

def scrape_csgo_skin_prices():
    url = "https://steamcommunity.com/market/search/render/"
    app_id = 730  # CS:GO App ID
    start = 0  # Starting index of the items
    count = 10  # Number of items per request
    total_count = 50 # Total number of items to scrape

    # Scrape loop
    while True:
        params = {
            "appid": app_id,
            "start": start,
            "count": count
        }
        response = requests.get(url, params=params)

        if response.status_code == 200: # Success
            data = response.json()
            soup = BeautifulSoup(data["results_html"], "html.parser")
            item_listings = soup.find_all("a", class_="market_listing_row_link")

            for listing in item_listings:
                # Get item name
                item_name_element = listing.find("span", class_="market_listing_item_name")
                item_name = item_name_element.text

                # Get item price
                item_price = listing.find("span", class_="normal_price").text.strip()
                item_price = item_price.split()[2]

                # Get quantity
                item_quantity = listing.find("span", class_="market_listing_num_listings_qty")
                item_quantity_value = item_quantity.text.strip()

                # Get item picture
                item_picture = listing.find("img", class_="market_listing_item_img")
                item_picture_url = item_picture["src"]

                # Pretty-print
                print(f"Name: {item_name}\nPrice: {item_price}\nQuantity: {item_quantity_value}\nPicture URL: {item_picture_url}\n")

            # This will run the program for all items in the steam market database
            # (Commented out for testing)
            # total_count = data["total_count"] 


            # Increase the current index by the request count
            start += count

            # Check if total count has been reached
            if start >= total_count:
                break

            # Pause to reduce the chance of being rate-limited
            time.sleep(1)

        # If not success, then display error code
        else:
            print(f"Error: Request failed with status code {response.status_code}.")

scrape_csgo_skin_prices()