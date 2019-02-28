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
import re
import logging

from umling.api import sql
from umling.api import input
from umling.api import database
from umling.api import graph


class Message:
    isFinal = False
    message = None
    shortcuts = None

    def __init__(self, is_final, message, shortcuts):
        self.isFinal = is_final
        self.message = message
        self.shortcuts = shortcuts


def state_to_message(user_id, state, *args):
    db_state = database.States[state]
    response = random.choice(db_state.responses)
    if state == sql.STATE_GRAPH_DONE:
        final_graph = sql.get_current_graph(user_id)
        return Message(True, final_graph.name, [final_graph.description, ])
    else:
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


def check_done(query):
    normalized_query = input.process_input(query)
    for item in normalized_query:
        if item in database.Done:
            return True
    return False


def state_by_action(query, state):
    normalized_query = input.process_input(query)
    for item in normalized_query:
        if item in database.ActionActors:
            return sql.STATE_ACTORS
        elif item in database.ActionUseCases:
            return sql.STATE_USE_CASES
        elif item in database.ActionRelations:
            return sql.STATE_RELATIONS
    return state


def parse_list(query):
    delimiters = ';|,'
    return re.split(delimiters, query.strip())


def write_graph_data(user_id, query, state):
    data = parse_list(query)
    if state is sql.STATE_ACTORS:
        for actor in data:
            sql.make_actor(user_id, actor.strip(), "")  # TODO empty field
    elif state is sql.STATE_USE_CASES:
        for use_case in data:
            sql.make_use_case(user_id, use_case.strip(), "")  # TODO empty field
    elif state is sql.STATE_RELATIONS:
        for relation in data:
            rel = relation.strip().split('-')
            graph = sql.get_current_graph(user_id)
            actor = sql.get_actor_by_name(graph, rel[0].strip())
            use_case = sql.get_use_case_by_name(graph, rel[1].strip())
            if actor is None or use_case is None:
                return None
            sql.make_relation("", actor, use_case)  # TODO empty field


def get_graph_nodes(user_id):
    graph = sql.get_current_graph(user_id)
    actors = sql.get_actors(graph.get_id())
    use_cases = sql.get_use_cases(graph.get_id())
    return (', '.join([actor.name for actor in actors]), ', '.join([use_case.name for use_case in use_cases]))


def handle_state(user_id, state, query):
    logging.debug("{}, current state: {}".format(user_id, state))
    result = None
    if sql.get_user(user_id).confirmation:
        result = check_positive(str(query))

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
            state = sql.STATE_GRAPH_NAME
        elif result is False:
            state = sql.STATE_NAME
    elif state == sql.STATE_GRAPH_NAME:
        if query is not None:
            sql.set_query(user_id, query)
            state = sql.STATE_GRAPH_DESCRIPTION
    elif state == sql.STATE_GRAPH_DESCRIPTION:
        if query is not None:
            name = sql.get_user(user_id).query
            sql.make_graph(user_id, name, query)
            sql.set_query(user_id, "")  # TODO empty field
            state = sql.STATE_BASIC_SELECTION
    elif state == sql.STATE_BASIC_SELECTION:
        state = state_by_action(query, state)
    elif state == sql.STATE_ACTORS:
        if query is not None:
            if check_done(query) is True:
                state = sql.STATE_SELECTION
            else:
                write_graph_data(user_id, query, state)
    elif state == sql.STATE_USE_CASES:
        if query is not None:
            if check_done(query) is True:
                state = sql.STATE_SELECTION
            else:
                write_graph_data(user_id, query, state)
    elif state == sql.STATE_RELATIONS:
        args = get_graph_nodes(user_id)
        if query is not None:
            if check_done(query) is True:
                state = sql.STATE_SELECTION
            else:
                write_graph_data(user_id, query, state)  # TODO crashes here if a typo is made
        pass
    elif state == sql.STATE_SELECTION:
        if query is not None:
            if check_done(query) is True:
                state = sql.STATE_GRAPH_DONE
            else:
                state = state_by_action(query, state)
                if state is sql.STATE_RELATIONS:
                    args = get_graph_nodes(user_id)
    elif state == sql.STATE_GRAPH_DONE:
        graph.generate(user_id)
        #sql.set_state(user_id, sql.STATE_GRAPH_NAME) TODO not implemented

    db_state = database.States[state]
    if db_state.requiresConfirmation:
        logging.debug("{}, state {} requires confirmation".format(user_id, state))
        sql.set_confirmation(user_id, True)

    logging.debug("{}, switching state to: {}".format(user_id, state))
    sql.set_state(user_id, state)
    return state_to_message(user_id, state, *args)


def handle_query(user_id, query):
    logging.info("{}, got input: {}".format(user_id, query))
    user = get_or_create_user(user_id)
    return handle_state(user_id, user.state, query)


def init():
    sql.init()
    pass
