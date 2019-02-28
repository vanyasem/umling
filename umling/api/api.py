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
This is the API (main logic) of umling.
"""

import random

from umling.api import sql
from umling.api import input
from umling.api import database


class Message:
    isFinal = False
    message = None
    shortcuts = None

    def __init__(self, is_final, message, shortcuts):
        self.isFinal = is_final
        self.message = message
        self.shortcuts = shortcuts


def state_to_message(state):
    response = random.choice(state.responses)
    return Message(False, response, state.shortcuts)


def handle_query(user_id, query):
    user = sql.get_user(user_id)
    if user is None:
        sql.create_user(user_id)
        user = sql.get_user(user_id)

    state = database.States[user.state]

    if state.requiresConfirmation:
        pass

    return state_to_message(state)
    pass


def init():
    sql.init()
    pass
