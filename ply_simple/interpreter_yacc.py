from interpreter_lex import tokens,literals
import ply.yacc as yacc
import sys


def p_begin(p):
    "begin : lexer yacc"

def p_lexer(p):
    "lexer : BEGINL declarations"
    
def p_yacc(p):
    "yacc : BEGINY"
    print("YACC")

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
    "types : REGEXP RETURN '(' PAL ',' TVALUE ')'"
    exp = construct_function(p)
    p.parser.string += exp
    
def construct_function(p):
    func_name = p[4][1:-1]
    exp = f"def t_{func_name}(t):\n\tr'{p[1]}'\n\tt.value = {p[6]}\n\treturn t\n"
    return exp

def p_typeserror(p):
    "types : REGEXP ERROR '(' elem ',' TVALUE ')' "
    exp = construct_error_func(p)
    p.parser.string += exp
    
def construct_error_func(p):
    exp = f"def p_error(t):\n\tprint({p[4]})\n"
    return exp

def p_typesbuild(p):
    "types : ID '=' LBUILD "
    p.parser.string += p[1] + p[2] + p[3] 
    
def check_if_present(p,str):
    tok = str[1:-1]
    if str[1:-1] in p.parser.tokens:
        error("Token already in list!", p)
    p.parser.tokens.append(tok)
    
def p_contentelem(p):
    "content : elem"
    check_if_present(p,p[1])
    p[0] = p[1]

def p_contentelems(p):
    "content : content ',' elem"
    check_if_present(p,p[3])
    p[0] = p[1] + p[2] + p[3]

def p_elem(p):
    "elem : PAL"
    p[0] = p[1]
    
def p_elemSTR(p):
    "elem : STR"
    p[0] = p[1]
    
def p_elemFormat(p):
    "elem : FSTR"
    p[0] = p[1]
    
def error(error,p):
    print(error)
    p.parser.success = False

def p_error(p):
    print("SYNTAX ERROR",p)
    parser.success = False


parser = yacc.yacc()

f = open("test.txt","r")

parser.string = "import ply.yacc as yacc\nimport ply.lex as lex\n"
parser.tokens = []
parser.success = True

content = f.read()
parser.parse(content)
print(parser.tokens)

if parser.success:
    print("Compilation successful!")
    fout = open("out.py","w")
    fout.write(parser.string)
    print(parser.string,end="")

else:
    print("Compilation failed!")






