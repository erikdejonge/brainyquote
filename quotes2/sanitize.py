from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library
standard_library.install_aliases()
import os
for f in os.listdir("."):
    if not os.path.isdir(f):
        c = open(f, "rt").read()
        c = c.replace("%\n%", "%").replace("	--", "	--")
        open(f, "wt").write(c)
        print(f)

