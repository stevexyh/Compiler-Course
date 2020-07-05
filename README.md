# Compiler-Course  
> Compiler lab project and demo  
> A minipascal parser implemented with Python-PLY  

## Files  
```
.
├── README.md
├── TODO_LIST.py
├── def
│   ├── grammar_def.txt
│   └── lexical_def.txt
├── input_pascal
│   ├── addition.pas
│   └── input.pas
├── requirements.txt
├── src
│   ├── README.md
│   ├── codegen
│   │   ├── ast.py
│   │   ├── quadruple.py
│   │   ├── table.py
│   │   └── var_table.py
│   ├── graph
│   │   ├── AST.pdf
│   │   └── AST.png
│   ├── lexical.py
│   ├── minipascal.py
│   ├── parser.out
│   ├── parsetab.py
│   ├── syntax.py
│   └── tools
│       ├── format_string.py
│       └── gen_table.py
└── test_demo

14 directories, 45 files
```

## AST
![AST Graph Loading Err](src/graph/AST.png)


## Environment
- `Python 3`
- `Linux / macOS`

## Usage  
1. Change to the src directory
   - `cd src`
2. Run
   - Run default test case
      - `python3 minipascal.py` or `./minipascal.py`
   - Run customize test cases
      - `python3 minipascal.py <file name>` or `./minipascal.py <file name>`
      - e.g. `./minipascal.py ../input_pascal/1-bool.pas`

## Installation  
- `pip install -r requirements.txt`  

## TODO List

- [x] TODO(Steve X): 使用 `flex` 实现词法分析器
- [x] TODO(Steve X): 识别 `MiniPascal` 语法要求
- [x] TODO(Steve X): 输入 `MiniPascal` 源文件
- [x] TODO(Steve X): 识别文法中的分隔符、算符等字符关键字(应该是 `yacc` 部分)
- [x] TODO(Steve X): 输出抽象语法树, 通过 `Graphviz` 显示
- [x] TODO(Steve X): 输出程序的四元式
- [x] TODO(Steve X): 输出程序中各种符号定义(符号表形式)
- [x] TODO(Steve X): 简单的错误诊断(所在行, 变量不存在, 重复定义等)
- [x] TODO(Steve X): 对数组的支持

---
**by [Steve X](https://github.com/Steve-Xyh)**  
