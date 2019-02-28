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
import logging

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


def state_to_message(state, *args):
    db_state = database.States[state]
    response = random.choice(db_state.responses)
    return Message(False, response.format(*args), db_state.shortcuts)


def get_or_create_user(user_id):
    user = sql.get_user(user_id)
    if user is None:
        sql.create_user(user_id)
        user = sql.get_user(user_id)
    return user


def check_positive(query):
    normalized_query = input.process_input(query)
    for item in normalized_query:
        if item in database.Positives:
            return True
        elif item in database.Negatives:
            return False
    return None


def state_by_action(query, state):
    normalized_query = input.process_input(query)
    for item in normalized_query:
        if item in database.ActionActors:
            return sql.STATE_ACTORS
        elif item in database.ActionUseCases:
            return sql.STATE_USE_CASES
    return state


def load_query_if_saved(user_id, query):
    if sql.get_user(user_id).query is not None \
            and query is None:
        return sql.get_user(user_id).query
    return query


def handle_state(user_id, state, query):
    logging.debug("{}, current state: {}".format(user_id, state))
    result = None
    if sql.get_user(user_id).confirmation:
        result = check_positive(str(query))
        pass

    args = ()
    if state == sql.STATE_GREETING:
        if result is True:
            sql.set_confirmation(user_id, False)
            state = sql.STATE_NAME
    elif state == sql.STATE_NAME:
        if query is not None:
            sql.set_name(user_id, query)
        state = sql.STATE_CONFIRM_NAME
        args = (sql.get_user(user_id).username, )
    elif state == sql.STATE_CONFIRM_NAME:
        args = (sql.get_user(user_id).username, )
        if result is True:
            sql.set_confirmation(user_id, False)
            state = sql.STATE_BASIC_SELECTION
        elif result is False:
            state = sql.STATE_NAME
    elif state == sql.STATE_BASIC_SELECTION:
        args = (sql.get_user(user_id).username, )
        query = load_query_if_saved(user_id, query)
        if sql.get_user(user_id).save_query is True:
            sql.set_query(user_id, query)
            state = state_by_action(query, state)
        else:
            sql.set_save_query(user_id, True)
    elif state == sql.STATE_ACTORS:
        pass
    elif state == sql.STATE_USE_CASES:
        pass

    db_state = database.States[state]
    if db_state.requiresConfirmation:
        logging.debug("{}, state {} requires confirmation".format(user_id, state))
        sql.set_confirmation(user_id, True)

    logging.debug("{}, switching state to: {}".format(user_id, state))
    sql.set_state(user_id, state)
    return state_to_message(state, *args)


def handle_query(user_id, query):
    logging.info("{}, got input: {}".format(user_id, query))
    user = get_or_create_user(user_id)
    return handle_state(user_id, user.state, query)


def init():
    sql.init()
    pass
