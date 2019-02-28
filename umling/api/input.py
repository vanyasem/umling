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
This is the input processing component of umling.
"""

import re

import pymorphy2

Morph = pymorphy2.MorphAnalyzer()


# Преобразует предложение в список нормализованных тэгов
def process_input(query, normalize=True):
    if type(query) is list:
        array = query
    elif type(query) is str:
        array = re.split(' ', query)
    else:
        raise TypeError

    tags = []
    for tag in array:
        # Каждое слово приводится к начальной форме
        result = normalize_str(tag, normalize)
        tags.append(result)
    return tags


# Приводит слово к начальной форме ("Нормализует")
def normalize_str(string, normalize):
    if normalize:
        input = re.sub(r'([^\s\w]|_)+', '', string.lower())
        result = Morph.parse(input)[0].normal_form
    else:
        result = string
    return result
