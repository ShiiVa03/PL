import ply.lex as lex
import re

tokens = ["BEGINL","STR","LITERAL","IGNORE","TOKENS","PAL","COMMENT","RETURN","REGEXP",
          "ERROR","FSTR", "ID","LBUILD","BEGINY","PRECEDENCE", "PRETYPES","LIT","CODE", "END"]
literals = ["%","=","[","]",",","(",")",":","{","}","-"]


def t_CODE(t):
    r'\{(.|\s)*?(?<!\\)}'
    t.value = t.value[1:-1].strip(' ').replace(r'\}', '}')
    return t

def t_BEGINL(t):
    r'%%lexer'
    return t

def t_BEGINY(t):
    r'%%yacc'
    return t

def t_END(t):
    r'%%\s*(.|\s)*'
    t.value = t.value.lstrip('% \n')
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

def t_PRECEDENCE(t):
    r'%precedence'
    t.value = t.value[1:]
    return t
    
def t_RETURN(t):
    r'return'
    return t

def t_ERROR(t):
    r'error'
    return t

def t_PRETYPES(t):
    r'\'(left|right|nonassoc)\''
    return t

def t_LBUILD(t):
    r'lex.lex\(\)'
    return t

def t_COMMENT(t):
    r'(\#)?\#.*'
    return t

def t_LIT(t):
    r'\'.+?\''
    return t

def t_STR(t):
    r'\"[^\"]+\"'
    return t

def t_PAL(t):
    r'\'\w+\''
    return t

def t_REGEXP(t):
    r'\/.*?(?<!\\)\/'
    t.value = t.value.replace(r'\/', r'/')[1:-1]
    return t    

def t_FSTR(t):
    r'f(\".+?\"|\'.+?\')'
    t.value = t.value[1:]
    return t

def t_ID(t):
    r'[a-zA-Z]([a-zA-Z_]|\d)*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = " \t"

def t_error(t):
    print("Illegal character", t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()
