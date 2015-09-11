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
    os.system("rm quotes/*.dat")
    for i in os.listdir("quotes"):
        if not os.path.isdir("quotes/"+i) and not i.endswith(".py"):
            print(i)
            os.system("python3 ~/workspace/brainyquote/printbrainyquote.py -d ~/workspace/brainyquote/quotes -u -f "+i)


if __name__ == "__main__":
    main()
