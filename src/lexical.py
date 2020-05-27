#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
* Project Name : Compiler-Course
* File Name    : lexical.py
* Description  : Lexer for the project
* Create Time  : 2020-05-28 02:07:25
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
'''

# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------

import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    # print(f'\nLine {t.lexer.lineno}')
    print('-'*50)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print(t.lineno, f"Illegal TOKEN '{t.value[0]}' at {t.lexpos}")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out
data = '''3 + 4 * 10 + -20 *2
1+1=2
+-*/
()
xx
'''

# Give the lexer some input
lexer.input(data)
# Tokenize
for tok in lexer:
    print(tok.lineno, tok.type, tok.value, tok.lexpos)
print('#EOF')
