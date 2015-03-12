# coding=utf-8
"""
brainyquotesdownloader
-
Active8 (11-03-15)
author: erik@a8.nl 
license: GNU-GPL2
"""

import os
def main():
    """
    main
    """
    for i in os.listdir("quotes"):
        print(i)
        os.system("python3 printbrainyquote.py -u -f "+i)


if __name__ == "__main__":
    main()
    