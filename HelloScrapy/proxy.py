import requests
from bs4 import BeautifulSoup

FILE_NAME = 'host.txt'


def fetch_proxy(num):
    api = 'http://www.xicidaili.com/nn/{}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

    fp = open(FILE_NAME, 'w', encoding='utf-8')
    for i in range(num + 1):
        api = api.format(i + 1)
        response = requests.get(api, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        tr_list = soup.find_all('tr', attrs={'class': 'odd'})
        for tr in tr_list:
            try:
                tds = tr.find_all('td')
                ip = tds[1].text
                port = tds[2].text
                print(ip, port)
                fp.write('{}\t{}\n'.format(ip, port))
            except Exception as e:
                print('error')
    fp.close()


def verify():
    fp = open(FILE_NAME, 'r')
    proxies = []
    for line in fp.readlines():
        line = line.strip().split('\t')
        proxy = 'http://{}:{}'.format(line[0], line[1])
        proxies.append({'proxy': proxy})

    fp2 = open('valid_host.txt', 'w')
    for proxy in proxies:
        try:
            response = requests.get('https://www.baidu.com', proxies=proxy)
            if response.status_code == 200:
                fp2.write('{}\n'.format(proxy['proxy']))
            print(proxy, response.status_code)
        except Exception as e:
            print(e)

    fp2.close()


def do_proxy():
    fetch_proxy(10)
    verify()


if __name__ == '__main__':
    do_proxy()
