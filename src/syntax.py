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
    * G[ProgDef]:
    * ProgDef       :Program Iden ';' SubProg '.'
    * SubProg       :VarDef CompState
    * VarDef        :Var VarDefList ';'
    * VarDefList    :VarDefList';'VarDefState | VarDefState
    * VarDefState   :VarList':'Type
    * Type          :Integer  |  Real
    * VarList       :VarList','Variable  |  Variable
    * StateList     :S_L Statement  |  Statement
    * S_L           :StateList ';'
    * Statement     :AssignState  |  ISE Statement  |  IBT   Statement
                    |  WBD Statement  |  CompState
                    |
    * CompState     :Begin StateList End
    * AssignState   :Variable AssignOper Expr
    * ISE           :IBT Statement Else
    * IBT           :If BoolExpr Then
    * WBD           :Wh BoolExpr Do
    * Wh            :While
    * Expr          :Expr'+'Expr  |  Expr'-'Expr  |  Expr'*'Expr
                    |  Expr'/'Expr  |  '('Expr')'   |  '-' Expr %prec UMINUS
                    |  Variable  |  Const
    * BoolExpr      :Expr RelationOp Expr  |  BoolExpr And BoolExpr  |  BoolExpr Or BoolExpr
                    |  Not BoolExpr  |  '(' BoolExpr ')'
    * Variable      :Iden
    * Const         :IntNo  |  RealNo
    * RelationOp    :'<'  |  '>'  |  '='
                    |  GE  |  NE  |  LE

- 算法的优先级类似于C语言，请自行搜索确定
- 条件语句的else限制同C语言
---------------------------------------------
'''
