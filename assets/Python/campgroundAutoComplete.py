import requests
import json

def searchAuto(campGroundTarget):
    campGroundTarget = input("Please enter the name of the campgound you wish to select(NO TYPOS BRUH): ")
    campgroundHeaders = {
        'authority': 'www.recreation.gov',
        'accept': 'application/json, text/plain, */*',
        'pragma': 'no-cache',
        'cache-control': 'no-cache, no-store, must-revalidate',
        'authorization': '',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.recreation.gov/',
        'accept-language': 'en-US,en;q=0.9',
    }
    campgroundParams = (
        ('q', campGroundTarget),
        ('geocoder', 'true'),
    )
    campgroundResponse = requests.get('https://www.recreation.gov/api/search/suggest', headers=campgroundHeaders, params=campgroundParams)
    campgroundData = json.loads(campgroundResponse.text)
    # print(campgroundData)
    # print(campgroundData)
    campgroundSuggestion= campgroundData['inventory_suggestions'][0]['name']
    # print(campgroundSuggestion)
    return campgroundSuggestion


