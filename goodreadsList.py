# Function: crawl the basic information of the books from the list of goodreads
# Input: id number and name of a list, e.g 1.Best_Books_Ever
# Output: a csv file or csv files (by list web pages) containing
# Output: book title, author, ave_rate, rate numbers, and cover(base64).
# Author: Renqing Luo
# Date: 2022/6/14
# Statue: Incomplete

import os
import re
import base64
import random
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


class BookList(object):
    def __init__(self) -> object:
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.66 Safari/537.36 '
        }
        self.url = 'https://www.goodreads.com/list/show/'
        self.book_name = []  # title and author
        self.book_cover = [] # 
        self.book_ave_rate = []
        self.book_rate_nums = []
        self.soup = None

    def get_soup(self):
        print(self.url)
        response = requests.get(self.url, headers=self.headers)
        html = response.content.decode('utf-8')
        self.soup = BeautifulSoup(html, 'lxml')

    def get_name(self):
        names = self.soup.find_all('span', itemprop="name")
        for name in names:
            self.book_name.append(name.string)

    def get_cover(self):
        covers = self.soup.find_all('img', {"class": "bookCover"})
        for img in covers:
            src = img.get('src')
            cover_img = requests.get(src, headers=self.headers).content
            cover_base = base64.b64encode(cover_img) # img to string
            self.book_cover.append(cover_base)
            print(img.get('alt'))
            time.sleep(random.random())

    def get_rate(self):
        rates = self.soup.find_all('span', {"class": "minirating"})
        for rate in rates:
            rate_info = re.findall(r"\d+\.?\d*", rate.text) # record digits only
            self.book_ave_rate.append(rate_info[0])
            self.book_rate_nums.append(rate_info[1])

    def get_info(self):
        self.get_soup()
        self.get_name()
        self.get_cover()
        self.get_rate()

    def get_total_page(self):
        return int(self.soup.select('.pagination a')[-2].string)

    def save_info(self, list_name, page):
        os.makedirs(list_name, exist_ok=True)
        title = self.book_name[::2]
        author = self.book_name[1::2]
        book_dict = {'Title': title, 'Author': author, 'Cover': self.book_cover,
                     'Average Rate': self.book_ave_rate, 'Rates': self.book_rate_nums}
        books = pd.DataFrame(book_dict)
        path = os.path.join(list_name, str(page) + '.csv')
        books.to_csv(path, index=False)

    def init_info(self):
        self.book_name = []
        self.book_cover = []
        self.book_ave_rate = []
        self.book_rate_nums = []

    def init_record(self):
        list_name = input('Listopia: ')
        self.url += list_name
        ori_url = self.url
        self.get_info()
        pages = self.get_total_page()
        return ori_url, pages, list_name

    def record_all_in_one(self):
        ori_url, pages, list_name = self.init_record()
        for page in range(2, pages + 1):
            self.url = ori_url + '?page=' + str(page)
            self.get_info()
        self.save_info(list_name, list_name)

    def record_by_page(self):
        ori_url, pages, list_name = self.init_record()
        self.save_info(list_name, 1)
        for page in range(2, pages + 1):
            self.init_info()
            self.url = ori_url + '?page=' + str(page)
            self.get_info()
            self.save_info(list_name, page)


if __name__ == '__main__':
    book_list = BookList()
    #book_list.record_by_page()
    book_list.record_all_in_one()
