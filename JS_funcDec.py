import ply.lex as lex
import ply.yacc as yacc

# Define tokens
tokens = (
    'FUNCTION', 'LPAR', 'RPAR', 'LCURL', 'RCURL','MINUS',
    'COMMA', 'VAR', 'EQUALS', 'TRUE', 'FALSE', 'RETURN','LET',
    'IDENTIFIER', 'NUMBER', 'STRING', 'SEMICOLON', 'PLUS','CONST'
)

t_LPAR = r'\('
t_RPAR = r'\)'
t_LCURL = r'\{'
t_RCURL = r'\}'
t_COMMA = r','
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_SEMICOLON = r';'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9]*'
t_NUMBER = r'[0-9]+'

def t_FUNCTION(t):
    r'function'
    t.type = 'FUNCTION'
    return t

def t_VAR(t):
    r'var'
    t.type = 'VAR'
    return t

def t_LET(t):
    r'let'
    t.type = 'LET'
    return t

def t_CONST(t):
    r'const'
    t.type = 'CONST'
    return t

def t_TRUE(t):
    r'true'
    t.type = 'TRUE'
    return t

def t_FALSE(t):
    r'false'
    t.type = 'FALSE'
    return t

def t_RETURN(t):
    r'return'
    t.type = 'RETURN'
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Define precedence


# Define parsing rules

def p_function_declaration(p):
    '''
    function_declaration : FUNCTION IDENTIFIER LPAR parameter_list RPAR LCURL statements RCURL
    '''
    p[0] = ('function-declaration', p[2], p[4], p[7])

def p_parameter_list(p):
    '''
    parameter_list : IDENTIFIER
                  | IDENTIFIER COMMA parameter_list
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_statements(p):
    '''
    statements : statement
               | statement statements
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_statement(p):
    '''
    statement : expression SEMICOLON
             | return_statement SEMICOLON
    '''
    p[0] = p[1]

def p_return_statement(p):
    '''
    return_statement : RETURN expression
    '''
    p[0] = ('return', p[2])

def p_expression_assignment(p):
    '''
    expression : VAR IDENTIFIER EQUALS expression
                | LET IDENTIFIER EQUALS expression
                | CONST IDENTIFIER EQUALS expression
    '''
    p[0] = ('assignment', p[2], p[4])

def p_expression_identifier(p):
    '''
    expression : IDENTIFIER
    '''
    p[0] = p[1]

def p_expression_number(p):
    '''
    expression : NUMBER
    '''
    p[0] = ('number', p[1])

def p_expression_string(p):
    '''
    expression : STRING
    '''
    p[0] = ('string', p[1])

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

input_code = '''
function add(x, y, z){
    var x = "statement1";
    let y = "statement2";
    return 1;
}
'''

lexer.input(input_code)

result = parser.parse(input_code)
print(result)
