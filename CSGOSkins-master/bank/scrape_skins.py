import json
import requests # make http requests

from bank.models import create_tables, insert_asset

qualities = ["Well-Worn", "Factory New", "Minimal Wear", "Battle-Scarred", "Field-Tested"]

cookie = {'steamLoginSecure': '76561198177735706%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MThEMF8yNTBEMjI4Rl85OEE0NSIsICJzdWIiOiAiNzY1NjExOTgxNzc3MzU3MDYiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MjY2NzE5NjgsICJuYmYiOiAxNzE3OTQ1NDg3LCAiaWF0IjogMTcyNjU4NTQ4NywgImp0aSI6ICIxNjRCXzI1MEQyMTJBX0Q4MUY2IiwgIm9hdCI6IDE3MjY1ODU0ODcsICJydF9leHAiOiAxNzQ0NTQ0MTIxLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiMTMxLjE2NC4yMTEuNTYiLCAiaXBfY29uZmlybWVyIjogIjEzMS4xNjQuMjExLjU2IiB9.IeHbcI617erXZpcsEReWo-BWglx463WMyEYt3sE1IYy5xsY9grUxCtDM8u89fFjEKN4KqaBa_PNZftzbYKieDw'}
icon_path = 'https://community.cloudflare.steamstatic.com/economy/image/'
webAPIKey = '0F7DDCACDE7F7DFB4EA42CE1FCF501B2'
token = 'ce4090bc6a3c4acbaf7f6d05b5eb5888'
steamID = '76561198018670985'
gameID = '730'
count = '100'


def init_database():
	# find total number items
	allItemsGet = requests.get('https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&appid='+gameID+'&norender=1&count='+count, cookies=cookie) # get page
	allItems = allItemsGet.content; # get page content
	allItems = json.loads(allItems); # convert to JSON

	create_tables()

	for result in allItems["results"]:
		classid = result['asset_description']['classid']
		instanceid = result['asset_description']['instanceid']
		icon_url = icon_path + result['asset_description']['icon_url']
		sell_price = result['sell_price']
		quantity = result['sell_listings']
		
		if(instanceid == '0'):
			itemid = classid
		else:
			itemid = classid + '_' + instanceid
		
		name = result['asset_description']['name']	
		quality = ""
		for q in qualities:
			if(result["name"][-len(q)-1:-1] in qualities):
				quality = q
				break
		insert_asset((classid), int(instanceid), name, sell_price, quality, icon_url, quantity)

