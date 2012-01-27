#!/usr/bin/env python

import os
import sys
from distutils.core import setup

sys.path.append(os.path.realpath("src"))

setup(name = "pyhtmleditor",
        version = "0.0.1",
        description = "PyQt WYSIWYG HTML Editor",
        long_description = "Python port of QtWebKit htmleditor from the Graphics Dojo project on Qt Labs.",
        author = "Milan Nikolic",
        author_email = "gen2brain@gmail.com",
        license = "GNU GPLv3",
        url = "http://github.com/gen2brain/pyhtmleditor",
        packages = ["pyhtmleditor", "pyhtmleditor.ui"],
        package_dir = {"": "src"},
        scripts = ["pyhtmleditor"],
        requires = ["PyQt4"],
        platforms = ["Linux", "Windows", "OSX"]
        )
