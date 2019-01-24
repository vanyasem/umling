#!/usr/bin/env python3

# Copyright (c) 2019 Ivan Semkin.
#
# This file is part of umling
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
This is the CEF (embedded browser) component of umling.
"""

import platform
import sys
import threading

from cefpython3 import cefpython as cef

from umling.web import server


def main():
    check_versions()

    thread = threading.Thread(target=server.main, args=())
    thread.daemon = True
    thread.start()

    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url="http://localhost:8000/",
                          window_title="umling")
    cef.MessageLoop()
    cef.Shutdown()


def check_versions():
    ver = cef.GetVersion()
    print("[cef.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[cef.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[cef.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[cef.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


if __name__ == '__main__':
    main()
