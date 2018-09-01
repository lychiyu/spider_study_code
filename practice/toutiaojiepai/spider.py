# coding: utf-8

"""
 Created by liuying on 2018/9/1.
"""
import json
import os
import re
from multiprocessing.pool import Pool

import pymongo
import requests
from hashlib import md5
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from config import *

client = pymongo.MongoClient(MONGO_HOST, connect=False)
db = client[MONGO_DB]


def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab',
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        res = requests.get(url)
    except RequestException:
        print('get page index err')
        return None
    if res.status_code == requests.codes.ok:
        return res.text
    return None


def parse_page_index(text):
    data = json.loads(text)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            if 'image_list' in item.keys():
                yield item.get('article_url')


def get_page_detail(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    }
    try:
        res = requests.get(url, headers=headers)
    except RequestException:
        print('get page index err ', url)
        return None
    if res.status_code == requests.codes.ok:
        return res.text
    return None


def parse_page_detail(text, url):
    soup = BeautifulSoup(text, 'lxml')
    title = soup.select('title')[0].get_text()
    pattern = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
    result = re.search(pattern, text)
    images = []
    if result:
        data = json.loads(json.loads(('"' + result.group(1) + '"')))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
    for img in images:
        download_img(img, title)
    return {'url': url, 'title': title, 'images': images}


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('true', result)
        return True
    return False


def download_img(url, title):
    print(f'downloadimg {url}')
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    }
    try:
        res = requests.get(url)
    except RequestException:
        print('download_img err ', url)
        return None
    if res.status_code == requests.codes.ok:
        return save_img(res.content, title)
    return None


def save_img(content, title):
    dir_path = f'{os.getcwd()}/images/{title}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, f'{md5(content).hexdigest()}.jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    result = get_page_index(offset, KEYWORDS)
    for url in parse_page_index(result):
        detail = get_page_detail(url)
        if detail:
            result = parse_page_detail(detail, url)
            if result:
                save_to_mongo(result)


if __name__ == "__main__":
    groups = [x * 20 for x in range(START, END + 1)]
    pool = Pool()
    pool.map(main, groups)
