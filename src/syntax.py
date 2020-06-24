#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---------------------------------------------
* Project Name : Compiler-Course
* File Name    : syntax.py
* Description  : Syntax parse
* Create Time  : 2020-06-02 15:13:02
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
---------------------------------------------
* Notice

- MIniPascal语言的文法：
    G[ProgDef]:
    * ProgDef       : Program Iden ';' SubProg '.'
    * SubProg       : VarDef CompState
    * VarDef        : Var VarDefList ';'
    * VarDefList    : VarDefList ';' VarDefState
                    | VarDefState
    * VarDefState   : VarList ':' Type
    * Type          : Integer
                    | Real
    * VarList       : VarList ',' Variable
                    | Variable
    * StateList     : S_L Statement
                    | Statement
    * S_L           : StateList ';'
    * Statement     : AssignState
                    | ISE Statement
                    | IBT Statement
                    | WBD Statement
                    | CompState
                    | empty
    * CompState     : Begin StateList End
    * AssignState   : Variable AssignOper Expr
    * ISE           : IBT Statement Else
    * IBT           : If BoolExpr Then
    * WBD           : Wh BoolExpr Do
    * Wh            : While
    * Expr          : Expr '+' Expr
                    | Expr '-' Expr
                    | Expr '*' Expr
                    | Expr '/' Expr
                    | '(' Expr ')'
                    | '-' Expr %prec UMINUS
                    | Variable
                    | Const
    * BoolExpr      : Expr RelationOp Expr
                    | BoolExpr And BoolExpr
                    | BoolExpr Or BoolExpr
                    | Not BoolExpr
                    | '(' BoolExpr ')'
    * Variable      : Iden
    * Const         : IntNo
                    | RealNo
    * RelationOp    : '<'
                    | '>'
                    | '='
                    | GE
                    | NE
                    | LE

- 算法的优先级类似于C语言，请自行搜索确定
- 条件语句的else限制同C语言
---------------------------------------------
'''

import ply.yacc as yacc
from lexical import tokens
from codegen import ast as ast


#----------------------------Preset grammar def functions for PLY----------------------------#
def p_ProgDef(p):
    '''ProgDef : Program Iden ';' SubProg '.' '''


def p_SubProg(p):
    '''SubProg : VarDef CompState'''


# FIXME(Steve X): store var into variable_list
def p_VarDef(p):
    '''VarDef : Var VarDefList ';' '''

    if len(p) > 2:
        p[0] = p[2]


def p_VarDefList(p):
    '''VarDefList   : VarDefList ';' VarDefState
                    | VarDefState
    '''


def p_VarDefState(p):
    '''VarDefState : VarList ':' Type'''


def p_Type(p):
    '''Type : Integer
            | Real
    '''

    p[0] = ast.Node(node_type='VarList', value=p[2], children=[p[1]])


def p_VarList(p):
    '''VarList  : VarList ',' Variable
                | Variable
    '''

    if len(p) == 2:
        p[0] = ast.Node(node_type='VarList', value=p[2], children=[p[1]])
    elif len(p) == 4:
        p[0] = ast.Node(node_type='VarList', value=p[2], children=[p[1], p[3]])


def p_StateList(p):
    '''StateList    : S_L Statement
                    | Statement
    '''

    print('-'*10, 'StateList')
    for i in p:
        print(i)
    print('-'*10)


def p_S_L(p):
    '''S_L : StateList ';'
    '''


def p_Statement(p):
    '''Statement    : AssignState
                    | ISE Statement
                    | IBT Statement
                    | WBD Statement
                    | CompState
                    | empty
    '''


def p_CompState(p):
    '''CompState : Begin StateList End'''


def p_AssignState(p):
    '''AssignState : Variable AssignOper Expr'''
    # p[0] = p[3]

    print('-'*10, 'Assign')
    for i in p:
        print(i)
    print('-'*10)


def p_ISE(p):
    '''ISE : IBT Statement Else'''


def p_IBT(p):
    '''IBT : If BoolExpr Then'''


def p_WBD(p):
    '''WBD : Wh BoolExpr Do'''


def p_Wh(p):
    '''Wh : While'''


# FIXME(Steve X): Variable, Const 那里不知道对不对
def p_Expr(p):
    '''Expr : Expr '+' Expr
            | Expr '-' Expr
            | Expr '*' Expr
            | Expr '/' Expr
            | '(' Expr ')'
            | '-' Expr %prec UMINUS
            | Variable
            | Const
    '''
    # 'expression : expression op term'
    #   ^            ^          ^  ^
    #  p[0]         p[1]      p[2] p[3]

    if len(p) == 4:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[1] == '(' and p[3] == ')':
            p[0] = p[2]
    elif p[1] == '-':
        p[0] = -p[2]
    elif len(p) == 2:
        p[0] = p[1]
    else:
        for i in p:
            print('err>>>', i, '<<<', end='|')
        print('')

    print('-'*10, 'Expr')
    for i in p:
        print(i)
    print('-'*10)


def p_BoolExpr(p):
    '''BoolExpr : Expr RelationOp Expr
                | BoolExpr And BoolExpr
                | BoolExpr Or BoolExpr
                | Not BoolExpr
                | '(' BoolExpr ')'
    '''
    # 'expression : expression op term'
    #   ^            ^          ^  ^
    #  p[0]         p[1]      p[2] p[3]

    if len(p) == 4 and p[0]:
        print('-'*10)
        for i in p:
            print(i)
        print('-'*10)
        if p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '=':
            p[0] = p[1] == p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]
        elif p[2] == '<>':
            p[0] = p[1] != p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]
        elif p[2] == 'and':
            p[0] = p[1] and p[3]
        elif p[2] == 'or':
            p[0] = p[1] or p[3]
        elif p[1] == '(' and p[3] == ')':
            p[0] = p[2]
    elif len(p) == 2 and p[1] == 'not':
        p[0] = not p[1]
    else:
        for i in p:
            print('/*******/', i, '/******/', end='|')
        print('')


def p_Variable(p):
    '''Variable : Iden'''

    p[0] = p[1]


def p_Const(p):
    '''Const    : IntNo
                | RealNo
    '''

    p[0] = p[1]


def p_RelationOp(p):
    '''RelationOp   : '<'
                    | '>'
                    | '='
                    | GE
                    | NE
                    | LE
    '''

    p[0] = p[1]


# Operator precedence
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)


def p_empty(p):
    'empty :'

    pass


# Error rule for syntax errors
# def p_error(p):
#     print("Syntax error in input!")
#     print(p)
def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")


# Store the declared vars
variable_list = {}

# Build the parser
parser = yacc.yacc(debug=True)

#--------------------------------------------END---------------------------------------------#


# INPUT_FILE = 'input_pascal/addition.pas'
# with open('../' + INPUT_FILE) as f:
#     data = f.read()
#     prog = parser.parse(data)
#     print(prog)

# result = parser.parse(lx.INPUT_DATA)
# print(result)
# while True:
#     try:
#         s = input('input > ')
#     except EOFError:
#         break
#     if not s:
#         continue
#     result = parser.parse(s)
#     print(result)
