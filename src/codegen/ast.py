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


class Node:
    '''Def of AST node'''

    def __init__(self, node_type: str = '', value=None, children: list = None):
        self.node_type = node_type
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []
