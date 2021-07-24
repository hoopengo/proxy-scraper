#!/usr/bin/env python3
"""from @hold-lib:1.1"""
import requests
from sys import argv
from prettytable import PrettyTable
from colorama import Fore, Style
from random import randint
from progress.spinner import MoonSpinner
from time import sleep
import threading as th


# default_config
vers = '0.1'
config = {
'l': '',               # Кол-во прокси
'proxy': 'http,https', # Типы прокси
'p': '',               # Порт
'ms': ''               # Время отклика
}

# Проверка параметров
for v,i in enumerate(argv):
    if i == '-l':
        try:
           config['l'] = int(argv[v+1])
        except Exception:
            print("-l [len]", "Не указано количество прокси!")
            exit()

    if i == '-p':
        try:
            config['p'] = argv[v+1] if argv[v+1][1:] not in config else ''
        except Exception:
            pass
    
    if i == '-ms':
        try:
            config['ms'] = argv[v+1]
        except Exception:
            print("-ms [ping]", "Не указана маскимальная задержка!")
            exit()

    if i == '--proxy':
        try:
            config['proxy'] = argv[v+1]
        except Exception:
            pass
    
    if i in ['--help', '-h']:
        print('''использование: proxysc [--version or -V] [--help or -h] [-l <кол-во прокси>]
           [-p <port>] (-p 80) [-ms <ping>] (-ms 1500)
           [--proxy <list>] (--proxy http,https,socks4,socks5)
           <command> [<args>]''')
        exit()

    if i in ['--version', '-V']: 
        print(vers)
        exit()

table = PrettyTable(['count', 'proxy', 'ports', 'ms'])
table.add_row([f"{config['l'] if config['l'] != '' else 'all'}",
               f"{f'{Fore.GREEN}http{Style.RESET_ALL}' if 'h' in config['proxy'] else f'{Fore.RED}http{Style.RESET_ALL}'}, {f'{Fore.GREEN}https{Style.RESET_ALL}' if 's' in config['proxy'] else f'{Fore.RED}https{Style.RESET_ALL}'}, {f'{Fore.GREEN}socks4{Style.RESET_ALL}' if '4' in config['proxy'] else f'{Fore.RED}socks4{Style.RESET_ALL}'}, {f'{Fore.GREEN}socks5{Style.RESET_ALL}' if '5' in config['proxy'] else f'{Fore.RED}socks5{Style.RESET_ALL}'}",
               config["p"] if config["p"] != '' else 'any',
               config["ms"] if config["ms"] != '' else 'any'
])

logo = (
f'''{Fore.GREEN}
██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗     ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝     ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝█████╗███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝ ╚════╝╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║        ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
{Fore.CYAN}[from hold-lib]
{Style.RESET_ALL}'''
)

print(logo)
print(table, '\n')

finished = False

def target():
    spinner = MoonSpinner('  Подключение к API\r')
    while not finished:
        spinner.next()
        sleep(0.1)

t = th.Thread(target=target, daemon=True)
t.start()

r = requests.get(f"https://api.proxyscrape.com/?request=getproxies&proxytype=" + config['proxy'] + "&timeout=" + str(config['ms']) + "&limit=" + str(config['l']))
finished = True

proxys = (r.text).split('\n') if input('\rВывести прокси? (y/n): ') == 'y' else ''
print('\n'.join([i for i in proxys if i.endswith(f'{config["p"]}\r')]))

if input('Сохранить прокси? (y/n): ') == 'y':
    with open(f'basic-proxy-{randint(1,10000)}.txt', 'w', encoding='utf-8') as f:
        f.write(r.text)

print("Done ✔")
