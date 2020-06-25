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


import uuid
from graphviz import Digraph


class Node:
    '''Def of AST node'''

    def __init__(self, node_type: str = '', value=None, children: list = None, depth: int = 0):
        self.node_type = node_type
        self.depth = depth
        self.value = value
        self.children = children if children else []
        self.dot = Digraph(comment='ASTree')

    def __str__(self):
        def print_tree(self):
            indent = '    '
            res = '\n' + indent*self.depth + 'Type: ['+str(self.node_type)+']{'
            if self.children:
                for child in self.children:
                    if child:
                        res += print_tree(child)
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
        res = print_tree(self)

        return res

    # def print_tree(self, save_path='./Binary_Tree.gv', label=False):
    def graphviz(self, label=False):
        '''Visualize tree by Graphviz'''

        # colors for labels of nodes
        # colors = ['skyblue', 'tomato', 'orange',
        #           'purple', 'green', 'yellow', 'pink', 'red']

        # 绘制以某个节点为根节点的二叉树
        def print_node(node, node_tag):
            # 节点颜色
            # color = sample(colors, 1)[0]

            for i in range(len(node.children)):
                if node.children[i]:
                    child_tag = str(uuid.uuid1())
                    self.dot.node(
                        child_tag,
                        str(node.children[i].data),
                        style='filled',
                        # color=color
                    )

                    # 子节点与其父节点的连线, 是否在连接线上写上标签
                    label_string = 'child' if label else ''
                    self.dot.edge(node_tag, child_tag, label=label_string)

                    print_node(node.children[i], child_tag)

        # 如果树非空
        if self.value is not None:
            root_tag = str(uuid.uuid1())                # 根节点标签
            self.dot.node(
                root_tag,
                str(self.value),
                style='filled',
                # color=sample(colors, 1)[0]
            )     # 创建根节点
            print_node(self, root_tag)

        self.dot.render()                              # 保存文件为指定文件
