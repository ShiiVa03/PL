from interpreter_lex import tokens,literals
import ply.yacc as yacc
import sys


def p_begin(p):
    "begin : lexer yacc"

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
    "types : REGEXP RETURN '(' elem ',' TVALUE ')'"
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
    exp = f"def p_error(t):\n\tprint(f{p[4]})\n"
    return exp

def p_typesbuild(p):
    "types : ID '=' LBUILD "
    p.parser.string += p[1] + p[2] + p[3] + "\n"
    
def check_if_present(p,str):
    tok = str[1:-1]
    if tok in p.parser.tokens:
        error("Token already in list!", p)
    else:
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

def p_yacc(p):
    "yacc : BEGINY yaccdecs"
    
def p_yaccdecs(p):
    "yaccdecs : yaccdecs yaccdec"

def p_yaccdecconly(p):
    "yaccdecs : yaccdec"
    
def p_yaccdec(p):
    "yaccdec : yacctype"

def p_yacctype(p):
    "yacctype : PRECEDENCE '=' '[' tuples ']'"
    p.parser.string += p[1] + p[2] + "(\n\t" + p[4] + "\n\t)\n"

def p_yacctypecomment(p):
    "yacctype : COMMENT"


#TODO MAKE ATRIBS RECEIVE MORE THAT ELEM
def p_yacctypeatribs(p):
    "yacctype : ID '=' elem "
    p.parser.atribs[p[1]] = p[3]    

def p_yacctypegrammar(p):
    "yacctype : ID ':' gramcontents '{' '}' '-' ID"
    p.parser.string += construct_grammar_func(p)

def construct_grammar_func(p):
    func_name = p[7]
    exp = f"def p_{func_name}(p):\n\t\"{p[1]} ':' {p[3]}\"\n\n"
    return exp
    
def p_gramcontentsonly(p):
    "gramcontents : gramcontent"
    
    
def p_gramcontents(p):
    "gramcontents : gramcontents gramcontent"
    
def p_gramcontent(p):
    "gramcontent : LIT"

def p_gramcontentw(p):
    "gramcontent : ID"


def p_tuples(p):
    "tuples : tuples ',' tuple"
    p[0] = p[1] + p[2] + "\n\t" + p[3]

def p_tuplesone(p):
    "tuples : tuple"
    p[0] = p[1] 
    
def p_tuple(p):
    "tuple : '(' PRETYPES ',' tupelems ')'"
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

def p_tupelem(p):
    "tupelems : elem"
    if p[1][1:-1] not in p.parser.tokens:
        error("Token not in previous defined tokens!!!",p)
        raise SyntaxError
    
    p[0] = p[1]

def p_tupeelems(p):
    "tupelems : tupelems ',' elem"
    if p[3][1:-1] not in p.parser.tokens:
        error("Token not in previous defined tokens!!!",p)
        raise SyntaxError
    p[0] = p[1] + p[2] + p[3]

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
parser.atribs = {}


content = f.read()
parser.parse(content)
print(parser.tokens)
print(parser.atribs)

if parser.success:
    print("Compilation successful!")
    fout = open("out.py","w")
    fout.write(parser.string)
    print(parser.string,end="")

else:
    print("Compilation failed!")
