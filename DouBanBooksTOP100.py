import requests
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException
cnt = 0

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_html(html):

    pattern = re.compile('<table width="100%">.*?<img src="(.*?)" width=.*?</a>'
                         + '.*?<a href=.*?title="(.*?)".*?<p class="pl">(.*?)</p>'
                         + '.*?"rating_nums">(.*?)</span>.*?<span class="pl">\D\s+(.*?)\D+</span>', re.S)

    items = re.findall(pattern,html)
    for item in items:
        yield {
            'comments': item[4],
            'title':item[1],
            'rating': item[3],
            'info':item[2],
            'pic':item[0]

        }


def save_data(name,data):
    with open(name+'.txt','a',encoding='utf_8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
        f.close()


def main(num):
    global cnt
    url = 'https://book.douban.com/top250?start='+str(num)
    html = get_one_page(url)
    for item in parse_html(html):
        print(item)
        cnt += 1
        save_data('result',item)
    print(cnt)

if __name__ == '__main__':

    pool = Pool()
    pool.map(main,[25*i for i in range(10)])


