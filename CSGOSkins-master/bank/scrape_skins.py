import json
import requests # make http requests

from bank.models import create_tables, insert_asset_description

cookie = {'steamLoginSecure': '76561198070606333%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MENFRV8yMjEzMUEzMF81MkI5RCIsICJzdWIiOiAiNzY1NjExOTgwNzA2MDYzMzMiLCAiYXVkIjogWyAid2ViIiBdLCAiZXhwIjogMTY4NTcyMjA2OCwgIm5iZiI6IDE2NzY5OTUzMTIsICJpYXQiOiAxNjg1NjM1MzEyLCAianRpIjogIjBEMzBfMjJBMDFFM0VfRjY2RUYiLCAib2F0IjogMTY3NjQxMzA2OSwgInJ0X2V4cCI6IDE2OTQ1OTI5MTcsICJwZXIiOiAwLCAiaXBfc3ViamVjdCI6ICIxODUuMTIxLjE3NC4xMzMiLCAiaXBfY29uZmlybWVyIjogIjE4NS4xMjEuMTc0LjEzMyIgfQ.rkTS3CYuYRakaZL7YQVm_LbP-3EP7PykOtj1JGi0B9nu8teiOAX4l0hQLs3GbU_QABxTC4jxO3ZWzIm2nOmkBQ'}
imagePath = 'https://community.cloudflare.steamstatic.com/economy/image/'
webAPIKey = 'C34AF91C568BBF6D3D031292210741A3'
token = 'ce4090bc6a3c4acbaf7f6d05b5eb5888'
steamID = '76561198070606333'
gameID = '730'
count = '50'


def init_database():
	# find total number items
	allItemsGet = requests.get('https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&appid='+gameID+'&norender=1&count='+count, cookies=cookie) # get page
	allItems = allItemsGet.content; # get page content
	allItems = json.loads(allItems); # convert to JSON
		

	create_tables()

	for result in allItems['results']:
		classid = result['asset_description']['classid']
		instanceid = result['asset_description']['instanceid']
		icon_url = result['asset_description']['icon_url']
		sell_price = result['sell_price']
		
		itemGet = requests.get('https://api.steampowered.com/ISteamEconomy/GetAssetClassInfo/v1/?access_token='+token+'&appid='+gameID+'&class_count=1&classid0='+classid+'&instanceid0='+instanceid)
		item = itemGet.content; # get page content
		item = json.loads(item)
		
		if(instanceid == '0'):
			name = item['result'][classid]['name']
		else:
			name = item['result'][classid + '_' + instanceid]['name']	
			
		insert_asset_description((classid), int(instanceid), name, sell_price, icon_url)

