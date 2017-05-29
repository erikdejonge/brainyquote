
# coding=utf-8
"""
Quote of the day from https://www.goodreads.com/quotes_of_the_day
Usage:
  goodreads_qotd.py [options] <quotefile>

Options:
  -h --help     Show this screen.
  -u --url      Show origin

author  : rabshakeh (erik@a8.nl)
project : quotes
created : 05 Jun 2016 / 20:57
where   : Latitude: 51.825439
          longitude: 4.650873
          https://www.google.nl/maps/place/51.825439,4.650873
"""
import consoleprinter
import os
import requests
import sys

from arguments import Arguments
from bs4 import BeautifulSoup
from consoleprinter import console

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
        self.quotefile = ""
        super().__init__(doc)


def addprint(buf, news):
    """
    @type buf: str
    @type news: list
    @return: None
    """
    buf += news
    buf += "\n"
    return buf


def main():
    """
    main
    """
    arguments = IArguments(__doc__)

    # console(arguments)
    baseurl = "https://www.goodreads.com"
    url = baseurl + "/quotes_of_the_day"


    #if os.path.exists("r.txt"):
    #    rtext = open("r.txt").read()
    #else:
        # print("downloading")
    r = requests.get(url)

    #open("r.txt", "w").write(r.text)
    rtext = r.text

    soup = BeautifulSoup(rtext, 'html.parser')
    allhtml = soup.find_all(class_="quoteText")[0]

    # scripts = allhtml.find_all("script")[0]
    rtext = str(allhtml).split("</span>")[0]
    soup = BeautifulSoup(rtext, 'html.parser')
    colors = ["33", "91", "94"]
    indexc = 0
    quotestring = ""

    for i in str(soup.getText().strip().replace('    ―', '')).strip().split("\n"):
        if len(i.strip()) > 0:
            if indexc == 0:
                content = i.replace("\n\n", "\n").replace(".", ".\n")
                content = content.strip().replace("\n\n", "\n")

                for c in content.split("\n"):
                    if len(c) > 0:
                        for i in range(0, 5):
                            c = c.replace("\n.", ".")

                        quotestring = addprint(quotestring, "\033[" + colors[indexc] + "m" + consoleprinter.remove_escapecodes(c.strip()).strip() + "\033[0m")
            else:
                quotestring = addprint(quotestring, "\033[" + colors[indexc] + "m" + consoleprinter.remove_escapecodes(i.strip().replace("\n\n", "\n")).strip() + "\033[" + colors[indexc] + "m")

            indexc += 1
            if indexc > 2:
                indexc = 0

    if arguments.url:
        for i in soup.find_all("a"):
            quotestring = addprint(quotestring, "\033[37m  " + baseurl + i.get('href') + "\033[0m")

    quotestring = quotestring.strip()
    print(quotestring)
    quotestring = quotestring.replace("\n\x1b[33m”", "\x1b[33m”\n")
    if len(quotestring) > 0:
        open(arguments.quotefile, "w").write(quotestring)


if __name__ == "__main__":
    main()
