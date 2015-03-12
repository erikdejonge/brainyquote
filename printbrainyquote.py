# coding=utf-8
# $Id: f95776c6a6fa8a2b954005004fce99819efdee4f $
"""
fortunes
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import os
import sys
import random
import pickle as pickle

# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------
__all__ = ['main', 'get_random_fortune', 'make_fortune_data_file']

# Info about the module
__version__ = '1.0'
__author__ = 'Brian M. Clapper'
__email__ = 'bmc@clapper.org'
__url__ = 'http://software.clapper.org/fortune/'
__copyright__ = '2008-2011 Brian M. Clapper'
__license__ = 'BSD-style license'

# ---------------------------------------------------------------------------
# Internal Constants
# ---------------------------------------------------------------------------
_PICKLE_PROTOCOL = 2

# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------


def random_int(start, end):
    """
    @type start: str, unicode
    @type end: str, unicode
    @return: None
    """
    return random.randint(start, end)


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
    random_record = random_int(0, len(data) - 1)
    (start, length) = data[random_record]
    f = open(fortune_file, 'rt')
    f.seek(start)
    fortune_cookie = f.read(length)
    f.close()
    spaces = "   "
    content = fortune_cookie.strip().replace("\t", spaces)
    cnt = 0
    nc = spaces

    for c in content:
        nc += c
        cnt += 1

        if cnt > 70 and c == " ":
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
        author = "--"+ncs[1]
    return quote, author


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


def main():
    """
    Main program.
    """
    from argparse import ArgumentParser
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
    args = arg_parser.parse_args(sys.argv[1:])
    lf = []

    if args.fortunefolder is None:
        print('no fortunefolder given')
        return

    if args.random is True:
        for fn in os.listdir(args.fortunefolder):
            if fn.endswith(".dat"):
                lf.append(fn.replace(".dat", ""))

    if len(lf) > 0:
        fortune_file = lf[random.randint(0, len(lf) - 1)]
    else:
        fortune_file = args.fortunefile

    if fortune_file is not None:
        fortune_title = fortune_file.capitalize()
        fortune_file = os.path.join(args.fortunefolder, fortune_file)

        if args.update:
            make_fortune_data_file(fortune_file)
        else:
            quote, author = get_random_fortune(fortune_file)
            print("\033[94m"+fortune_title + ":\n\033[96m" + quote+"\033[95m"+author,"\033[0m")
    else:
        print('no file given')


if __name__ == '__main__':
    main()
