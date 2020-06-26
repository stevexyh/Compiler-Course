#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---------------------------------------------
* Project Name : Compiler-Course
* File Name    : table.py
* Description  : Class def for general tables
* Create Time  : 2020-06-25 23:48:54
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
---------------------------------------------
* Notice
-
-
---------------------------------------------
'''


class Table():
    '''
    Def of general tables

    Parameters::
        title: str - table title
        items: list - table data
    '''

    def __init__(self, title: str = '', items: list = None):
        self.title = title
        self.items = items if items else []

    def __str__(self):
        res = ''
        for item in self.items:
            res += str(item) + '\n'

        return res

    def add(self, item: tuple = None):
        '''
        Add single item to list

        Parameters::
            item: tuple - a table item
        '''

        self.items.append(item)

    def print_tab(self):
        '''Output items in a pretty table'''
