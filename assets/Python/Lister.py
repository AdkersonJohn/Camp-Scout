import requests

headers = {
    'authority': 'www.reserveamerica.com',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.reserveamerica.com/campgroundDirectory.do',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'JSESSIONID=E8D696EA11939470404939A31B55EE6D.ue1-prod-aspiraone-web-13; AWSALB=k9mo635IhVr2puH6JvqdMwSdu2xNEXPvonJw0fSDs01UTi9Bc4d8wJ9daOH0QepD4HlAFPAiHE+tVttxgTe2j4wdwLTIp553mbh+TeQ2mmF+ZHujWCWOP81kJuI3; AWSALBCORS=k9mo635IhVr2puH6JvqdMwSdu2xNEXPvonJw0fSDs01UTi9Bc4d8wJ9daOH0QepD4HlAFPAiHE+tVttxgTe2j4wdwLTIp553mbh+TeQ2mmF+ZHujWCWOP81kJuI3',
}

params = (
    ('contractCode', 'ID'),
)

response = requests.get('https://www.reserveamerica.com/camping/alaska-state-parks/r/campgroundDirectoryList.do', headers=headers, params=params)

print(response.text)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.reserveamerica.com/camping/alaska-state-parks/r/campgroundDirectoryList.do?contractCode=AK', headers=headers)