#!/usr/bin/env python3
# coding=utf-8
"""
Quote of the day from https://www.goodreads.com/quotes_of_the_day

Usage:
  goodreads_qotd.py

Options:
  -h --help     Show this screen.

author  : rabshakeh (erik@a8.nl)
project : quotes
created : 05 Jun 2016 / 20:57
where   : Latitude: 51.825439
          longitude: 4.650873
          https://www.google.nl/maps/place/51.825439,4.650873
"""
import os
import sys
import requests
from arguments import Arguments
from consoleprinter import console
from bs4 import BeautifulSoup


if sys.version_info.major < 3:
    console("Python 3 is required", color="red", plaintext="True")
    exit(1)


class IArguments(Arguments):
    """
    IArguments
    """

    def __init__(self, doc):
        """
        __init__
        """
        self.help = False
        self.input = ""
        super().__init__(doc)


def main():
    """
    main
    """
    #arguments = IArguments(__doc__)
    #console(arguments)
    baseurl = "https://www.goodreads.com"
    url = baseurl + "/quotes_of_the_day"
    if os.path.exists("r.txt"):
        rtext = open("r.txt").read()
    else:
        #print("downloading")
        r = requests.get(url)
        #open("r.txt", "w").write(r.text)
        rtext = r.text
    soup = BeautifulSoup(rtext, 'html.parser')
    allhtml = soup.find_all(class_="quoteText")[0]
    scripts = allhtml.find_all("script")[0]
    rtext = str(allhtml).split("</span>")[0]
    soup = BeautifulSoup(rtext, 'html.parser')
    colors = ["33", "91", "94"]
    indexc = 0
    for i in str(soup.getText().strip().replace('    ―', '')+"\n").split("\n"):
        print("\033["+colors[indexc]+"m{}\033[0m".format(i))
        indexc += 1
        if indexc > 2:
            indexc = 0


    for i in soup.find_all("a"):
        print("\033[37m{}\033[0m".format(baseurl+i.get('href')))



if __name__ == "__main__":
    main()
