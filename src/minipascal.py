#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---------------------------------------------
* Project Name : Compiler-Course
* File Name    : minipascal.py
* Description  : Entry of minipascal parser
* Create Time  : 2020-06-23 19:36:31
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
---------------------------------------------
* Notice
- 
- 
---------------------------------------------
'''

import lexical
from lexical import tokens
import syntax

lexical.lexer.lineno = 1
INPUT_FILE = 'input_pascal/addition.pas'
with open('../' + INPUT_FILE) as f:
    data = f.read()
    prog = syntax.parser.parse(data)
