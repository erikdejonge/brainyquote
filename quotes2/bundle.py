from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()
import os


def ab(s):
    s2 = ""
    t = tuple(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

    for i in s:
        if i in t:
            s2 += i
    return s2


current = ""
currentfp = None
for f in os.listdir("."):
    if f.endswith("txt"):
        fpn = f.split(".")[0].replace("topic_", "")
        abfpn = ab(fpn)
        if abfpn != current:
            print(abfpn)
            current = abfpn
            currentfp = open(abfpn, "wt")
        if currentfp is not None:
            c = open(f, "rt").read()
            currentfp.write(c)
