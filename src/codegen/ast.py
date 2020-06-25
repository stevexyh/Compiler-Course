#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---------------------------------------------
* Project Name : Compiler-Course
* File Name    : ast.py
* Description  : Class def for AST node
* Create Time  : 2020-06-24 18:38:03
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
---------------------------------------------
* Notice
-
-
---------------------------------------------
'''


import pygraphviz as pgv


class NodeCnt():
    '''Super class of AST node, used for counting'''

    cnt = 0


class Node(NodeCnt):
    '''Def of AST node'''

    def __init__(self, node_type: str = '', value=None, name='', children: list = None):
        self.node_type = node_type
        self.value = value
        self.name = name
        self.children = children if children else []
        self.idx = self.cnt
        NodeCnt.cnt += 1

    def __str__(self):
        res = f'id   : {self.idx}\n'
        res += f'Type : {self.node_type}\n'
        res += f'Name: {self.name}\n' if self.name else ''

        if isinstance(self.value, list):
            value = [i.name for i in self.value]
        else:
            value = str(self.value)
        res += f'Value: {value}\n' if self.value else ''

        return str(res)

    def print_tree(self, depth: int = 0):
        '''Output tree in string'''

        indent = '    '
        res = '\n' + indent*depth + 'Type: ['+str(self.node_type) + ']{'
        if self.children:
            for child in self.children:
                if child:
                    res += child.print_tree(depth=depth+1)
                else:
                    res += '\n'+indent * (depth+1) + 'empty'
        else:
            res += '\n' + indent*(depth+1) + 'Value: ' + str(self.value)
            res += '\n' + indent*(depth+1) + 'Depth: ' + str(depth)

        res += '\n' + indent * depth + '}'

        return res


def draw_graph(root: Node):
    '''Visualize tree by Graphviz'''

    tree = pgv.AGraph(strict=True, directed=False, name='AST')

    def print_node(node: Node):
        for i in range(len(node.children)):
            if node.children[i]:
                tree.add_edge(node, node.children[i])
                print_node(node.children[i])

    print_node(root)
    print(tree.string())

    tree.layout(prog='dot')
    tree.draw(path='graph/AST.pdf', format='pdf')
    tree.draw(path='graph/AST.png', format='png')
