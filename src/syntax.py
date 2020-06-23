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
                    | IBT   Statement
                    | WBD Statement
                    | CompState
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


def p_ProgDef(p):
    '''ProgDef : Program Iden ';' SubProg '.' '''


def p_SubProg(p):
    'SubProg : VarDef CompState'


def p_VarDef(p):
    '''VarDef : Var VarDefList ';' '''


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


def p_VarList(p):
    '''VarList  : VarList ',' Variable
                | Variable
    '''


def p_StateList(p):
    '''StateList    : S_L Statement
                    | Statement
    '''


def p_S_L(p):
    '''S_L : StateList ';' '''


def p_Statement(p):
    '''Statement    : AssignState
                    | ISE Statement
                    | IBT   Statement
                    | WBD Statement
                    | CompState
    '''


def p_CompState(p):
    '''CompState : Begin StateList End'''


def p_AssignState(p):
    '''AssignState : Variable AssignOper Expr'''


def p_ISE(p):
    '''ISE : IBT Statement Else'''


def p_IBT(p):
    '''IBT : If BoolExpr Then'''


def p_WBD(p):
    '''WBD : Wh BoolExpr Do'''


def p_Wh(p):
    '''Wh : While'''


# TODO(Steve X): 完成语法规则p[0]
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


def p_BoolExpr(p):
    '''BoolExpr : Expr RelationOp Expr
                | BoolExpr And BoolExpr
                | BoolExpr Or BoolExpr
                | Not BoolExpr
                | '(' BoolExpr ')'
    '''


def p_Variable(p):
    '''Variable : Iden'''


def Const(p):
    '''Const    : IntNo
                | RealNo
    '''


# TODO(Steve X): 完成p[0]
def p_RelationOp(p):
    '''RelationOp   : '<'
                    | '>'
                    | '='
                    | GE
                    | NE
                    | LE
    '''


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


def p_empty(p):
    'empty :'
    pass


# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    result = parser.parse(s)
    print(result)
