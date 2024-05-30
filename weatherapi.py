__author__ = 'suriyakumar.s2'

import json
import re
import requests
from datetime import date

class TestPage:
    def dataExtraction(self, soup, url):
        dataList = []
        InputCountryName = re.findall('q=([^"]+)', url)[0]
        
        for weatherName in soup:
            data = {}
            cityName = weatherName['name']
            apiKey = re.findall('key=.*?&', url)[0].replace('&', '').replace('key=', '')
            forecasturl = f'http://api.weatherapi.com/v1/forecast.json?key={apiKey}&q={cityName}&days=5&aqi=yes&alerts=yes'
            headers = {
                "Host": "api.weatherapi.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
            }
            response = requests.get(forecasturl, headers=headers)
            responseUrl = response.content.decode('utf-8')

            if InputCountryName in responseUrl:
                regionsData = json.loads(responseUrl)
                data['Name'] = regionsData['location']['name'] + ', ' + regionsData['location']['country']
                data['Coordinates'] = f"latitude: {regionsData['location']['lat']}, longitude: {regionsData['location']['lon']}"
                tempData = regionsData['forecast']['forecastday']
                temList = [str(i['day']['avgtemp_f']) for i in tempData]
                avgT = sum(map(float, temList)) / len(temList)
                data['averageTemperature'] = "{:.2f}".format(avgT)
                
                curforecasturl = f'http://api.weatherapi.com/v1/current.json?key={apiKey}&q={cityName}&aqi=yes'
                cur_response = requests.get(curforecasturl)
                cur_responseUrl = cur_response.content.decode('utf-8')
                
                if InputCountryName in cur_responseUrl:
                    curTempData = json.loads(cur_responseUrl)
                    data['currentTemperature'] = curTempData['current']['temp_f']
            
            dataList.append(data)
        
        return dataList

def parse(urlResponse, url):
    soup = json.loads(urlResponse)
    test_page_object = TestPage()
    output = test_page_object.dataExtraction(soup, url)
    print(json.dumps(output, indent=2))
    return output

if __name__ == '__main__':
    url = 'http://api.weatherapi.com/v1/search.json?key=5dad4c31e4434311a8e132245222103&q=Germany'
    headers = {
        "Host": "api.weatherapi.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    urlResponse = response.content.decode('utf-8')
    parse(urlResponse, url)
