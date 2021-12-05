import os
import re
import sys
import ast
import tokenize


# Misc Functions
def is_camel_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s


def parse(fle):
    return ast.parse(tokenize.open(fle).read(), fle)


# S001 - Length of line is not less than 80
def len_line(ind, ln):
    try:
        assert len(ln) < 80
    except AssertionError:
        print(f"{path}: Line {ind + 1}: S001 Too long")


# S002 - Indentation is not a multiple of 4
def indent(ind, ln):
    try:
        assert (len(ln) - len(ln.lstrip(' '))) % 4 == 0
    except AssertionError:
        print(f"{path}: Line {ind + 1}: S002 Incorrect indentation")


# S003 - Unnecessary semicolon after a statement
def semicolon(ind, ln):
    try:
        if '#' in ln:
            ln = ln[:ln.index('#')]
        ln = re.sub('".*?"', '', ln)
        ln = re.sub("'.*?'", '', ln)
        assert ';' not in reversed(ln)
    except AssertionError:
        print(f"{path}: Line {ind + 1}: S003 Unnecessary semicolon")


# S004 - Less than 2 spaces before inline comments
def spaces(ind, ln):
    try:
        if '#' in ln:
            ln_index = ln.index('#')
            if ln_index > 1:
                assert (ln[ln_index - 1] == ' ' and ln[ln_index - 2] == ' ')
    except AssertionError:
        print(f"{path}: Line {ind + 1}: S004 At least two spaces required before inline comments")


# S005 - To do found
def todo(ind, ln):
    try:
        if '#' in ln:
            ln_index = ln.index('#')
            assert "todo" not in ln[ln_index:].lower()
    except AssertionError:
        print(f"{path}: Line {ind + 1}: S005 TODO found")


# S006 - More than two blank lines preceding a code line
def blank_lines(ind, ln):
    try:
        if lines[ind - 2]:
            if lines[ind - 1] == '\n' and lines[ind - 2] == '\n':
                assert lines[ind - 3] != '\n'
    except AssertionError:
        print(f"{path}: Line {ind + 1}: S006 More than two blank lines preceding a code line")


# S007 - Too many spaces after construction_name (def or class)
def name_spaces(ind, ln):
    try:
        if 'def' in ln:
            ln = ln.partition('def')[2]
            ln = list(ln)
            assert ln[0] + ln[1] != '  '
        elif 'class' in ln:
            ln = ln.partition('class')[2]
            ln = list(ln)
            assert ln[0] + ln[1] != '  '
    except AssertionError:
        print(f"{path}: Line {ind + 1}: S007 Too many spaces after 'class'")


# S008 - Class name class_name should be written in CamelCase
def camel_case(ind, ln):
    try:
        if 'class' in ln:
            ln = ln.partition('class')[2]
            ln = ln.lstrip()
            first_word = ln.split()[0]
            assert is_camel_case(first_word)
    except AssertionError:
        print(f"{path}: Line {ind + 1}: S008 Class name should use CamelCase")


# S009 - Function name function_name should be written in snake_case
def snake_case(ind, ln):
    try:
        if 'def' in ln:
            ln = ln.partition('def')[2]
            ln = ln.lstrip()
            first_word = ln.split()[0]
            assert is_camel_case(first_word) == False
    except AssertionError:
        print(f"{path}: Line {ind + 1}: S009 Function name should use snake_case")


# S010 - Argument name arg_name should be written in snake_case
def arg_case(pth):
    errors = []
    parsed_file = parse(pth)
    for x in ast.walk(parsed_file):
        if isinstance(x, ast.FunctionDef):
            if x.args.args:
                for i in x.args.args:
                    if is_camel_case(i.arg):
                        errors.append(f'{pth}: Line {i.lineno}: S010 Argument name {i.arg} should be snake_case')
    for error in errors:
        print(error)


# S011 - Variable var_name should be written in snake_case
def var_case(pth):
    errors = []
    used_vars = []
    for x in ast.walk(parse(pth)):
        if isinstance(x, ast.Name):
            if is_camel_case(x.id):
                if x.id not in used_vars:
                    errors.append(f'{pth}: Line {x.lineno}: S011 Variable {x.id} in function should be snake_case')
                used_vars.append(x.id)
    for error in errors:
        print(error)


# S012 - The default argument value is mutable
def is_mutable(pth):
    errors = []
    for x in ast.walk(parse(pth)):
        if isinstance(x, ast.FunctionDef):
            for i in ast.iter_child_nodes(x):
                if isinstance(i, ast.arguments):
                    if i.defaults:
                        for thing in i.defaults:
                            if isinstance(thing, ast.List) or isinstance(thing, ast.Set) or isinstance(thing, ast.Dict):
                                errors.append(f'{pth}: Line {thing.lineno}: S012 Default argument value is mutable')
    for error in errors:
        print(error)


args = sys.argv
if ".py" in args[1]:
    path = args[1]
    lines = open(path, 'r').readlines()
    for index, line in enumerate(lines):
        len_line(index, line)
        indent(index, line)
        semicolon(index, line)
        spaces(index, line)
        todo(index, line)
        blank_lines(index, line)
        name_spaces(index, line)
        camel_case(index, line)
        snake_case(index, line)
    arg_case(path)
    var_case(path)
    is_mutable(path)
elif args[1]:
    py_files = []
    for file in os.listdir(args[1]):
        if file.endswith(".py"):
            py_files.append(file)
    py_files = sorted(py_files)
    for file in py_files:
        path = f'{args[1]}/{file}'
        lines = open(path, 'r').readlines()
        for index, line in enumerate(lines):
            len_line(index, line)
            indent(index, line)
            semicolon(index, line)
            spaces(index, line)
            todo(index, line)
            blank_lines(index, line)
            name_spaces(index, line)
            camel_case(index, line)
            snake_case(index, line)
        arg_case(path)
        var_case(path)
        is_mutable(path)
