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

    p[2] = ast.Node(node_type='Program', value=p[2])
    p[0] = ast.Node(node_type='ProgDef', children=[p[2], p[4]])


def p_SubProg(p):
    '''SubProg : VarDef CompState'''

    p[0] = ast.Node(node_type='SubProg', children=[p[1], p[2]])


# FIXME(Steve X): store var into variable_list
def p_VarDef(p):
    '''VarDef : Var VarDefList ';' '''

    p[0] = ast.Node(node_type='VarDef',  children=[p[2]])


def p_VarDefList(p):
    '''VarDefList   : VarDefList ';' VarDefState
                    | VarDefState
    '''

    if len(p) == 2:
        p[0] = ast.Node(node_type='VarDefList',  children=[p[1]])
    elif len(p) == 4:
        p[0] = ast.Node(node_type='VarDefList',  children=[p[1], p[3]])


def p_VarDefState(p):
    '''VarDefState : VarList ':' Type'''

    p[0] = ast.Node(node_type='VarDefState',  children=[p[1], p[3]])


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

    if len(p) == 2:
        p[0] = ast.Node(node_type='Expr', children=[p[1]])
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = ast.Node(node_type='Expr', children=[p[2]])
        elif p[1] == '-':
            p[0] = ast.Node(node_type='Expr', children=[p[2]])
        elif p[2] in '+-*/':
            p[0] = ast.Node(node_type='Expr', children=[p[1], p[3]])


def p_BoolExpr(p):
    '''BoolExpr : Expr RelationOp Expr
                | BoolExpr_AndOr
                | Not BoolExpr
                | '(' BoolExpr ')'
    '''

    if len(p) == 2:
        p[0] = ast.Node(node_type='BoolExpr', children=[p[1]])
    elif len(p) == 3:
        p[0] = ast.Node(node_type='BoolExpr', children=[p[2]])
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = ast.Node(node_type='BoolExpr', children=[p[2]])
        else:
            p[0] = ast.Node(node_type='BoolExpr', children=[p[1], p[2], p[3]])


def p_BoolExpr_AndOr(p):
    '''BoolExpr_AndOr   : BoolExpr And BoolExpr
                        | BoolExpr Or BoolExpr
    '''

    p[0] = ast.Node(node_type='BoolExpr_AndOr', children=[p[1], p[3]])


def p_Variable(p):
    '''Variable : Iden'''

    p[0] = ast.Node(node_type='Variable', value=p[1])
    # p[0] = ast.Node(node_type='Variable', children=[p[1]])


def p_Const(p):
    '''Const    : IntNo
                | RealNo
    '''

    p[0] = ast.Node(node_type='Const', value=p[1])
    # p[0] = ast.Node(node_type='Const', children=[p[1]])


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


# Error rule for syntax errors
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
