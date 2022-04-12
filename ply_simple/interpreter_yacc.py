from interpreter_lex import tokens,literals
import ply.yacc as yacc
import sys


def p_begin(p):
    "begin : lexer"

def p_lexer(p):
    "lexer : BEGINL declarations"

def p_declarations(p):
    "declarations : declarations declaration"

def p_declarationsstop(p):
    "declarations : declaration"

def p_declaration(p):
    "declaration : types commentlex"

def p_commentlexempty(p):
    "commentlex : "

def p_commentlex(p):
    "commentlex : COMMENT"
    
def p_typesliteral(p):
    "types :  LITERAL '=' STR"
    p.parser.string += p[1] + p[2] + p[3] + "\n"

def p_typesignores(p):
    "types :  IGNORE '=' STR"
    p.parser.string += p[1] + p[2] + p[3] + "\n"
    
def p_typestokens(p):
    "types :  TOKENS '=' '[' content ']'"
    p.parser.string += p[1] + p[2] + p[3] + p[4] + p[5] +"\n"

def p_typesreturn(p):
    "types : REGEXP RETURN"
    exp = "r'" + p[1] +"'"+ p[2]+ "\n"
    p.parser.string += exp
    
def p_contentelem(p):
    "content : elem"
    p[0] = p[1]

def p_contentelems(p):
    "content : content ',' elem"
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