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

"""umling.

This is the main umling file. It will initialize, run and manage the whole of umling.
"""
import datetime
import getopt
import logging
import os
import sys

from umling import config
from umling.cef import cef
from umling.api import api


def print_help() -> None:
    print("""usage: umling.py [-h] [-t] [-w] [-c]

optional arguments:
  -h, --help            Show this help message and exit
  -t, --telegram        Start a Telegram bot
  -w, --web             Start a webserver at 127.0.0.1:8000
  -c, --cef             Default, launch the webapp in a Chromium sandbox""")
    pass


def cd_to_work_dir():
    sep = os.sep
    os.chdir(sep.join(os.path.realpath((sys.argv[0])).split(os.sep)[0:-1]))
    # os.path.split refuses to work with PyInstaller


def init_logging():
    if not os.path.exists(config.LOG_PATH):
        os.makedirs(config.LOG_PATH)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = config.LOG_PATH + timestamp + "." + config.LOG_LEVEL + '.log'
    logging.basicConfig(filename=path, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)


def main(argv) -> None:
    """Start the application."""
    try:
        opts, args = getopt.getopt(argv, "htwc", ["help", "telegram", "web", "cef"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    cd_to_work_dir()
    init_logging()
    api.init()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-t", "--telegram"):
            from umling.telegram import telegram
            telegram.init()
            sys.exit()
        elif opt in ("-w", "--web"):
            from umling.web import server
            server.init()
            sys.exit()

    cef.init()
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
