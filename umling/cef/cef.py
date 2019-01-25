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
import os
import platform
import sys

from cefpython3 import cefpython as cef
from umling.api.graph import graph

Browser = None


def main() -> None:
    global Browser
    check_versions()

    graph.main()

    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    Browser = cef.CreateBrowserSync(url=get_static_folder(), window_title="umling")
    Browser.SetClientHandler(LoadHandler())
    bindings = cef.JavascriptBindings()
    bindings.SetFunction("py_process_message", py_process_message)
    Browser.SetJavascriptBindings(bindings)
    cef.MessageLoop()
    cef.Shutdown()


class LoadHandler(object):
    def OnLoadEnd(self, browser, **_):
        browser.ExecuteFunction("message", "Привет! Меня зовут umling")


def py_process_message(msg) -> None:
    global Browser
    Browser.ExecuteFunction("message", "hi " + msg)
    Browser.ExecuteFunction("picture", "graphs" + os.sep + "graph.png", "Title", "Desc")


def check_versions() -> None:
    ver = cef.GetVersion()
    print("[cef.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[cef.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[cef.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[cef.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


def get_static_folder() -> str:
    return os.getcwd() + os.sep + "static" + os.sep + "index.html"


if __name__ == '__main__':
    main()
