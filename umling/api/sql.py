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
import os

from peewee import *
from umling import config

db = SqliteDatabase(config.DATA_PATH + 'umling.db')


class User(Model):
    user_id = CharField()

    class Meta:
        database = db


class Data(Model):
    actors = []
    use_cases = []

    class Meta:
        database = db


def save_user(user_id):
    test_user = User(user_id=user_id)
    test_user.save()


def init():
    if not os.path.exists(config.DATA_PATH):
        os.makedirs(config.DATA_PATH)

    db.connect()
    db.create_tables([User])

    save_user("cef2")
    save_user("cef3")

