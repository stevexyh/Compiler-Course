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

import ply.lex as lex

'''
    词法分析的Token(终结符):
    GE    	    大于等于 >=
    LE    	    小于等于 <=
    NE    	    不等于 <>
    AssignOper  :=

    IntNo  	    无符号整数
    RealNo 	    无符号实数 含科学计数法
    Iden   	    标识符 以字母或下划线开头，后面紧跟字母或数字或下划线的字符串

    Program     关键字 program
    Var         关键字 var
    Begin       关键字 begin
    End         关键字 end
    While       关键字 while
    If          关键字 if
    Then        关键字 then
    Else        关键字 else
    And         关键字 and 逻辑与
    Not         关键字 not 逻辑非
    Or          关键字 or  逻辑或
    Integer     关键字 integer 整数类型
    Real        关键字 reald 实数类型

    还有文法中的分隔符、算符等字符关键字
'''

reserved = {
    'program': 'Program',
    'var': 'Var',
    'begin': 'Begin',
    'end': 'End',
    'while': 'While',
    'if': 'If',
    'then': 'Then',
    'else': 'Else',
    'and': 'And',
    'not': 'Not',
    'or': 'Or',
    'integer': 'Integer',
    'reald': 'Real',
}

# List of token names.   This is always required
tokens = [
    'GE',
    'LE',
    'NE',
    'AssignOper',
    'IntNo',
    'RealNo',
    'Iden',
] + list(reserved.values())

# Regular expression rules for simple tokens
t_GE = r'>='
t_LE = r'<='
t_NE = r'<>'
t_AssignOper = r':='


# A regular expression rule with some action code
def t_Iden(t):
    r'( |\t|^|$)+([a-zA-Z]|_)\w*( |\t|^|$)+'

    # Check for reserved words
    t.type = reserved.get(t.value, 'Iden')
    return t


def t_RealNo(t):
    r'( |\t|^|$)+\d*\.\d+( |\t|^|$)+'
    t.value = float(t.value)
    return t


def t_IntNo(t):
    r'( |\t|^|$)+\d+( |\t|^|$)+'
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
    err_token = t.value.split()[0]
    # print('*'*10 + str(err_token) + '*'*10)
    print(t.lineno, f"INVALID TOKEN '{err_token}' at {t.lexpos}")
    t.lexer.skip(len(err_token))


# Build the lexer
lexer = lex.lex()

# Test it out
data = '''var myVar := 1
xyz
123
0123
0.123   .123    +.123   -.123   +0234.123   -0213.123   123.456
aaaa
0abc := 1
_abc := 2
@abc
123
1e3 1E3

>= <= <>
and or if else while
abc.123
1.5E3
1e-3    1ee3
'''

# Give the lexer some input
lexer.input(data)
# Tokenize
for tok in lexer:
    print(tok.lineno, tok.type, tok.value)
print('#EOF')

# print(dir(lex))
