#!/usr/bin/python3

'''
    Fast-PROX - utility for checking proxy in terminal under the GNU GPL V3.0 License
    ORIGINAL AUTHORS: Hasanov Abdurahmon & Ilyosiddin Kalandar
    MODIFIED BY: YellowRoseCx
    Version: 0.2.5
'''

from sys import argv
import urllib3
import os
from os import system as terminal
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty

URL = "http://google.com"
CMD_CLEAR_TERM = "clear" if os.name != "nt" else "cls"
TIMEOUT = (3.05, 27)
MAX_THREADS = 10
goods = 0

def check_proxy(proxy):
    '''
        Function for checking proxy. Returns ERROR if the proxy is bad, otherwise returns None.
    '''
    try:
        session = requests.Session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        session.max_redirects = 300
        proxy = proxy.split('\n', 1)[0]
        print(Fore.LIGHTYELLOW_EX + 'Checking ' + proxy)
        session.get(URL, proxies={'http': 'http://' + proxy}, timeout=TIMEOUT, allow_redirects=True)
    except requests.exceptions.ConnectionError as e:
        print(Fore.LIGHTRED_EX + 'Error!')
        return e
    except requests.exceptions.ConnectTimeout as e:
        print(Fore.LIGHTRED_EX + 'Error, Timeout!')
        return e
    except requests.exceptions.HTTPError as e:
        print(Fore.LIGHTRED_EX + 'HTTP ERROR!')
        return e
    except requests.exceptions.Timeout as e:
        print(Fore.LIGHTRED_EX + 'Error! Connection Timeout!')
        return e
    except urllib3.exceptions.ProxySchemeUnknown as e:
        print(Fore.LIGHTRED_EX + 'ERROR unknown Proxy Scheme!')
        return e
    except requests.exceptions.TooManyRedirects as e:
        print(Fore.LIGHTRED_EX + 'ERROR! Too many redirects!')
        return e

def process_proxy(queue):
    global goods
    while True:
        try:
            proxy = queue.get(timeout=1)
            try:
                if check_proxy(proxy):
                    print(Fore.LIGHTRED_EX + 'Bad proxy ' + proxy)
                else:
                    print(Fore.LIGHTGREEN_EX + 'Good proxy ' + proxy)
                    with open('good.txt', 'a') as file_with_goods:
                        file_with_goods.write(proxy)
                        goods += 1
            except KeyboardInterrupt:
                print(Fore.LIGHTGREEN_EX + '\nExit.')
                exit()
        except Empty:
            break

def process_proxies(proxies):
    terminal(CMD_CLEAR_TERM)
    print(Fore.LIGHTCYAN_EX + '===========================================')
    proxy_queue = Queue()
    for proxy in proxies:
        proxy_queue.put(proxy)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        threads = []

        # Start the initial threads
        for _ in range(MAX_THREADS):
            thread = executor.submit(process_proxy, proxy_queue)
            threads.append(thread)

        # Wait for the initial threads to complete
        for thread in threads:
            thread.result()

    print(Fore.LIGHTCYAN_EX + '===========================================')
    print(Fore.LIGHTGREEN_EX + 'Total ' + str(goods) + ' good proxies found')
    print(Fore.LIGHTRED_EX + 'And ' + str(len(proxies) - goods) + ' are bad')
    print(Fore.LIGHTYELLOW_EX + 'Have a nice day! :)')
    print()

def print_help():
    terminal(CMD_CLEAR_TERM)
    print(Fore.LIGHTGREEN_EX + 'Fast-PROX v0.2.5 - Utility for checking proxy in terminal')
    print(Fore.LIGHTGREEN_EX + 'Original Authors: Hasanov Abdurahmon & Ilyosiddin Kalandar')
    print(Fore.LIGHTGREEN_EX + 'Modified By: YellowRoseCx')
    print(Fore.LIGHTCYAN_EX)
    print('Usage -> prox -f <filename> - Check file with proxies')
    print('prox -p <proxy> - check only one proxy')
    print('prox --help - show this menu')


if len(argv) > 1:
    commands = ['--help', '-h', '-f', '-p', '/?', '--?','--file','-file','--proxy','-proxy']
    if argv[1] in commands:
        if argv[1] in ('--help', '-help', '/?', '--?'):
            print_help()
        elif argv[1] in ('-f', '--file', '-file'):
            try:
                with open(argv[2], 'r') as file:
                    proxies = list(file)
                    process_proxies(proxies)
            except FileNotFoundError:
                print(Fore.LIGHTRED_EX + 'Error!\nFile Not found!')
            except IndexError:
                print(Fore.LIGHTRED_EX + 'Error!\nMissing filename!')
        elif argv[1] in ('-p', '--proxy', '-proxy'):
            try:
                argv[2] = argv[2].split(' ')[0]
                process_proxy(argv[2])
            except IndexError:
                print(Fore.LIGHTRED_EX + 'Error! Missing proxy!')
    else:
        print(Fore.LIGHTRED_EX + 'Unknown option \"' + argv[1] + '\"')
else:
    print_help()
