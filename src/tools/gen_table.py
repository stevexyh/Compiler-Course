#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---------------------------------------------
* Project Name : Compiler-Course
* File Name    : gen_table.py
* Description  : Generate and render tables
* Create Time  : 2020-06-01 19:39:15
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
---------------------------------------------
* Notice
- pip install rich
---------------------------------------------
'''


from rich.console import Console
from rich.table import Table


def print_table(title: str = '', header_list: list = None, data_list: list = None):
    '''
    Render and print a tible in beautiful style

    Parameters::
        title: str - title of the table
        header_list: list - header of each column, e.g. [{'header': '', 'justify': '', 'style': ''}]
        data_list: list - data of the table, e.g. [(val_1, val_2,...)]
    '''

    table = Table(title=title)

    # Add header for each column
    for hdr in header_list:
        try:
            table.add_column(
                header=hdr['header'],
                justify=hdr['justify'],
                style=hdr['style']
            )
        except KeyError:
            table.add_column(
                header=hdr['header'],
            )

    # Add data for each row
    for row in data_list:
        table.add_row(*row)

    console = Console()
    console.print(table)


if __name__ == "__main__":
    header = [
        {'header': 'Ln', 'justify': 'center', 'style': 'green'},
        {'header': 'Type', 'style': 'cyan'},
        {'header': 'Value', 'style': 'red'},
    ]

    data = [
        ('1', 'int', '123'),
        ('2', 'float', '1.23'),
        ('3', 'str', 'this is a string'),
    ]
    print_table(header_list=header, data_list=data)
