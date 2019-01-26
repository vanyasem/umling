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
LEVEL_ACTOR = 0
LEVEL_USE_CASE = 1


class UmlingModel(Model):
    class Meta:
        database = db


class User(UmlingModel):
    user_id = CharField()


class Graph(UmlingModel):
    user = ForeignKeyField(User, backref='graphs')
    name = CharField()
    description = CharField()


class Node(UmlingModel):
    graph = ForeignKeyField(Graph, backref='nodes')
    level = SmallIntegerField()
    name = CharField()
    description = CharField()


class Relationship(UmlingModel):
    start_node = ForeignKeyField(Node, backref='relationships')
    end_node = ForeignKeyField(Node, backref='relationships')
    name = CharField()  # TODO Probably worth converting to SmallIntegerField, as this will enum include / extend
    direction = BooleanField()


def populate_test_data():
    test_user = User(user_id="Test user")
    test_user.save()

    test_graph = Graph(user=test_user, name="Test graph", description="This graph is intended for testing")
    test_graph.save()

    test_node1 = Node(graph=test_graph, level=LEVEL_ACTOR, name="Test node 1", description="First node intended for testing")
    test_node1.save()

    test_node2 = Node(graph=test_graph, level=LEVEL_USE_CASE, name="Test node 2", description="Second node intended for testing")
    test_node2.save()

    test_relationship = Relationship(start_node=test_node1, end_node=test_node2, name="Test relationship", direction=False)
    test_relationship.save()


def init():
    if not os.path.exists(config.DATA_PATH):
        os.makedirs(config.DATA_PATH)

    db.connect()
    db.create_tables([User, Graph, Node, Relationship])
