import ply.yacc as yacc
from jit_lexer import *

class Parser():

    def p_statement(self, p):
        '''statement : variable_decl
                      | function_call'''

    def p_variable_decl(self, p):
        '''variable_decl : type ID EQUALS expression
                         | ID EQUALS expression
                         | type ID'''
                         
    def p_function_call(self, p):
        '''function_call : fun LPAREN parameters RPAREN'''

    def p_fun(self, p):
        '''fun : SAY
                | LISTEN
                | IMPORT
                | SAVE
                | GET
                | PUSH
                | PULL
                | SEARCH'''

    def p_parameters(self, p):
        '''parameters : empty
                     | parameter COMMA parameters
                     | parameter'''

    def p_parameter(self, p):
        '''parameter : ID
                    | STRING_s
                    | ID EQUALS expression'''
    
    
    def p_type(self, p):
        '''type : STRING
                | BOOLEAN
                | INT
                | NODE
                | LIST
                | GRAPH'''

    def p_expression(self, p):
        '''expression : arithmetic_expr
                      | function_call
                      | STRING_s
                      | BOOLEAN_s'''

    def p_arithmetic_expr(self, p):
        '''arithmetic_expr : arithmetic_expr '+' term
                           | arithmetic_expr '-' term
                           | term'''

    def p_empty(self, p):
        'empty :'
        pass

    def p_term(self, p):
        '''term : term '*' factor
                | term '/' factor
                | factor'''

    def p_factor(self, p):
        '''factor : LPAREN arithmetic_expr RPAREN
                  | ID
                  | NUM'''

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)

    def __init__(self):
        lexer = Lexer()
        self.tokens = tokens = lexer.tokens
        
        self.parser = yacc.yacc(module=self)