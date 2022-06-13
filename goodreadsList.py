# Function: crawl the basic information of the books from the list of goodreads
# Input: id number and name of a list, e.g 1.Best_Books_Ever
# Output: csv file containing book title, author, and cover(base64).
# Author: Renqing Luo
# Date: 2022/6/11
# Statue: Complete

import base64
import random
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


class Book(object):
    def __init__(self) -> object:
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.66 Safari/537.36 '
        }
        self.url = 'https://www.goodreads.com/list/show/'
        self.book_info = []  # title and author
        self.book_cover = []

    def get_soup(self):
        print(self.url)
        response = requests.get(self.url, headers=self.headers)
        html = response.content.decode('utf-8')
        return BeautifulSoup(html, 'lxml')

    def get_info(self, soup):
        names = soup.find_all('span', itemprop="name")
        for name in names:
            self.book_info.append(name.string)
        covers = soup.find_all('img', {"class": "bookCover"})
        for img in covers:
            src = img.get('src')
            cover_img = requests.get(src, headers=self.headers).content
            cover_base = base64.b64encode(cover_img)
            self.book_cover.append(cover_base)
            print(img.get('alt'))
            time.sleep(random.random())

    def save_info(self, list_name):
        title = self.book_info[::2]
        author = self.book_info[1::2]
        Book_dict = {'Title': title, 'Author': author, 'Cover': self.book_cover}
        books = pd.DataFrame(Book_dict)
        books.to_csv(list_name + '.csv', index=False)

    def main(self):
        list_name = input('Listopia: ')
        self.url += list_name
        ori_url = self.url
        soup = self.get_soup()
        pages = int(soup.select('.pagination a')[-2].string)
        self.get_info(soup)
        for page in range(2, pages + 1):
            self.url = ori_url + '?page=' + str(page)
            self.get_info(self.get_soup())
        self.save_info(list_name)


if __name__ == '__main__':
    book = Book()
    book.main()
