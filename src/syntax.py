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


import sys
import ply.yacc as yacc
import tools.format_string as fs
from lexical import tokens
from lexical import lexer
from codegen import ast
from codegen import quadruple
from codegen import var_table


#----------------------------Preset grammar def functions for PLY----------------------------#
def p_ProgDef(p):
    '''ProgDef : Program Iden ';' SubProg '.' '''

    p[2] = ast.Node(node_type='Program', value=p[2])
    p[0] = ast.Node(node_type='ProgDef', children=[p[2], p[4]])


def p_SubProg(p):
    '''SubProg : VarDef CompState'''

    p[0] = ast.Node(node_type='SubProg', children=[p[1], p[2]])


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
    for var in p[1].value:
        if variable_list.exist(var.name):
            print(f'Line {lexer.lineno}: Redefined var "{var.name}"')
            sys.exit(-1)
        else:
            if p[3].node_type == 'ArrayType':
                arr_begin = p[3].value[0]
                arr_end = p[3].value[1]

                variable_list.add({
                    var.name: {
                        'value': p[3].value,
                        'var_type': 'Array',
                        'var_items': [0 for i in range(arr_begin, arr_end)],
                    }
                })
            else:
                variable_list.add({
                    var.name: {
                        'value': var.value,
                        'var_type': p[3].value,
                    }
                })


def p_Type(p):
    '''Type : Type_Single
            | ArrayType
    '''

    p[0] = ast.Node(node_type=p[1].node_type, value=p[1].value)


def p_Type_Single(p):
    '''Type_Single  : Integer
                    | Real
    '''

    p[0] = ast.Node(node_type='Type', value=p[1])


# XXX(Steve X): 二维数组还不支持, 等一会再改吧, 一维的又不是不能用
# XXX(Steve X): Pascal语法的数组下标和主流语言似乎不太一样, 如果需要的话再改吧
def p_ArrayType(p):
    '''ArrayType : ARRAY '[' IntNo '.' '.' IntNo ']' OF Type_Single'''
    #  ^           ^      ^  ^      ^   ^  ^      ^  ^   ^
    #  p[0]       p[1]  p[2]p[3]  p[4]p[5] p[6] p[7]p[8] p[9]

    arr_begin = p[3]
    arr_end = p[6] + 1

    p[0] = ast.Node(node_type='ArrayType', value=(arr_begin, arr_end, p[9].value), children=[p[3], p[6], p[9]])


# XXX(Steve X): 输出 AST 时, VarList 每一步元素都不变
def p_VarList(p):
    '''VarList  : VarList ',' Variable
                | Variable
    '''

    if len(p) == 2:
        if p[1].node_type == 'Variable_Arr':
            print('Invalid Syntax: Can not declare an array element')
            sys.exit(-1)

        p[0] = ast.Node(node_type='VarList', value=[p[1]], children=[p[1]])
    elif len(p) == 4:
        if p[3].node_type == 'Variable_Arr':
            print('Invalid Syntax: Can not declare an array element')
            sys.exit(-1)

        p[1].value.append(p[3])
        p[0] = ast.Node(node_type='VarList', value=p[1].value, children=[p[1], p[3]])


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

    var_name = p[1].value[2] if p[1].node_type == 'Variable_Arr' else p[1].name

    if variable_list.exist(var_name):
        p[0] = ast.Node(node_type='AssignState', children=[p[1], p[3]])
        p[1].value = (p[3].value, p[1].value[1], p[1].value[2])
        variable_list.update(var_name=var_name, arr_idx=p[1].value[1], value=p[1].value[0])
    else:
        print(f'Line {lexer.lineno}: Undefined var "{p[1].name}"')
        sys.exit(-1)


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
        p[0].name = p[1].name

        if p[1].node_type == 'Variable':
            p[0].value = variable_list.search(var_name=p[0].name)['value']
        elif p[1].node_type == 'Variable_Arr':
            p[0].value = variable_list.search(var_name=p[1].name, arr_idx=p[1].value[1])

    elif len(p) == 4:
        if p[1] == '(':
            p[0] = ast.Node(node_type='Expr', value=p[2].value, children=[p[2]])
        elif p[1] == '-':
            quad = ('-', p[1], None, -p[1].value)

            p[1] = ast.Node(node_type='UnaryOp', value=p[1])
            p[0] = ast.Node(node_type='Expr', value=quad[3], children=[p[1], p[2]])
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

            p[2] = ast.Node(node_type='BinOp', value=p[2])
            p[0] = ast.Node(node_type='Expr', value=quad[3], children=[p[1], p[2], p[3]])

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
        p[1] = ast.Node(node_type='UnaryOp', value=p[1])
        p[0] = ast.Node(node_type='BoolExpr', value=quad[3], children=[p[1], p[2]])
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


def p_BoolExpr_AndOr(p):
    '''BoolExpr_AndOr   : BoolExpr And BoolExpr
                        | BoolExpr Or BoolExpr
    '''

    if p[2] == 'and':
        quad = ('and', p[1], p[3], p[1].value and p[3].value)
    elif p[2] == 'or':
        quad = ('or', p[1], p[3], p[1].value or p[3].value)

    p[2] = ast.Node(node_type='RelationOp', value=p[2])
    p[0] = ast.Node(node_type='BoolExpr_AndOr', value=quad[3], children=[p[1], p[2], p[3]])
    quadruple_list.add(quad)


def p_Variable(p):
    '''Variable : Iden
                | Iden '[' IntNo ']'
    '''

    # Variable      - value = (var_value, None, None)
    # Variable_Arr  - value = (var_value, arr_idx, arr_name)

    if len(p) == 2:
        p[0] = ast.Node(node_type='Variable', value=(0, None, None), name=p[1])
    elif len(p) == 5:
        arr_val = variable_list.search(var_name=p[1], arr_idx=p[3])
        p[0] = ast.Node(node_type='Variable_Arr', value=(arr_val, p[3], p[1]), name=f'{p[1]}[{3}]')


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
    if p is None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    err_info = fs.set_color(string=f'Syntax error: Unexpected {token}', color='redBack')
    print(err_info)
    sys.exit(-1)


print(tokens)


# Build the parser
parser = yacc.yacc(debug=True)
#--------------------------------------------END---------------------------------------------#

# Store the declared vars & quadruples
# quadruple = (OP，arg1，arg2，result)
variable_list = var_table.VarTable()
quadruple_list = quadruple.Quadruple()
