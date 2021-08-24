import flask
from flask import jsonify, request, Response
import zlib
import json
import urllib.request
import urllib.parse
from urllib.error import HTTPError
from bs4 import BeautifulSoup

headers = {
    'Host': 'sslecal2.forexprostools.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://sslecal2.forexprostools.com',
    'Referer': 'https://sslecal2.forexprostools.com/?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&features=datepicker,timezone&countries=25,32,37,17,72,22,39,14,48,10,35,6,43,21,38,12,36,26,110,5,4&calType=week&timeZone=16&lang=8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/get_data', methods=['GET'])
def get_data():

    try:
        resData = []

        url = 'https://sslecal2.forexprostools.com/ajax.php'
        dateFrom = request.args.get('dateFrom')
        dateTo = request.args.get('dateTo')
        if (dateFrom == None and dateTo == None) or (dateFrom == "" and dateTo == ""):
            return Response(
                "You have to send date data",
                status=400,
            )
        # data = {
        #     'dateFrom': '2021-06-04',
        #     'dateTo': '2021-06-10',
        #     'timeframe': '',
        #     'columns': ['exc_flags', 'exc_currency', 'exc_importance', 'exc_actual', 'exc_forecast', 'exc_previous'],
        #     'timeZone': 16,
        #     'country': [25, 32, 37, 17, 72, 22, 39, 14, 48, 10, 35, 6, 43, 21, 38, 12, 36, 26, 110, 5, 4],
        #     'importance': [1, 2, 3],
        #     'category': ['_employment', '_economicActivity', '_inflation', '_credit', '_centralBanks', '_confidenceIndex', '_balance', '_Bonds'],
        #     'action': 'filter',
        #     'lang': 8
        # }

        # data = urllib.parse.urlencode(data).encode('utf-8')
        data = b'dateFrom=' + dateFrom.encode() + b'&dateTo=' + dateTo.encode() + b'&timeframe=&timeZone=16&columns[]=exc_flags&columns[]=exc_currency&columns[]=exc_importance&columns[]=exc_actual&columns[]=exc_forecast&columns[]=exc_previous&country[]=25&country[]=32&country[]=37&country[]=17&country[]=72&country[]=22&country[]=39&country[]=14&country[]=48&country[]=10&country[]=35&country[]=6&country[]=43&country[]=21&country[]=38&country[]=12&country[]=36&country[]=26&country[]=110&country[]=5&country[]=4&importance[]=1&importance[]=2&importance[]=3&action=filter&lang=8'

        req = urllib.request.Request(url)
        req.data = data
        req.headers = headers
        f = urllib.request.urlopen(req)
        decompressed_data = zlib.decompress(f.read(), 16+zlib.MAX_WBITS)
        response = json.loads(decompressed_data)
        table = response['renderedFilteredEvents']
        soup = BeautifulSoup(str(table), 'html.parser')
        trElems = soup.select('tr:not(.noHover.displayNone)')
        date = ""
        for trElem in trElems:
            dateElem = trElem.select_one('td.theDay')
            if dateElem:
                date = dateElem.text.strip()
                continue
            trData = {
                "time": "",
                "currency": "",
                "sentiment": 0,
                "event": "",
                "act": "",
                "fore": "",
                "prev": "",
                "diamond": 0,
                "date": "",
                "rowId": "",
                "attr_id": "",
            }

            trData["rowId"] = trElem.get("id")
            trData["attr_id"] = trElem.get("event_attr_id")

            timeElem = trElem.select_one('td.time')
            if timeElem:
                trData['time'] = timeElem.text.strip()
            flagCurElem = trElem.select_one('td.flagCur')
            if flagCurElem:
                trData['currency'] = flagCurElem.text.strip()
            sentimentElem = trElem.select_one('td.textNum.sentiment')
            if sentimentElem:
                trData['sentiment'] = len(sentimentElem.select(
                    'i.grayFullBullishIcon'))
            eventElem = trElem.select_one('td.event')
            if eventElem:
                trData['event'] = eventElem.text.strip()
            actElem = trElem.select_one('td.act')
            if actElem:
                trData['act'] = actElem.text.strip()
            foreElem = trElem.select_one('td.fore')
            if foreElem:
                trData['fore'] = foreElem.text.strip()
            prevElem = trElem.select_one('td.prev')
            if prevElem:
                trData['prev'] = prevElem.text.strip()
            diamondElem = trElem.select_one('td.diamond')
            if diamondElem:
                trData['diamond'] = len(diamondElem.select('span'))
            trData['date'] = date

            resData.append(trData)
        return jsonify(resData)
    except HTTPError as err:
        print(err)
        return jsonify('error')


@app.route('/get_detail', methods=['GET'])
def get_detail():
    event_attr_id = request.args.get('attr_id')

    url = "https://sslecal2.forexprostools.com/events_charts/eu/" + event_attr_id + ".json"

    if event_attr_id == None or event_attr_id == "":
        return Response(
            'attr_id is required',
            400
        )

    req = urllib.request.Request(url)
    req.headers = headers
    f = urllib.request.urlopen(req)
    decompressed_data = zlib.decompress(f.read(), 16+zlib.MAX_WBITS)
    response = json.loads(decompressed_data)
    # print(response)
    return jsonify(response)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
