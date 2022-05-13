import ply.yacc as yacc
import ply.lex as lex
tokens=["ID","INT","PRINT","READ","DUMP"]
literals=["+","-","*","/","(",")","=",]
def t_PRINT(t):
  r'print|PRINT'
  return t

def t_READ(t):
  r'read|READ'
  return t

def t_DUMP(t):
  r'dump|DUMP'
  return t

def t_ID(t):
  r'[a-zA-Z_]\w*'
  return t

def t_INT(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_error(t):
  print(f"illegal character")
  t.lexer.skip(1)

t_ignore=" \n\t\r"
lexer=lex.lex()
ids = {}

def p_prog(p):
  "prog :  comandos"
  global ids
  


def p_comandosvazio(p):
  "comandos : "
  global ids
  


def p_co(p):
  "comandos :  comandos comando"
  global ids
  


def p_comando_atrib(p):
  "comando :  ID '=' exp"
  global ids
  ids[p[1]] = p[3]


def p_comando_print(p):
  "comando :  PRINT exp"
  global ids
  print(p[2])


def p_comando_read(p):
  "comando :  READ ID"
  global ids
  
  r = int(input())
  ids[p[2]] = r


def p_comando_dump(p):
  "comando :  DUMP"
  global ids
  print(ids)


def p_exp(p):
  "exp :  aexp"
  global ids
  p[0] = p[1]


def p_aexp_add(p):
  "aexp :  aexp '+' termo"
  global ids
  p[0] = p[1] + p[3]


def p_aexp_minus(p):
  "aexp :  aexp '-' termo"
  global ids
  p[0] = p[1] - p[3]


def p_aexp_termo(p):
  "aexp :  termo"
  global ids
  p[0] = p[1]


def p_termo_mul(p):
  "termo :  termo '*' fator"
  global ids
  p[0] = p[1] * p[3]


def p_termo_div(p):
  "termo :  termo '/' fator"
  global ids
  p[0] = p[1] / p[3]


def p_termo_fator(p):
  "termo :  fator"
  global ids
  p[0] = p[1]


def p_fator_ID(p):
  "fator :  ID"
  global ids
  
  if p[1] in ids:
    p[0] = ids[p[1]]
  else:
    print("Variavél nao definida. Vai ser inicializada a zero")
    p[0] = 0



def p_fator_INT(p):
  "fator :  INT"
  global ids
  p[0] = p[1]


def p_fator_par(p):
  "fator :  '(' aexp ')'"
  global ids
  p[0] = p[2]

parser = yacc.yacc()


import sys 

for line in sys.stdin:
	parser.parse(line)

