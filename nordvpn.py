#!/usr/bin/python3

import requests
import json
import os
import sys

URLS = {"country_codes" : "https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_countries", "recommendation" : "https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations&filters={{%22country_id%22:{}}}"}
DEFAULT_CO = "SE"
UDP_LINK = "https://downloads.nordcdn.com/configs/files/ovpn_legacy/servers/{}.udp1194.ovpn"

def load_countries():
    a = requests.get(URLS['country_codes'])

    return a.json()

def find_country(code):
    for country in get_countries():
        if country['code'].upper() == code.upper():
            return country

def load_recommendations(code=DEFAULT_CO):
    c_id = find_country(code)['id']
    url = URLS['recommendation'].format(c_id)
    #print("url: {}, code: {}, id: {}".format(url, code, c_id))
    a = requests.get(url)

    return a.json()

def load_config(host):
    #print('Downloading {}'.format(UDP_LINK.format(host)))
    a = requests.get(UDP_LINK.format(host))
    with open(os.path.join('configs',host+'.ovpn'), 'wb') as f:
        f.write(a.content)


def get_countries():
    if not os.path.isfile('cached_countries.json'):
        countries = load_countries()
        with open('cached_countries.json', 'w') as f:
            f.write(json.dumps(countries))
    else:
        with open('cached_countries.json', 'r') as f:
            countries = json.loads(f.read())

    return countries


def main():
    code = sys.argv[1]
    countries = get_countries()
    server = load_recommendations(code)[0]

    #print("host: {}".format(server['hostname']))
    
    path = os.path.join('configs',server['hostname']+'.ovpn')
    if not os.path.isfile(path):
        #print('{} not found')
        load_config(server['hostname'])

    with open(path, 'r') as f:
        pass
        #print(f.read())

    print(server['hostname']+'.ovpn')

    return server['hostname']+'.ovpn'

if __name__ == '__main__':
    main()
