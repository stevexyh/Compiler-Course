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


import sys
import beeprint
from .table import Table


class VarTable(Table):
    '''
    Def of Var Table

    Parameters::
        title: str - table title
        items: dict - table data
    '''

    def __init__(self, title: str = 'Var Table', items: list = None):
        Table.__init__(self, title=title)
        self.items = items if items else {}

    def __str__(self):
        res = beeprint.pp(self.__dict__, output=False)

        return res

    # XXX(Steve X): 符号表美化输出
    def print_tab(self):
        '''Output items in a pretty table'''

    def add(self, item: dict = None):
        '''
        Add single item to VarTab

        Parameters::
            item: dict - a VarTab item {
                '<var name(e.g. var_1)>' : {
                    'value' : 1,
                    'var_type' : 'integer',
                }
            }
        '''

        self.items.update(item)

    def update(self, var_name: str = '', value=None):
        '''
        Update value for vars

        Parameters::
            var_name: str - name of the var to be updated
            value: - value to be set
        '''

        if self.exist(var_name):
            self.items[var_name]['value'] = value
        else:
            print(f'Undefined var "{var_name}"')
            sys.exit(-1)

    def exist(self, key: str = ''):
        '''
        Check if the var is already defined

        Parameters::
            key: str - var name
        Returns::
            res: bool - True for exist & False for not defined
        '''

        res = False if self.items.get(key) is None else True

        return res
