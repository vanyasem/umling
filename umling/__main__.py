#!/usr/bin/env python3

# Copyright (c) 2018 Ivan Semkin.
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

import sys

from PyQt5.QtWidgets import QApplication, QWidget


def main() -> None:
    """Start the application."""
    print("Hello World")
    app = QApplication(sys.argv)

    w = QWidget()
    w.setWindowTitle('Hi')
    w.show()
    sys.exit(app.exec_())
    pass


if __name__ == "__main__":
    main()
