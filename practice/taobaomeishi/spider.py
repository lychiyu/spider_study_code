# coding: utf-8

"""
 Created by liuying on 2018/9/2.
"""
import re
from multiprocessing.pool import Pool
from time import sleep

import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pyquery import PyQuery as pq

from config import *

# 使用headless来启动chrome
option = webdriver.ChromeOptions()
option.add_argument('headless')

browser = webdriver.Chrome(chrome_options=option)

wait = WebDriverWait(browser, 10)

client = pymongo.MongoClient(MONGO_HOST, connect=False)
db = client[MONGO_DB]


def search(kw):
    browser.get('https://www.taobao.com/')
    try:
        # 输入框加载
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        # 搜索按钮可点击状态
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        # 输入action
        input.send_keys(kw)
        # 点击action
        submit.click()
        # 等待分页出来
        total_pages = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        get_data(kw)
        return total_pages.text
    except TimeoutException:
        return search(kw)


def next_page(page, kw):
    try:
        # 页码框
        page_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        # 跳转页面按钮
        page_submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        page_input.clear()
        page_input.send_keys(page)
        page_submit.click()
        current_page = wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page))
        )
        get_data(kw)
    except TimeoutException:
        return next_page(page)


def get_data(kw):
    # 确保商品信息全部加载出来了
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item"))
    )
    # 获取网页源码
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            'kw': kw,
            'image': item.find('.pic .img').attr('src'),
            'price': re.compile('.*?(\d+\.?\d+)', re.S).search(item.find('.price').text()).group(1),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
        }
        save_to_mongo(product)


def save_to_mongo(data):
    try:
        if db[MONGO_TABLE].insert(data):
            print('true', data)
            return True
    except Exception as e:
        print(f'save_to_mongo err: {e}')
        return False
    print('false')
    return False


def main(kw):
    total = search(kw)
    total = int(re.compile('(\d+)').search(total).group(1))
    for i in range(2, total + 1):
        print(f'page: {i}')
        next_page(i, kw)


if __name__ == '__main__':
    # main(KEYWORDS)
    kws = l5.split(' ')
    for kw in kws:
        print(f'{kw} start')
        main(kw)
        print(f'{kw} end')
    print("all end")

