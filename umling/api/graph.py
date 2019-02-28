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
This is the graph generation logic of umling.
"""
import os

import pydot

from umling.api import sql


def determine_color(level):
    if level == sql.LEVEL_ACTOR:
        return "red"
    elif level == sql.LEVEL_USE_CASE:
        return "blue"

def main():
    os.environ["PATH"] += os.pathsep + os.getcwd() + os.sep + 'graphviz' + os.sep + 'bin'

    # a DIrected GRAPH
    pydot_graph = pydot.Dot(graph_type='digraph')

    graph = sql.get_current_graph(user_id)
    nodes = sql.get_graph_nodes(graph.get_id())
    pydot_nodes = {}
    for node in nodes:
        pydot_node = pydot.Node(node.name, style="filled", fillcolor=determine_color(node.level))
        pydot_nodes[node.get_id()] = pydot_node
        pydot_graph.add_node(pydot_node)

    # full reference here:
    # http://www.graphviz.org/doc/info/attrs.html
    # which in turn is part of the full docs in
    # http://www.graphviz.org/Documentation.php

    relations = sql.get_relations(graph.get_id())
    for relation in relations:
        start_node = pydot_nodes[relation.start_node.get_id()]
        end_node = pydot_nodes[relation.end_node.get_id()]
        pydot_graph.add_edge(pydot.Edge(start_node, end_node, label=relation.name))
    # pydot_graph.add_edge(pydot.Edge(node_d, node_a, label="test5", labelfontcolor="#009933", fontsize="10.0", color="blue"))

    if not os.path.exists('static' + os.sep + 'graphs'):
        os.makedirs('static' + os.sep + 'graphs')
    pydot_graph.write_png('static' + os.sep + 'graphs' + os.sep + str(graph.get_id()) + '.png', encoding='utf-8')
    pass
