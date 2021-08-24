import urllib.request
import json
import urllib.parse
from urllib.error import HTTPError
import zlib
from bs4 import BeautifulSoup


class Scraper():

    def __init__(self):
        pass

    def scrape(self):

        try:
            url = 'https://sslecal2.forexprostools.com/ajax.php'

            data = {
                'dateFrom': '2021-06-01',
                'dateTo': '2021-06-06',
                'timeframe': '',
                'columns': ['exc_flags', 'exc_currency', 'exc_importance', 'exc_actual', 'exc_forecast', 'exc_previous'],
                'timeZone': 16,
                'country': [25, 32, 37, 17, 72, 22, 39, 14, 48, 10, 35, 6, 43, 21, 38, 12, 36, 26, 110, 5, 4],
                'importance': [1, 2, 3],
                'category': ['_employment', '_economicActivity', '_inflation', '_credit', '_centralBanks', '_confidenceIndex', '_balance', '_Bonds'],
                'action': 'filter',
                'lang': 8
            }

            data = urllib.parse.urlencode(data).encode('utf-8')
            # data = json.dumps(data).encode('utf-8')
            # data = "league=1\nSeasonString=2014-2015\nYear=1\nMonth=1\nDay=1"

            headers = {
                'Host': 'sslecal2.forexprostools.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                # 'Cookie': 'geoC=RU; __utmc=229954078; __utmz=229954078.1623461094.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=229954078.925252517.1623461094.1623461094.1623464489.2',
                'Accept-Encoding': 'gzip, deflate, br',
                'Origin': 'https://sslecal2.forexprostools.com',
                'Referer': 'https://sslecal2.forexprostools.com/?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&features=datepicker,timezone&countries=25,32,37,17,72,22,39,14,48,10,35,6,43,21,38,12,36,26,110,5,4&calType=week&timeZone=16&lang=8',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Connection': 'keep-alive',
                'X-Requested-With': 'XMLHttpRequest',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'
            }

            req = urllib.request.Request(url)
            req.data = data
            req.headers = headers
            f = urllib.request.urlopen(req)
            decompressed_data = zlib.decompress(f.read(), 16+zlib.MAX_WBITS)
            # soup = BeautifulSoup(decompressed_data, 'html.parser')
            print(decompressed_data)
        except HTTPError as err:
            # print(err.read().decode("utf8", 'ignore'))
            print(err)
        return 'okay'
