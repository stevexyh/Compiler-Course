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


class NodeCnt(object):
    '''Super class of AST node, used for counting'''

    cnt = 0


class Node(NodeCnt):
    '''Def of AST node'''

    def __init__(self, node_type: str = '', value=None, children: list = None, depth: int = 0):
        self.node_type = node_type
        self.depth = depth
        self.value = value
        self.children = children if children else []
        self.idx = self.cnt
        NodeCnt.cnt += 1

    def __str__(self):
        res = f'Type : {self.node_type}\n'
        res += f'Value: {self.value}\n' if self.value else ''
        res += f'id   : {self.idx}'

        return str(res)

    def print_tree(self):
        '''Output tree in string'''

        def print_node(self):
            indent = '    '
            res = '\n' + indent*self.depth + 'Type: ['+str(self.node_type)+']{'
            if self.children:
                for child in self.children:
                    if child:
                        res += print_node(child)
                    else:
                        res += '\n'+indent * (self.depth+1) + 'empty'
            else:
                res += '\n' + indent*(self.depth+1) + 'Value: '+str(self.value)
                res += '\n' + indent*(self.depth+1) + 'Depth: '+str(self.depth)

            res += '\n' + indent * self.depth + '}'

            return res

        def traverse_depth(self, depth: int = 0):
            self.depth = depth
            for i in range(len(self.children)):
                if self.children[i]:
                    traverse_depth(self.children[i], depth=self.depth+1)

        traverse_depth(self)
        res = print_node(self)

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
