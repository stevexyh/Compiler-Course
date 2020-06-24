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

from graphviz import Digraph


# TODO(Steve X): 输出AST
class Node:
    '''Def of AST node'''

    def __init__(self, node_type: str = '', children: list = None):
        self.node_type = node_type
        self.children = children if children else []
        self.dot = Digraph(comment='ASTree')

    def __str__(self):
        res = 'Type: [' + str(self.node_type) + ']{\n'
        # res += ''.join(['\tchild: ' + str(child) + '\n' for child in self.children])
        for child in self.children:
            res += '\tchild: ' + str(child) + '\n\t'

        res += '\n}'
        return res

    # # 利用Graphviz实现二叉树的可视化
    # def print_tree(self, save_path='./Binary_Tree.gv', label=False):

    #     # colors for labels of nodes
    #     colors = ['skyblue', 'tomato', 'orange',
    #               'purple', 'green', 'yellow', 'pink', 'red']

    #     # 绘制以某个节点为根节点的二叉树
    #     def print_node(node, node_tag):
    #         # 节点颜色
    #         color = sample(colors, 1)[0]
    #         if node.left is not None:
    #             left_tag = str(uuid.uuid1())            # 左节点的数据
    #             self.dot.node(left_tag, str(node.left.data),
    #                           style='filled', color=color)    # 左节点
    #             label_string = 'L' if label else ''    # 是否在连接线上写上标签，表明为左子树
    #             self.dot.edge(node_tag, left_tag,
    #                           label=label_string)   # 左节点与其父节点的连线
    #             print_node(node.left, left_tag)

    #         if node.right is not None:
    #             right_tag = str(uuid.uuid1())
    #             self.dot.node(right_tag, str(node.right.data),
    #                           style='filled', color=color)
    #             label_string = 'R' if label else ''  # 是否在连接线上写上标签，表明为右子树
    #             self.dot.edge(node_tag, right_tag, label=label_string)
    #             print_node(node.right, right_tag)

    #     # 如果树非空
    #     if self.data is not None:
    #         root_tag = str(uuid.uuid1())                # 根节点标签
    #         self.dot.node(root_tag, str(self.data), style='filled',
    #                       color=sample(colors, 1)[0])     # 创建根节点
    #         print_node(self, root_tag)

    #     self.dot.render(save_path)                              # 保存文件为指定文件
