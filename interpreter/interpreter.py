# CONSTANTS
DIGITS = '0123456789'
# LETTERS = string.ascii_letters
# LETTERS_DIGITS = LETTERS + DIGITS

# ERROR
class errors:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        return f'{self.error_name}: {self.details}\n'

class illegalChar(errors):
    def __init__(self, details):
        super().__init__('Illegal Character Detected', details)

class InvalidSyntax(errors):
    def __init__(self, details):
        super().__init__('Invalid syntax Detected', details)

# TOKENS
TT_INT = 'TT_INT'
TT_FLOAT = 'TT_FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MOD = 'MOD'
TT_NEWLINE = 'NEWLINE'
TT_EOF = 'EOF'
TT_PRINT = 'PRINT'
TT_STRING = 'STRING'
TT_CONVERTBINARY = 'CONVERTBINARY'
TT_CONVERTOCTAN = 'CONVERTOCTAN'
TT_CONVERTHEXADEC = 'CONVERTHEXADEC'
TT_IDENTIFIER = 'IDENTIFIER'

class token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

# LEXER
class lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = -1
        self.current_char = None
        self.keywords = {
            "binaire": TT_CONVERTBINARY,
            "octale": TT_CONVERTOCTAN,
            "hexadecimale": TT_CONVERTHEXADEC,
            "imprimer": TT_PRINT,
            # Add more keywords as needed
        }
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def tokenCreate(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '\n':
                tokens.append(token('NEWLINE'))
                self.advance()
            elif self.current_char == '+':
                tokens.append(token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(token(TT_DIV))
                self.advance()
            elif self.current_char == '%':
                tokens.append(token(TT_MOD))
                self.advance()
            elif self.current_char.isalpha():
                keyword_str = self.make_identifier()
                if keyword_str in self.keywords:
                    tokens.append(token(self.keywords[keyword_str]))  
                else:
                    tokens.append(token(TT_IDENTIFIER, keyword_str))
            elif self.current_char == '"':
                tokens.append(self.make_string())  
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                char = self.current_char
                self.advance()
                return [], illegalChar("'" + char + "' is not listed")
        
        tokens.append(token('EOF'))    
        return tokens, None
    
    def make_identifier(self):
        identifier_str = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier_str += self.current_char
            self.advance()
        return identifier_str
    
    def make_string(self):
        string_value = ''
        quote_type = self.current_char
        self.advance()

        while self.current_char is not None and self.current_char != quote_type:
            string_value += self.current_char
            self.advance()
        self.advance()
        return token(TT_STRING, string_value)
    
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: 
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        
        if dot_count == 0:
            return token(TT_INT, int(num_str))
        else:
            return token(TT_FLOAT, float(num_str))

########################        
# PARSER
########################
#NODES
class NumberNode:
    def __init__(self, tok):
        self.tok = tok
    def __repr__(self):
        return f'{self.tok}'

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    
    def __repr__(self):
        return f'({self.left_node},{self.op_tok},{self.right_node})'

class PrintNode:
    def __init__(self,value_node):
        self.value_node = value_node

class StringNode:
    def __init__(self,tok):
        self.tok = tok
    def __repr__(self):
        return f'{self.tok}'

# PARSER
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()
    
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def parse_statement(self):
        statements = []
        while self.current_tok.type != 'EOF':
            if self.current_tok.type == 'NEWLINE':
               self.advance()
            elif self.current_tok.type == TT_PRINT:
                self.advance()
                statements.append(PrintNode(self.expr()))
            else:
               statements.append(self.expr())
               if self.current_tok.type == 'NEWLINE':
                   self.advance()
        return statements

    def parse(self):
        return self.parse_statement()

    def factor(self):
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)
        if tok.type == TT_CONVERTBINARY:
            self.advance()
            node = self.factor()
            return ConversionNode(tok, node, base=2)

        elif tok.type == TT_CONVERTOCTAN:
            self.advance()
            node = self.factor()
            return ConversionNode(tok, node, base=8)

        elif tok.type == TT_CONVERTHEXADEC:
            self.advance()
            node = self.factor()
            return ConversionNode(tok, node, base=16)
        
        elif tok.type == TT_STRING:
            self.advance()
            return StringNode(tok)

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
        
    def bin_op(self, func, ops):
        left = func()

        while self.current_tok is not None and self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left = BinOpNode(left, op_tok, right)
        return left

#CONVERT
class ConversionNode:
    def __init__(self, token, number_node, base):
        self.token = token
        self.number_node = number_node
        self.base = base

    
#####################
#INTERPRETER            
#####################
class interpreter:
    def visit(self,node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)
    
    def no_visit_method(self,node):
        raise Exception(f'No Visit_{type(node).__name__}method defined')
    
    def visit_NumberNode(self,node):
        return node.tok.value
    
    def visit_BinOpNode(self,node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op_tok.type == TT_PLUS:
            return left + right
        elif node.op_tok.type == TT_MINUS:
            return left - right
        elif node.op_tok.type == TT_MUL:
            return left * right
        elif node.op_tok.type == TT_DIV:
            if right == 0:
                raise Exception("Division by 0 is not available")
            return left / right
        elif node.op_tok.type == TT_MOD:
            return left % right
        
    def visit_ConversionNode(self, node):
        number = self.visit(node.number_node)  # Get the number to convert

        if node.base == 2:
            return bin(int(number))[2:]  # Convert to binary without '0b' prefix
        elif node.base == 8:
            return oct(int(number))[2:]  # Convert to octal without '0o' prefix
        elif node.base == 16:
            return hex(int(number))[2:]  # Convert to hexadecimal without '0x' prefix
        else:
            raise ValueError(f"Unknown base: {node.base}")
    
    def visit_StringNode(self,node):
        return node.tok.value
    
    def visit_PrintNode(self,node):
        value = self.visit(node.value_node)
        print(value)
        return value

# Program Run
# Program Run
# Program Run
def run(text):
    lex = lexer('<stdin>', text) 
    tokens, error = lex.tokenCreate()
    if error: 
        print(error.as_string())
        return None, error  # Explicitly return error tuple if there's a lexer error

    # Parse multiple statements
    parser = Parser(tokens)
    statements = parser.parse()
    
    # Interpret each statement
    Interpreter = interpreter()
    for statement in statements:
        if statement:
            Interpreter.visit(statement)  # Removed extra print
            
    return None, None  # Consistent return of tuple
