# coding: utf-8

"""
 Created by liuying on 2018/9/4.
"""
import json
import re
from datetime import datetime

import pymongo
import requests
from lxml.etree import XMLSyntaxError
from requests.exceptions import RequestException, ConnectionError
from pyquery import PyQuery as pq
from config import *

proxy = None
max_req_count = 5

client = pymongo.MongoClient(MONGO_HOST, connect=False)
db = client[MONGO_DB]


def get_proxy():
    proxy_url = 'http://127.0.0.1:5001/random'
    try:
        res = requests.get(proxy_url)
        if res.status_code == 200:
            return json.loads(res.text)
        return None
    except ConnectionError:
        return None


def get_html(url, params=None, count=0):
    if count >= max_req_count:
        print("request count max")
        return None
    global proxy
    headers = {
        'Cookie': 'SUV=00125394B49F30AB5A8D7B8BDCDF9774; CXID=1452B6FA481B2E72916DBE103EDD9B31; SUID=F90E5D654C238B0A5AB5C62500015910; wuid=AAGQCLsNHwAAAAqLFD3d1QUApwM=; ad=zVlHSkllll2zHtYOlllllVmpjsllllllBq1nMyllll9lllll4v7ll5@@@@@@@@@@; IPLOC=CN4403; SNUID=1B18E8B3CACFBE3D5D5B323CCBE821A7; ABTEST=8|1535977320|v1; weixinIndexVisited=1; JSESSIONID=aaaU_9aOgduJbeHTHDBvw; sct=1; ppinf=5|1535991228|1537200828|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTYlOTclQTAlRTglODAlQkIlRTYlQjclQjclRTglOUIlOEJ8Y3J0OjEwOjE1MzU5OTEyMjh8cmVmbmljazozNjolRTYlOTclQTAlRTglODAlQkIlRTYlQjclQjclRTglOUIlOEJ8dXNlcmlkOjQ0Om85dDJsdUk2LVloN0RYQmhqNjdWclNQQ1dqSjBAd2VpeGluLnNvaHUuY29tfA; pprdig=XCnEOVQlldnqPgMakbzOJX911jRvTYPC_5tYabunrKcgKYBwJj8_A6fhtNka_JYIni7nSnf9nnH3N02kMdpmgPb7L3pvC0r2UK-r8CqOSeSeauWRQgxJMTH41UYfU_hoVQ6aDSV-kpCXp2BljZNqYgSUrXPQ__JzC9XC_XGS_iA; sgid=08-36954651-AVuNXbzQ3KyI8fjPgtia8PXE; ppmdig=1535991228000000178b8cf35487153adbe30b3d7770044f',
        'Host': 'weixin.sogou.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        if proxy:
            proxies = {proxy['scheme']: f'{proxy["scheme"]}://{proxy["proxy"]}'}
            res = requests.get(url, params=params, headers=headers, allow_redirects=False, proxies=proxies)
        else:
            res = requests.get(url, params=params, headers=headers, allow_redirects=False)
    except RequestException:
        count += 1
        print('get error')
        proxy = get_proxy()
        return get_html(url, params, count)
    if res.status_code == requests.codes.ok:
        return res.text
    if res.status_code == requests.codes.found:
        proxy = get_proxy()
        if proxy:
            print('using proxy', proxy)
            return get_html(url, params)
        else:
            print('get proxy fail')
            return None


def get_index(keyword, page):
    params = {
        'query': keyword,
        'type': 2,
        'page': page,

    }
    url = 'http://weixin.sogou.com/weixin'
    return get_html(url, params)


def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')


def parse_detail(url):
    try:
        res = requests.get(url)
        if res.status_code == requests.codes.ok:
            detail = res.text
        else:
            detail = None
    except RequestException:
        detail = None
    print(url)
    if detail:
        try:
            doc = pq(detail)
            title = doc('.rich_media_title').text()
            content = doc('.rich_media_content').text()
            pub_date = re.compile(r'.*?<em id="publish_time".*?">(.*?)</em>').search(detail).group(1)
            if pub_date == '今天' or pub_date == "":
                pub_date = datetime.now().date().strftime('%Y-%m-%d')
            nick_name = doc('#js_profile_qrcode > div > strong').text()
            mp_name = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
            return {
                'title': title,
                'pub_date': pub_date,
                'nick_name': nick_name,
                'mp_name': mp_name,
                'url': url,
                'content': content
            }
        except XMLSyntaxError:
            return None
    return None


def save_to_mongo(result):
    # 根据url进行更新
    if db[MONGO_TABLE].update({'url': result['url']}, result, True):
        print('save success')
    else:
        print(f'save {result} failed')


def main():
    for page in range(1, 101):
        html = get_index(KEYWORDS, page)
        if html:
            urls = parse_index(html)
            for url in urls:
                data = parse_detail(url)
                print(data)
                save_to_mongo(data)


if __name__ == "__main__":
    main()
