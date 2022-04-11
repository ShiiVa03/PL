from interpreter_lex import tokens,literals
import ply.yacc as yacc
import sys


def p_Inicio(p):
    "Inicio : Lexer"

def p_Lexer(p):
    "Lexer : BEGINL Declaracoes"

def p_declaracoes(p):
    "Declaracoes : Declaracoes declaracao"

def p_declaracoesstop(p):
    "Declaracoes : declaracao"

def p_declaracao(p):
    "declaracao : Types"

def p_typesliteral(p):
    "Types : LITERAL '=' STR"
    p.parser.string += p[1] + p[2] + p[3] + "\n"

def p_typesignores(p):
    "Types : IGNORE '=' STR"
    p.parser.string += p[1] + p[2] + p[3] + "\n"
    
def p_typestokens(p):
    "Types : TOKENS '=' '[' Conteudo ']'"
    p.parser.string += p[1] + p[2] + p[3] + p[4] + p[5] +"\n"
    
def p_conteudoelem(p):
    "Conteudo : elem"
    p[0] = p[1]

def p_conteudoelems(p):
    "Conteudo : Conteudo ',' elem"
    p[0] = p[1] + p[2] + p[3]

def p_elem(p):
    "elem : PAL"
    p[0] = p[1]
    
def p_elemSTR(p):
    "elem : STR"
    p[0] = p[1]
    

parser = yacc.yacc()
parser.string = "import ply.yacc as yacc\nimport ply.lex as lex\n"


f = open("test.txt","r")
fout = open("out.py","w")

content = f.read()
parser.parse(content)
print(parser.string,end="")

fout.write(parser.string)