import ply.lex as lex
import re

tokens = ["BEGINL","STR","LITERAL","IGNORE","TOKENS","PAL","COMMENT","RETURN","REGEXP","TVALUE","ERROR","FSTR", "ID","LBUILD","BEGINY"]
literals = ["%","=","[","]",",","(",")"]


def t_BEGINL(t):
    r'%%lexer'
    return t

def t_BEGINY(t):
    r'%%yacc'
    return t    

def t_COMMENT(t):
    r'\#\#.*'
    return t

def t_STR(t):
    r'\"[^\"]+\"'
    return t

def t_LITERAL(t):
    r'%literals'
    t.value = t.value[1:]
    return t

def t_IGNORE(t):
    r'%ignore'
    t.value = t.value[1:]
    return t

def t_TOKENS(t):
    r'%tokens'
    t.value = t.value[1:]
    return t

def t_PAL(t):
    r'\'\w+\''
    return t

def t_REGEXP(t):
    r'\/.*?(?<!\\)\/'
    t.value = t.value.replace(r'\/', r'/')[1:-1]
    return t    
    
def t_RETURN(t):
    r'return'
    return t

def t_ERROR(t):
    r'error'
    return t


def t_TVALUE(t):
    r'(float|int)?\(t.value\)|t.value'
    return t

def t_FSTR(t):
    r'f(\".+\"|\'.+\')'
    return t
def t_LBUILD(t):
    r'lex.lex\(\)'
    return t

def t_ID(t):
    r'[a-zA-Z]([a-zA-Z_]|\d)*'
    return t


t_ignore = " \t\n"




def t_error(t):
    print("Illegal character", t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()