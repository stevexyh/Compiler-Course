#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---------------------------------------------
* Project Name : Compiler-Course
* File Name    : quadruple.py
* Description  : Class def for quadruple(四元式)
* Create Time  : 2020-06-25 21:06:09
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
---------------------------------------------
* Notice
- 
- 
---------------------------------------------
'''


class Quadruple():
    '''
    Def of quadruple

    Parameters::
        items: list - items in list should be a tuple(quadruple)
    '''

    def __init__(self, items: list = None):
        self.items = items if items else []

    def __str__(self):
        res = ''
        for quad in self.items:
            qd_1 = quad[1].name if quad[1].name else quad[1].value
            qd_2 = quad[2].name if quad[2].name else quad[2].value
            res += str((quad[0], qd_1, qd_2, quad[3])) + '\n'

        return res

    def print_quad(self):
        '''Output quadruples in a pretty table'''

    def add(self, item: tuple = None):
        '''
        Add items to quadruple list

        Parameters::
            item: tuple - a quadruple item (OP，arg1，arg2，result)
        '''

        self.items.append(item)
