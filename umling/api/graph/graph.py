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
import pydot


def main():
    import os
    os.environ["PATH"] += os.pathsep + 'C:\\Utils\\graphviz-2.38\\bin'

    # a DIrected GRAPH
    graph = pydot.Dot(graph_type='digraph')

    # creating nodes
    node_a = pydot.Node("test1", style="filled", fillcolor="red")
    # full reference here:
    # http://www.graphviz.org/doc/info/attrs.html
    # which in turn is part of the full docs in
    # http://www.graphviz.org/Documentation.php
    node_b = pydot.Node("test2", style="filled", fillcolor="green")
    node_c = pydot.Node("test3", style="filled", fillcolor="#0000ff")
    node_d = pydot.Node("test4", style="filled", fillcolor="#976856")

    # add the nodes to the graph
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    graph.add_node(node_d)

    # create the edges
    graph.add_edge(pydot.Edge(node_a, node_b))
    graph.add_edge(pydot.Edge(node_b, node_c))
    graph.add_edge(pydot.Edge(node_c, node_d))
    graph.add_edge(pydot.Edge(node_d, node_a, label="test5", labelfontcolor="#009933", fontsize="10.0", color="blue"))

    graph.write_png('static\\graphs\\graph.png', encoding='utf-8')
    pass


if __name__ == '__main__':
    main()
