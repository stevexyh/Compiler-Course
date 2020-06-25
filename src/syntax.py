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
from codegen import quadruple
from codegen import ast as ast


#----------------------------Preset grammar def functions for PLY----------------------------#
def p_ProgDef(p):
    '''ProgDef : Program Iden ';' SubProg '.' '''

    p[2] = ast.Node(node_type='Program', value=p[2])
    p[0] = ast.Node(node_type='ProgDef', children=[p[2], p[4]])


def p_SubProg(p):
    '''SubProg : VarDef CompState'''

    p[0] = ast.Node(node_type='SubProg', children=[p[1], p[2]])


# FIXME(Steve X): store var into variable_list(符号表)
def p_VarDef(p):
    '''VarDef : Var VarDefList ';' '''

    p[0] = ast.Node(node_type='VarDef', children=[p[2]])


def p_VarDefList(p):
    '''VarDefList   : VarDefList ';' VarDefState
                    | VarDefState
    '''

    if len(p) == 2:
        p[0] = ast.Node(node_type='VarDefList', children=[p[1]])
    elif len(p) == 4:
        p[0] = ast.Node(node_type='VarDefList', children=[p[1], p[3]])


def p_VarDefState(p):
    '''VarDefState : VarList ':' Type'''

    p[0] = ast.Node(node_type='VarDefState', children=[p[1], p[3]])


def p_Type(p):
    '''Type : Integer
            | Real
    '''

    p[0] = ast.Node(node_type='Type', value=p[1])


def p_VarList(p):
    '''VarList  : VarList ',' Variable
                | Variable
    '''

    if len(p) == 2:
        p[0] = ast.Node(node_type='VarList', children=[p[1]])
    elif len(p) == 4:
        p[0] = ast.Node(node_type='VarList', children=[p[1], p[3]])


def p_StateList(p):
    '''StateList    : S_L Statement
                    | Statement
    '''

    if len(p) == 2:
        p[0] = ast.Node(node_type='StateList', children=[p[1]])
    elif len(p) == 3:
        p[0] = ast.Node(node_type='StateList', children=[p[1], p[2]])


def p_S_L(p):
    '''S_L : StateList ';'
    '''

    p[0] = ast.Node(node_type='S_L', children=[p[1]])


def p_Statement(p):
    '''Statement    : AssignState
                    | ISE Statement
                    | IBT Statement
                    | WBD Statement
                    | CompState
                    | empty
    '''

    if len(p) == 2:
        p[0] = ast.Node(node_type='Statement', children=[p[1]])
    elif len(p) == 3:
        p[0] = ast.Node(node_type='Statement', children=[p[1], p[2]])


def p_CompState(p):
    '''CompState : Begin StateList End'''

    p[0] = ast.Node(node_type='CompState', children=[p[2]])


def p_AssignState(p):
    '''AssignState : Variable AssignOper Expr'''

    p[0] = ast.Node(node_type='AssignState', children=[p[1], p[3]])
    p[1].value = p[3].value


def p_ISE(p):
    '''ISE : IBT Statement Else'''

    p[0] = ast.Node(node_type='ISE', children=[p[1], p[2]])


def p_IBT(p):
    '''IBT : If BoolExpr Then'''

    p[0] = ast.Node(node_type='IBT', children=[p[2]])


def p_WBD(p):
    '''WBD : Wh BoolExpr Do'''

    p[0] = ast.Node(node_type='WBD', children=[p[1], p[2]])


def p_Wh(p):
    '''Wh : While'''

    p[0] = ast.Node(node_type='Wh', value=p[1])


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

    quad = None

    if len(p) == 2:
        p[0] = ast.Node(node_type='Expr', value=p[1].value, children=[p[1]])
        if p[1].node_type == 'Variable':
            p[0].name = p[1].name
            print(p[0].name, '***',p[0].value)
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = ast.Node(node_type='Expr', value=p[2].value, children=[p[2]])
        elif p[1] == '-':
            quad = ('-', p[1], None, -p[1].value)
            p[0] = ast.Node(node_type='Expr', value=quad[3], children=[p[2]])
        elif p[2] in '+-*/':
            if p[2] == '+':
                print(p[1].node_type, p[3].node_type)
                quad = ('+', p[1], p[3], p[1].value + p[3].value)
            elif p[2] == '-':
                quad = ('-', p[1], p[3], p[1].value - p[3].value)
            elif p[2] == '*':
                quad = ('*', p[1], p[3], p[1].value * p[3].value)
            elif p[2] == '/':
                quad = ('/', p[1], p[3], p[1].value / p[3].value)
            p[0] = ast.Node(node_type='Expr', value=quad[3], children=[p[1], p[3]])

    if quad:
        quadruple_list.add(quad)


def p_BoolExpr(p):
    '''BoolExpr : Expr RelationOp Expr
                | BoolExpr_AndOr
                | Not BoolExpr
                | '(' BoolExpr ')'
    '''

    quad = None

    if len(p) == 2:
        p[0] = ast.Node(node_type='BoolExpr', value=p[1].value, children=[p[1]])
    elif len(p) == 3:
        quad = ('not', p[2], None, not p[2].value)
        p[0] = ast.Node(node_type='BoolExpr', value=quad[3], children=[p[2]])
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = ast.Node(node_type='BoolExpr', value=p[2].value, children=[p[2]])
        else:
            if p[2].value == '<':
                quad = (p[2].value, p[1], p[3], p[1].value < p[3].value)
            elif p[2].value == '>':
                quad = (p[2].value, p[1], p[3], p[1].value > p[3].value)
            elif p[2].value == '=':
                quad = (p[2].value, p[1], p[3], p[1].value == p[3].value)
            elif p[2].value == '>=':
                quad = (p[2].value, p[1], p[3], p[1].value >= p[3].value)
            elif p[2].value == '<>':
                quad = (p[2].value, p[1], p[3], p[1].value != p[3].value)
            elif p[2].value == '<=':
                quad = (p[2].value, p[1], p[3], p[1].value <= p[3].value)

            p[0] = ast.Node(node_type='BoolExpr', value=quad[3], children=[p[1], p[2], p[3]])

    if quad:
        quadruple_list.add(quad)


# FIXME(Steve X): 关键字大小写匹配
def p_BoolExpr_AndOr(p):
    '''BoolExpr_AndOr   : BoolExpr And BoolExpr
                        | BoolExpr Or BoolExpr
    '''

    if p[2] == 'and':
        quad = ('and', p[1], p[3], p[1].value and p[3].value)
    elif p[2] == 'or':
        quad = ('or', p[1], p[3], p[1].value or p[3].value)

    p[0] = ast.Node(node_type='BoolExpr_AndOr', value=quad[3], children=[p[1], p[3]])
    quadruple_list.add(quad)


def p_Variable(p):
    '''Variable : Iden'''

    p[0] = ast.Node(node_type='Variable', value=0, name=p[1])


def p_Const(p):
    '''Const    : IntNo
                | RealNo
    '''

    p[0] = ast.Node(node_type='Const', value=p[1])


def p_RelationOp(p):
    '''RelationOp   : '<'
                    | '>'
                    | '='
                    | GE
                    | NE
                    | LE
    '''

    p[0] = ast.Node(node_type='RelationOp', value=p[1])


# Operator precedence
precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)


def p_empty(p):
    'empty :'

    p[0] = None


# Error rule for syntax errors
def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")


print(tokens)


# Build the parser
parser = yacc.yacc(debug=True)
#--------------------------------------------END---------------------------------------------#

# Store the declared vars & quadruples
# quadruple = (OP，arg1，arg2，result)
variable_list = {}
quadruple_list = quadruple.Quadruple()
