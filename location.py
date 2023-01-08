import json
import requests
import re
import subprocess
import os

base_geolocation_api_url = "https://www.googleapis.com/geolocation/v1/geolocate?key="    #adres url do google geolocation api
base_geocoding_api_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="    #adres url go google geocoding api
api_key = "AIzaSyB1PUPXMdxyKLi3EdVufBQqWXbd-oIBxjs"                     #klucz api  (konto wnowogorski10@gmail.com)

complete_geolocation_api_url = base_geolocation_api_url + api_key
request = {'considerIp' : 'true'}
class LocationApi:
    @staticmethod
    def get_location():
        ### TWORZENIE ZAPYTANIA ###
        try:
            cmdout = subprocess.check_output('netsh wlan show networks mode=bssid').decode(encoding="437")      #zwraca dostępne wifi-access-pointy
            mac_addresses = re.findall(r'(?:[0-9a-fA-F]:?){12}', cmdout)    #\
            signals_quality = re.findall(r'([\d]+)(%)', cmdout)              #| parsowanie cmdout przy użyciu wyrażeń regularnych
            channels = re.findall(r'(Channel[\W]+: )([\d]+)', cmdout)       #/
            if not (len(mac_addresses) == len(signals_quality) == len(channels)):      #musi się zgadzac ilość adresów mac i odpowiadających im wartości jakości sygnału
                raise ("error")
        except:
            print("Unable to retrive wifi access points...")
        else:
            wifi_list = []                          #lista dostępnych punktów wifi
            for i in range(len(mac_addresses)):                     # pętla for uzupełnia wifi_list wartościami pobranymi przez komendę netsh
                wifi_list.append({'macAddress' : mac_addresses[i],
                                  'signalStrength' : str(int(signals_quality[i][0])/2-100),
                                  'channel' : channels[i][1]
                                  })
            request['wifiAccessPoints'] = wifi_list        #dodawanie wifi_list do zapytania


        ### OTRZYMYWANIE ODPOWIEDŹI ###

        try:
            response = requests.post(complete_geolocation_api_url, json=request)    #wysyłanie żądania
            loc = response.json()
            lat = loc['location']['lat']
            lng = loc['location']['lng']
            if 'error' in loc.keys():
                raise  requests.RequestException()
        except Exception as e:
            print(e)

        complete_geocoding_api_url = base_geocoding_api_url + str(lat) + "," + str(lng) + "&key=" + api_key     #żądanie do geocoding api
        try:
            cresponse = requests.get(complete_geocoding_api_url)
            cloc = cresponse.json()
        except Exception as e:
            print(e)

        json_object = json.dumps(cloc, indent=3)
        with open("loc.json", "w") as outfile:  # wrzucanie odpowiedzi do pliku json
            outfile.write(json_object)