# coding=utf-8
"""
-
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import int
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range

import os
import requests
import time
from urllib import parse
from lxml import html

import concurrent.futures


def fetch_quotes(url):
    """
    @type url: str, unicode
    @return: None
    """
    page = requests.get(url)

    # print(page.url)
    title = str(os.path.basename(parse.urlparse(url).path).split('.html')[0])
    tree = html.fromstring(page.text)
    f = open(os.path.join("quotes", title + ".txt"), "tw+")
    f.write("%\n")
    allquotes = ""
    cnt = 0
    for quotes in tree.xpath('//div[@id="quotesList"]//span[@class="bqQuoteLink"]/a/text()'):
        cnt += 1
        f.write(quotes + "\n")
        cnt2 = 0
        for author in tree.xpath('//div[@id="quotesList"]//div[@class="bq-aut"]/a/text()'):
            cnt2 += 1

            if cnt == cnt2:
                f.write("\t\t--" + author + "\n%\n")

    # f.seek(0)
    # print(f.read())
    f.close()


def fetch_links(topic):
    """
    @type topic: str, unicode
    @return: None
    """
    url = "http://brainyquote.com" + topic
    page = requests.get(url)
    print(page.url)
    tree = html.fromstring(page.text)
    end = tree.xpath('/html/body/div[4]/div/div/div[1]/div[2]/div/ul[2]/li[1]/div/ul/li[last()-1]/a/text()')

    # print end[0],"\n"
    for link in range(1, int(end[0]) + 1):
        if link == 1:
            fetch_quotes(url)
        else:
            blink = url.split('.html')
            fetch_quotes(url.replace(url, "%s%s.html" % (blink[0], link)))


def get_topics():
    """
    get_topics
    """
    page = requests.get('http://www.brainyquote.com/quotes/topics.html')
    tree = html.fromstring(page.text)
    topics = tree.xpath('//div[@class="bqLn"]/div[@class="bqLn"]/a/@href')

    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        executor.map(fetch_links, topics)


if __name__ == '__main__':
    get_topics()
