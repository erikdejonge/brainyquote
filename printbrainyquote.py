#!/usr/bin/env python3
# coding=utf-8
"""
fortunes
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from future import standard_library
import os
import sys
import pickle
import random

from argparse import ArgumentParser
from clint.textui.progress import mill
__all__ = ['main', 'get_random_fortune', 'make_fortune_data_file']
__url__ = 'http://software.clapper.org/fortune/'
__copyright__ = '2008-2011 Brian M. Clapper'
__author__ = 'Brian M. Clapper'
__email__ = 'bmc@clapper.org'
_PICKLE_PROTOCOL = 2

__version__ = '1.0'


def _read_fortunes(fortune_file):
    """ Yield fortunes as lists of lines """
    result = []
    start = None
    pos = 0

    for line in fortune_file:
        if line == "%\n":
            if pos != 0:  # "%" at top of file. Skip it.
                yield (start, pos - start, result)
                result = []
                start = None
        else:
            if start is None:
                start = pos

            result.append(line)

        pos += len(line)

    if result:
        yield (start, pos - start, result)


def get_random_fortune(fortune_file):
    """
    @type fortune_file: str, unicode
    @return: None
    """
    fortune_index_file = fortune_file + '.dat'

    if not os.path.exists(fortune_index_file):
        raise ValueError('Can\'t find file "%s"' % fortune_index_file)

    fortune_index = open(fortune_index_file, "rb")
    data = pickle.load(fortune_index)
    fortune_index.close()
    fortune_cookie = None

    for i in range(0, 5):
        try:
            random_record = random_int(0, len(data) - 1)
            (start, length) = data[random_record]
            f = open(fortune_file, 'rt')
            f.seek(start)
            fortune_cookie = f.read(length)
            f.close()
            break
        except UnicodeDecodeError as ude:
            if i > 3:
                print(i, ude)

    if fortune_cookie is None:
        return

    spaces = "   "
    content = fortune_cookie.strip().replace("\t", spaces)
    cnt = 0
    nc = spaces

    for c in content:
        nc += c
        cnt += 1

        if cnt > 80 and c == " ":
            nc += "\n" + spaces
            cnt = 0

    nc = nc.replace("\n" + spaces + "\n" + spaces + "--", "\n" + spaces + "--")

    if len(nc.split("--")) > 1:
        nc = spaces + nc.split("--")[0].strip() + "\n" + spaces + "-- " + nc.split("--")[1].replace("\n", "").replace(spaces, " ")

    for i in range(2, 6):
        sp = i * " "
        nc = nc.replace(sp, " ")

    ncs = nc.split("--")
    quote = nc
    author = ""

    if len(ncs) > 1:
        quote = ncs[0]
        author = "--" + ncs[1]

    return quote, author


def make_fortune_data_file(fortune_file, quiet=False):
    """
    @type fortune_file: str, unicode
    @type quiet: bool
    @return: None
    """
    fortune_index_file = fortune_file + '.dat'

    if not quiet:
        print('Updating "%s" from "%s"...' % (fortune_index_file, fortune_file))

    data = []
    shortest = sys.maxsize
    longest = 0

    for start, length, fortune in _read_fortunes(open(fortune_file, 'rt')):
        data += [(start, length)]
        shortest = min(shortest, length)
        longest = max(longest, length)

    fortune_index = open(fortune_index_file, 'wb')
    pickle.dump(data, fortune_index, _PICKLE_PROTOCOL)
    fortune_index.close()

    if not quiet:
        print('Processed %d fortunes.\nLongest: %d\nShortest %d' %
              (len(data), longest, shortest))


def random_int(start, end):
    """
    @type start: str, unicode
    @type end: str, unicode
    @return: None
    """
    return random.randint(start, end)


def search_fortune(searchquery, fortunefilep=None):
    """
    @type searchquery: str
    @type fortunefilep: str, None
    @return: None
    """
    results = {}

    for fortune_file in mill(os.listdir("."), label="- Searching quote files", every=4):
        if fortunefilep is not None:
            fortune_file = os.path.basename(fortunefilep) + ".dat"

        if fortune_file.endswith(".dat"):
            fortune_index_file = "./" + fortune_file

            if not os.path.exists(fortune_index_file):
                raise ValueError('Can\'t find file "%s"' % fortune_index_file)

            fortune_index = open(fortune_index_file, "rb")
            data = pickle.load(fortune_index)
            fortune_index.close()
            fortune_file = "./" + fortune_file
            f = open(fortune_file.replace(".dat", ""), 'rt')
            qwords = searchquery.split(" ")
            qwords = [w.lower() for w in qwords if w]
            for cnt in range(0, len(data) - 1):
                (start, length) = data[cnt]
                f.seek(start)
                fortune_cookie = f.read(length)
                spaces = "   "
                content = fortune_cookie.strip().replace("\t", spaces)
                cnt = 0
                nc = spaces

                for c in content:
                    nc += c
                    cnt += 1

                    if cnt > 80 and c == " ":
                        nc += "\n" + spaces
                        cnt = 0

                nc = nc.replace("\n" + spaces + "\n" + spaces + "--", "\n" + spaces + "--")

                if len(nc.split("--")) > 1:
                    nc = spaces + nc.split("--")[0].strip() + "\n" + spaces + "-- " + nc.split("--")[1].replace("\n", "").replace(spaces, " ")

                for i in range(2, 6):
                    sp = i * " "
                    nc = nc.replace(sp, " ")

                ncs = nc.split("--")
                quote = nc
                author = ""

                if len(ncs) > 1:
                    quote = ncs[0]
                    author = "--" + ncs[1]

                score = 0
                quotesplit = [x for x in quote.lower().split(" ") if x]
                for word in qwords:
                    if word in quotesplit:
                        score += 1

                for word in qwords:
                    if word in author.lower():
                        if score not in results:
                            results[score] = []

                        results[score].append((100, fortune_file.replace(".dat", ""), quote, author))
                    elif score > 0:
                        if score == len(quotesplit):
                            if score not in results:
                                results[score] = []

                            results[score].append((score, fortune_file.replace(".dat", ""), quote, author))

            f.close()

        if fortunefilep is not None:
            return results

    return results


def main():
    """
    Main program.
    """
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                            help="When updating the index file, don't emit "
                                 "messages.")

    arg_parser.add_argument('-u', '--update', action='store_true', dest='update',
                            help='Update the index file, instead of printing a '
                                 'fortune.')

    arg_parser.add_argument('-d', '--fortunefolder', dest='fortunefolder', help='Fortune basedir to use.')
    arg_parser.add_argument('-f', '--fortunefile', dest='fortunefile', help='Fortune file to use.')
    arg_parser.add_argument('-r', '--random', dest='random', help='Use random fortune file to use.', action="store_true")
    arg_parser.add_argument('-l', '--length', dest='length', help='Max length.', action="store")
    arg_parser.add_argument('-s', '--search', dest='search', help='Search a quote.', action="store")
    arg_parser.add_argument('-c', '--clean', dest='clean', help='No color', action="store_true")
    args = arg_parser.parse_args(sys.argv[1:])

    lf = []
    length = None

    try:
        if args.length is not None:
            length = int(args.length)
    except ValueError:
        pass

    if args.fortunefolder is None:
        print('no fortunefolder given')
        return

    os.chdir(os.path.expanduser(args.fortunefolder))

    if args.random is True:
        for fn in os.listdir(os.path.expanduser(args.fortunefolder)):
            if fn.endswith(".dat"):
                lf.append(fn.replace(".dat", ""))

    if len(lf) > 0:
        # lf = ['age', 'alone', 'amazing', 'anger', 'anniversary', 'architecture', 'art', 'attitude', 'beauty', 'best', 'birthday', 'brainy', 'business', 'car', 'change', 'christmas', 'communication', 'computers', 'cool', 'courage', 'dad', 'dating', 'death', 'design', 'diet', 'dreams', 'easter', 'education', 'environmental', 'equality', 'experience', 'failure', 'faith', 'family', 'famous', 'fathersday', 'fear', 'finance', 'fitness', 'food', 'forgiveness', 'freedom', 'friendship', 'funny',
        # 'future', 'gardening', 'god', 'good', 'government', 'graduation', 'great', 'happiness', 'health', 'history', 'home', 'hope', 'humor', 'imagination', 'inspirational', 'intelligence', 'jealousy', 'knowledge', 'law', 'leadership', 'learning', 'legal', 'life', 'love', 'marriage', 'medical', 'memorialday', 'men', 'mom', 'money', 'morning', 'mothersday', 'motivational', 'movies', 'movingon', 'music', 'nature', 'newyears', 'parenting', 'patience', 'patriotism', 'peace', 'pet', 'poetry',
        # 'politics', 'positive', 'power', 'relationship', 'religion', 'respect', 'romantic', 'sad', 'saintpatricksday', 'science', 'smile', 'society', 'sports', 'strength', 'success', 'sympathy', 'teacher', 'technology', 'teen', 'thankful', 'thanksgiving', 'time', 'travel', 'trust', 'truth', 'valentinesday', 'veteransday', 'war', 'wedding', 'wisdom', 'women', 'work']
        lf = ["future", "god", "money", "freedom", "health", "women", "friendship", "respect", "business", "success", "technology", "history", "humor"]
        fortune_file = lf[random.randint(0, len(lf) - 1)]
    else:
        fortune_file = args.fortunefile

    fortune_title = ""
    if fortune_file is not None or args.search:
        if fortune_file:
            fortune_title = fortune_file.capitalize()
            fortune_file = os.path.join(args.fortunefolder, fortune_file)

        quote = None
        author = ""

        if args.search is not None:
            if length is None:
                length = -1

            results = search_fortune(args.search, fortune_file)

            for index in results:
                for score, fortune_file, quote, author in results[index]:
                    if score > len(args.search.split(" ")) / 3:
                        quotelen = len(quote)
                        if quotelen < length or length == -1:
                            print("\033[96m" + fortune_file.replace("./quotes/", "").capitalize() + " (" + str(score) + "):\033[0m\n\033[34m" + quote + "\033[34m" + author, "\033[0m\n")

        elif args.update:
            make_fortune_data_file(fortune_file)
        else:
            if length is None:
                quote, author = get_random_fortune(fortune_file)
            else:
                quotelen = -1

                while (quotelen > length) or (quotelen < 0):
                    quote, author = get_random_fortune(fortune_file)
                    quotelen = len(quote)
            if quote is None:
                print("Error: no quote found.!")
            else:
                if args.clean:
                    for _ in range(0, 10):
                        #quote = quote.replace("\n", "")
                        quote = quote.replace("  ", " ")
                    quote = quote.replace("'", "")
                    print(author.replace("--", "").strip().replace("'", "\'") + ": " + quote.strip())
                else:
                    print("\033[96m" + fortune_title + ":\033[0m\n\033[34m" + quote + "\033[34m" + author, "\033[0m")
    else:
        print('no file given')


standard_library.install_aliases()

if __name__ == '__main__':
    main()
