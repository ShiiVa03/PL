import ply.lex as lex
import re

tokens = ["BEGINL","STR","LITERAL","IGNORE","TOKENS","PAL"]
literals = ["%","=","[","]",","]

def t_BEGINL(t):
    r'--lexer'
    return t

def t_STR(t):
    r'\"([^"])*\"'
    return t
def t_LITERAL(t):
    r'literals'
    return t
def t_IGNORE(t):
    r'ignore'
    return t
def t_TOKENS(t):
    r'tokens'
    return t
def t_PAL(t):
    r'\'\w+\''
    return t

t_ignore = " \t\n"

def t_error(t):
    print("Illegal character", t.value[0])
    t.lexer.skip(1)
    
lexer = lex.lex()