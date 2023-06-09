#!/usr/bin/python3

from bs4 import BeautifulSoup
import re
import time
import signal
import sys
import requests
import random
import html
import re
from colorama import Fore, Style
from shodan import Shodan
import shodan
import os

banner = [
    "_______________________________________________________________________________",
    "",
    " ▄▄▄▄   ▓█████  ██░ ██  ██▓ ███▄    █ ▓█████▄    ▓██   ██▓ ▒█████   █    ██ ",
    "▓█████▄ ▓█   ▀ ▓██░ ██▒▓██▒ ██ ▀█   █ ▒██▀ ██▌    ▒██  ██▒▒██▒  ██▒ ██  ▓██▒",
    "▒██▒ ▄██▒███   ▒██▀▀██░▒██▒▓██  ▀█ ██▒░██   █▌     ▒██ ██░▒██░  ██▒▓██  ▒██░",
    "▒██░█▀  ▒▓█  ▄ ░▓█ ░██ ░██░▓██▒  ▐▌██▒░▓█▄   ▌     ░ ▐██▓░▒██   ██░▓▓█  ░██░",
    "░▓█  ▀█▓░▒████▒░▓█▒░██▓░██░▒██░   ▓██░░▒████▓      ░ ██▒▓░░ ████▓▒░▒▒█████▓ ",
    "░▒▓███▀▒░░ ▒░ ░ ▒ ░░▒░▒░▓  ░ ▒░   ▒ ▒  ▒▒▓  ▒       ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ",
    "▒░▒   ░  ░ ░  ░ ▒ ░▒░ ░ ▒ ░░ ░░   ░ ▒░ ░ ▒  ▒     ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░ ",
    " ░    ░    ░    ░  ░░ ░ ▒ ░   ░   ░ ░  ░ ░  ░     ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░ ",
    " ░         ░  ░ ░  ░  ░ ░           ░    ░        ░ ░         ░ ░     ░     ",
    "      ░                                ░          ░ ░                       ",
    "OSINT TOOL",
    "",
    "",
    "Author ➠ Bl4cksku11",
    "Github ➠ https://github.com/bl4cksku11",
    "Blog   ➠ https://blackskull.gitbook.io",
    "",
    "______________________________________________________________________________"
]

for line in banner:
    print(line)
    time.sleep(0.1)

shodan_api_key = 'PUT_YOU_API_KEY_HERE'
api = shodan.Shodan(shodan_api_key)

# Funcitions
#IP LOOKUP
def ip_lookup():
    ip = input("Enter target IP: ") #input
    try:
        ipinfo = api.host(ip)
        print("\nExecuting IP lookup...")
        for i in range(5):
            time.sleep(0.1)
            sys.stdout.write("\rProgress: [{0}{1}] {2}%".format('▦' * i, ' ' * (5-i), (i+1)*20))
            sys.stdout.flush()
        print("\nIP LOOKUP COMPLETED\n")
        # Give format to the response
        formatted_output = re.sub(r"[\[\]']", "", str(ipinfo))
        formatted_output = html.unescape(formatted_output)
        formatted_output = formatted_output.replace(",", ",\n")
        formatted_output = re.sub('<.*?>', '', formatted_output)
        print(formatted_output)
    except shodan.APIError as e:
        print('Error: {}'.format(e))

#DOMAIN LOOKUP
def domain_lookup():
    domain = input("Enter target domain: ")
    try:
        domain_info = api.search('hostname:' + domain)
        print("\n\nExecuting domain lookup...")
        for i in range(5):
            time.sleep(0.1)
            sys.stdout.write("\rProgress: [{0}{1}] {2}%".format('▦' * i, ' ' * (5-i), (i+1)*20))
            sys.stdout.flush()
        print("\nDOMAIN LOOKUP COMPLETED\n")
        # Give format to the response
        formatted_output = re.sub(r"[\[\]']", "", str(domain_info))
        formatted_output = html.unescape(formatted_output)
        formatted_output = formatted_output.replace(",", ",\n")
        formatted_output = re.sub('<.*?>', '', formatted_output)
        print(formatted_output)
    except shodan.APIError as e:
        print('Error: {}'.format(e))

#GEOPING
def geonet_geoping():
    domain = input("Enter target domain: ")
    url = f"https://geonet.shodan.io/api/geoping/{domain}"
    try:
        print("\n\nExecuting Geoping...")
        for i in range(5):
            time.sleep(0.1)
            sys.stdout.write("\rProgress: [{0}{1}] {2}%".format('▦' * i, ' ' * (5-i), (i+1)*20))
            sys.stdout.flush()
        print("\nGEOPING COMPLETED\n")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for result in data:
                ip = result['ip']
                is_alive = result['is_alive']
                min_rtt = result['min_rtt']
                avg_rtt = result['avg_rtt']
                max_rtt = result['max_rtt']
                city = result['from_loc']['city']
                country = result['from_loc']['country']
                latlon = result['from_loc']['latlon']

                print("IP:", ip)
                print("Is Alive:", is_alive)
                print("Min RTT:", min_rtt)
                print("Avg RTT:", avg_rtt)
                print("Max RTT:", max_rtt)
                print("City:", city)
                print("Country:", country)
                print("LatLon:", latlon)
                print()  # Jump point
        else:
            print("Error:", response.status_code)
    except requests.RequestException as e:
        print("Error:", str(e))

# Define the signal handler to capture Ctrl+C
def signal_handler(signal, frame):
    print("\n\nExiting program...")
    for i in range(5):
        time.sleep(0.1)
        sys.stdout.write("\rProgress: [{0}{1}] {2}%".format('▦' * i, ' ' * (5-i), (i+1)*20))
        sys.stdout.flush()
    print("\nSEE YOU SOON!!!")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def clear_screen():
    os.system('clear')

# Menú
while True:
    print("━━━━━ Menu ━━━━━")
    print("1. IP LOOKUP")
    print("2. DOMAIN LOOKUP")
    print("3. GEOPING")
    print("0. Clear screen")

    opcion = input("Select your option: ")

    if opcion == "1":
        ip_lookup()
    elif opcion == "2":
        domain_lookup()
    elif opcion == "3":
        geonet_geoping()
    elif opcion == "0":
        clear_screen()
    else:
        print("✕✕✕ Invalid option. ✕✕✕")
