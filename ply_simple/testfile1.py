import ply.yacc as yacc
import ply.lex as lex
literals=["+","*","-","/",]
t_ignore="ola"
def t_VAR(t):
  r'[a-zA-Z][a-zA-Z0-9]*'
  t.value = float(t.value)
  return t

def t_NUMBER(t):
  r'(\d+)'
  float(t.value)
  return t

def t_error(t):
  print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
  t.lexer.skip(1)

states=(("comment",'exclusive'),
  ("state",'inclusive'))
tokens=['VAR',"NUMBER"]
lexer=lex.lex()
ts = {}
x = []
precedence=(
  ('left',"VAR"),
  ('right',"NUMBER")
  )

def p_statfirst1(p):
  "stat :  NUMBER '+' stat"
  global ts
  global x
  print(p[1], p[3])


def p_statfirst2(p):
  "stat :  NUMBER '-' stat"
  global ts
  global x
  print(p[1], p[3])


def p_statfirst3(p):
  "stat :  NUMBER '/' stat"
  global ts
  global x
  print(p[1], p[3])


def p_statfirst4(p):
  "stat :  NUMBER '*' stat"
  global ts
  global x
  print(p[1], p[3])


def p_stat(p):
  "stat :  NUMBER"
  global ts
  global x
  print(p[1])

def p_error(p):
	if p:
		print("Syntax error at token", p.type)
	else:
		print("Syntax error at EOF")
	exit()
	
def getval(n):
	if n not in ts: print(f"Undefined name ’{n}’")
	return ts.get(n,0)
y=yacc.yacc()
y.parse("3+4*7")
