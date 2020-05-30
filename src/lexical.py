#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---------------------------------------------
* Project Name : Compiler-Course
* File Name    : lexical.py
* Description  : Lexer for the project
* Create Time  : 2020-05-28 02:07:25
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
---------------------------------------------
* Notice

- 词法分析的Token(终结符):
    * GE            大于等于 >=
    * LE            小于等于 <=
    * NE            不等符号 <>
    * AssignOper    赋值符号 :=

    * IntNo         无符号整数
    * RealNo        无符号实数      含科学计数法
    * Iden          变量标识符      以字母或下划线开头，后面紧跟字母或数字或下划线的字符串

    * Program       关键字 program
    * Var           关键字 var
    * Begin         关键字 begin
    * End           关键字 end
    * While         关键字 while
    * If            关键字 if
    * Then          关键字 then
    * Else          关键字 else
    * And           关键字 and      逻辑与
    * Not           关键字 not      逻辑非
    * Or            关键字 or       逻辑或
    * Integer       关键字 integer  整数类型
    * Real          关键字 reald    实数类型

- 还有文法中的分隔符、算符等字符关键字
---------------------------------------------
'''
# TODO(Steve X): 识别文法中的分隔符、算符等字符关键字


import ply.lex as lex
import format_string as fs

INPUT_FILE = 'input_pascal/input.pas'


#---------------------------------Preset vars for PLY module---------------------------------#
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


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
#--------------------------------------------END---------------------------------------------#


#-----------------------------RegEx rules for preset functions-------------------------------#
def t_Iden(t):
    r'\b[a-zA-Z_][0-9a-zA-Z_]*\b[^\.]'
    if t.value.endswith('\n'):
        t_newline(t)

    # Check for reserved words
    t.value = t.value.strip()
    t.type = reserved.get(t.value, 'Iden')
    return t


def t_RealNo(t):
    r'\b(\d*\.\d+|\d+(\.\d+)?([Ee][+-]?\d+))\b[^\.]'
    if t.value.endswith('\n'):
        t_newline(t)

    t.value = float(t.value)
    return t


def t_IntNo(t):
    r'\b[0-9]+\b[^\.]'
    if t.value.endswith('\n'):
        t_newline(t)

    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1


def t_error(t):
    '''
    Error handling rule

    Parameters::
        t:LexToken - a token instance
    '''
    err_token = t.value.split()[0]
    column = find_column(input_str=INPUT_DATA, token=t)
    err_line = INPUT_DATA.splitlines()[t.lineno - 1]

    # Locate and mark the error
    fs.err_en({
        (' ' + str(t.lineno) + f' File "{INPUT_FILE}", line {t.lineno},col {column} '.ljust(35)): f" INVALID TOKEN '{err_token}'"
    })
    print(err_line)
    print(' '*(column - 1) + '='*len(err_token))
    print(' '*(column - 1) + '↑')
    print('-'*TABLE_LEN)

    t.lexer.skip(len(err_token))
#--------------------------------------------END---------------------------------------------#


def find_column(input_str: str, token: lex.LexToken):
    '''
    Compute column.

    Parameters::
        input: str - the input text string
        token: LexToken - a token instance
    Returns::
        column: int - the column number of the token
    '''
    line_start = input_str.rfind('\n', 0, token.lexpos) + 1
    column = (token.lexpos - line_start) + 1
    return column


def read_data(file_name: str = INPUT_FILE):
    '''
    Read data from input Pascal file

    Parameters::
        file_name: str - name of the input file
    Returns::
        data: str - data read from the file
    '''
    data = ''
    with open(file_name) as input_file:
        data = input_file.read()

    return data


def buile_lines(data: str = ''):
    '''
    Input pascal file and run test
    Classify valid tokens by line number

    Parameters::
        data: str - the input string
    Returns::
        lines: list - a sorted list of tokens
    '''
    # Build the lexer
    lexer = lex.lex()
    lexer.input(data)

    line_no = 0
    lines = [[{'line_num': line_no}]]
    for tok in lexer:
        while True:
            if tok.lineno == line_no:
                lines[line_no].append(tok)
                break
            else:
                line_no += 1
                lines.append([])
                lines[0][0]['line_num'] = line_no

        print(tok.lineno, tok.type, tok.value)

    print('#EOF')
    return lines


if __name__ == "__main__":
    TABLE_LEN = 80
    INPUT_DATA = read_data(file_name='../' + INPUT_FILE)
    LINE_LIST = []
    LINE_LIST = buile_lines(data=INPUT_DATA)
    for l in LINE_LIST:
        print(l)
    print(LINE_LIST[0][0]['line_num'])
