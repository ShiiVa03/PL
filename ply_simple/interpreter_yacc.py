from interpreter_lex import tokens,literals
import ply.yacc as yacc

def p_begin(p):
    "begin : lexer yacc end"

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
    exp = construct_literals(p[3])
    p.parser.string += p[1] + p[2] + exp + "\n"
    
def construct_literals(lits):
    result = "["
    lits = lits[1:-1]
    for s in lits:
        result += f'"{s}",'
    result += "]"
    return result 

def p_typesignores(p):
    "types :  IGNORE '=' STR"
    p.parser.string += "t_" + p[1] + p[2] + p[3] + "\n"
    
def p_typestokens(p):
    "types :  TOKENS '=' '[' content ']'"
    p.parser.string += p[1] + p[2] + p[3] + p[4] + p[5] +"\n"

def p_typesreturn(p):
    "types : REGEXP RETURN '(' elem ',' code ')'"
    exp = construct_function(p)
    p.parser.string += exp
    
def construct_function(p):
    func_name = p[4][1:-1]
    p[6] = p[6].replace('\n', '\n  ').replace('\t', '  ')
    exp = f"def t_{func_name}(t):\n  r'{p[1]}'\n" 
    code = f"  {p[6]}\n  " 
    ret = "return t\n\n"
    return exp + "  " + ret if not p[6] else exp + code + ret

def p_code(p):
    "code : CODE"
    p[0] = p[1]

def p_code_empty(p):
    "code : "
    p[0] = ""

def p_typeserror(p):
    "types : ERROR '(' elem ',' code ')' "
    exp = construct_error_func(p)
    p.parser.string += exp
    
def construct_error_func(p):
    p[5] = p[5].replace('\n', '\n  ').replace('\t', '  ')
    exp = f"def t_error(t):\n  print(f{p[3]})\n  {p[5]}\n\n"
    return exp

def p_typesbuild(p):
    "types : ID '=' LBUILD "
    p.parser.string += p[1] + p[2] + p[3] + "\n"
    
def p_typesstates(p):
    "types : STATES '=' '(' tupstates ')' "
    p.parser.string += "states" + p[2] + "(" + p[4] + ")" + "\n"
    
def p_tups(p):
    "tupstates : tupstates ',' tup"
    p[0] = p[1] + p[2] + "\n  " + p[3]

def p_tupsones(p):
    "tupstates : tup"
    p[0] = p[1] 
    
def p_tuplex(p):
    "tup : '(' elem ',' STATESTYPES ')'"
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
    
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
    "yacc : BEGINY globals yaccdecs"
    
def p_yaccdecs(p):
    "yaccdecs : yaccdecs yaccdec"

def p_yaccdecconly(p):
    "yaccdecs : yaccdec"
    
def p_yaccdec(p):
    "yaccdec : yacctype"

def p_yacctype(p):
    "yacctype : PRECEDENCE '=' '[' tuples ']'"
    p.parser.string += p[1] + p[2] + "(\n  " + p[4] + "\n  )\n"

def p_yacctypecomment(p):
    "yacctype : COMMENT"
    

def p_yacctypegrammar(p):
    "yacctype : ID ':' gramcontents code '-' ID"
    p.parser.string += construct_grammar_func(p)

def p_end(p):
    "end : END"
    p.parser.string += p[1]

def p_yaccglobals(p):
    "globals : globals global"

def p_yaccglobalsempty(p):
    "globals : "
    
def p_yaccglobal(p):
    "global : ID '=' elem "
    p.parser.string += p[1] + " = " + p[3][1:-1] + "\n" 
    p.parser.atribs.append(p[1]) 


def construct_grammar_func(p):
    func_name = p[6]
    str_globals = '\n  '.join("global " + attr for attr in p.parser.atribs) 
    code = p[4].replace('\t', '  ')
    exp = f'''
def p_{func_name}(p):
  "{p[1]} : {p[3]}"
  {str_globals}
  {code}\n
'''
    return exp
    
def p_gramcontentsonly(p):
    "gramcontents : "
    p[0] = ""    
    
    
def p_gramcontents(p):
    "gramcontents : gramcontents gramcontent"
    p[0] = p[1] + ' ' + p[2]
    
    
def p_gramcontent(p):
    "gramcontent : LIT"
    p[0] = p[1]

def p_gramcontentw(p):
    "gramcontent : ID"
    p[0] = p[1]


def p_tuples(p):
    "tuples : tuples ',' tuple"
    p[0] = p[1] + p[2] + "\n  " + p[3]

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

import sys

if len(sys.argv) == 1 :
    print("Nenhum ficheiro escolhido para compilar")
else :
    print("Compiling: ",sys.argv[1]) 

f = open(sys.argv[1], "r", encoding ='utf8')

parser.string = "import ply.yacc as yacc\nimport ply.lex as lex\n"
parser.tokens = []
parser.success = True
parser.atribs = []


content = f.read()
parser.parse(content)


if parser.success:
    print("Compilation successful!")        
    fout_name = "out.py" if len(sys.argv) == 2 else "" + sys.argv[2]
    fout = open(fout_name, "w", encoding = 'utf8')
    fout.write(parser.string)

else:
    print("Compilation failed!")
