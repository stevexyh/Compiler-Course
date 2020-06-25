#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---------------------------------------------
* Project Name : Compiler-Course
* File Name    : var_table.py
* Description  : Class def for Token Table (for vars)
* Create Time  : 2020-06-25 23:44:42
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
---------------------------------------------
* Notice
-
-
---------------------------------------------
'''


from .table import Table


class VarTable(Table):
    '''
    Def of Var Table

    Parameters::
        title: str - table title
        items: list - table data
    '''

    def __init__(self, title: str = '', items: list = None):
        Table.__init__(self, title=title, items=items)

    def print_tab(self):
        '''Output items in a pretty table'''

    def add(self, item: dict = None):
        '''
        Add single item to VarTab

        Parameters::
            item: dict - a VarTab item {
                'name' : 'var_1',
                'value' : 1,
                'var_type' : 'integer',
            }
        '''

        Table.add(self, item=item)
