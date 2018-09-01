# coding: utf-8

"""
 Created by liuying on 2018/9/1.
"""
import json
import re
import requests
from multiprocessing import Pool
from requests.exceptions import RequestException


def get_one_page(url):
    """
    抓取一页数据
    :param url:
    :return:
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    }
    try:
        res = requests.get(url, headers=headers)
    except RequestException:
        return None
    if res.status_code == requests.codes.ok:
        return res.text


def parse_one_page(html):
    """
    解析网页数据
    :param html:
    :return:
    """

    """
    <dd>
        <i class="board-index board-index-1">1</i>
        <a href="/films/1203" title="霸王别姬" class="image-link" data-act="boarditem-click" data-val="{movieId:1203}">
          <img src="//ms0.meituan.net/mywww/image/loading_2.e3d934bf.png" alt="" class="poster-default" />
          <img data-src="http://p1.meituan.net/movie/20803f59291c47e1e116c11963ce019e68711.jpg@160w_220h_1e_1c" alt="霸王别姬" class="board-img" />
        </a>
        <div class="board-item-main">
          <div class="board-item-content">
                  <div class="movie-item-info">
            <p class="name"><a href="/films/1203" title="霸王别姬" data-act="boarditem-click" data-val="{movieId:1203}">霸王别姬</a></p>
            <p class="star">
                    主演：张国荣,张丰毅,巩俐
            </p>
        <p class="releasetime">上映时间：1993-01-01(中国香港)</p>    </div>
        <div class="movie-item-number score-num">
        <p class="score"><i class="integer">9.</i><i class="fraction">6</i></p>
        </div>

          </div>
        </div>
    </dd>
    """
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)"'
                         '.*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">'
                         '(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',
                         re.S)
    result = re.findall(pattern, html)
    for item in result:
        yield {
            'index': item[0],
            'img': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    """
    写入文件
    :param content:
    :return:
    """
    with open('top100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])
