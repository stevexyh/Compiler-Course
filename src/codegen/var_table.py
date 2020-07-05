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
from tools import gen_table as gt


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
        header = [
            {'header': 'Name', 'justify': 'center', 'style': 'green'},
            {'header': 'Type', 'style': 'cyan'},
            {'header': 'Value', 'style': 'red'},
        ]

        data = []

        for item in self.items:
            name = item
            var_type = self.items[item]['var_type']
            value = str(self.items[item]['var_items']) if var_type == 'Array' else str(self.items[item]['value'])
            value = value.replace('[', '').replace(']', '')

            data.append((name, var_type, value))

        gt.print_table(header_list=header, data_list=data)

    def add(self, item: dict = None):
        '''
        Add single item to VarTab

        Parameters::

        - for single var
            item: dict - a VarTab item {
                '<var name(e.g. var_1)>' : {
                    'value' : 1,
                    'var_type' : 'integer',
                }
            }

        - for array
            item: dict - a VarTab item {
                '<array name(e.g. arr_1)>' : {
                    'value': (arr_begin, arr_end, arr_type),
                    'var_type': 'Array',    # DO NOT EDIT THIS VALUE
                    'var_items': [],        # DO NOT EDIT THIS VALUE
                }
            }
        '''

        self.items.update(item)

    def update(self, var_name: str = '', arr_idx: int = None, value=None):
        '''
        Update value for vars

        Parameters::
            var_name: str - name of the var to be updated
            value: - value to be set
        '''

        if arr_idx is None:
            if self.exist(var_name):
                self.items[var_name]['value'] = value
            else:
                print(f'Undefined var "{var_name}"')
                sys.exit(-1)
        else:
            if self.exist(var_name):
                arr_begin = self.items[var_name]['value'][0]
                arr_end = self.items[var_name]['value'][1]

                if arr_idx in range(arr_begin, arr_end):
                    self.items[var_name]['var_items'][arr_idx] = value
                else:
                    print(f'Array index({arr_idx}) out of range({arr_begin},{arr_end})')
                    sys.exit(-1)
            else:
                print(f'Undefined array "{var_name}"')
                sys.exit(-1)

    def search(self, var_name: str = '', arr_idx: int = None):
        '''
        Search value for vars

        Parameters::
            var_name: str - name of the queried var
        Returns::
            var1
        '''

        if arr_idx is None:
            res = self.items.get(var_name)
        else:
            arr_begin = self.items[var_name]['value'][0]
            arr_end = self.items[var_name]['value'][1]

            if arr_idx in range(arr_begin, arr_end):
                res = self.items.get(var_name)['var_items'][arr_idx]
            else:
                print(f'Array index({arr_idx}) out of range({arr_begin},{arr_end})')
                sys.exit(-1)

        return res

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
