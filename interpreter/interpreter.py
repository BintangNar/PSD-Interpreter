# CONSTANTS
DIGITS = '0123456789'

# ERROR
class errors:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        return f'{self.error_name}: {self.details}'

class illegalChar(errors):
    def __init__(self, details):
        super().__init__('Illegal Character Detected', details)

# TOKENS
TT_INT = 'TT_INT'
TT_FLOAT = 'TT_FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MOD = 'MOD'

class token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

# LEXER
class lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def tokenCreate(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
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
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                char = self.current_char
                self.advance()
                return [], illegalChar("'" + char + "' is not listed")
            
        return tokens, None
    
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
            
# Program Run
def run(text):
    lex = lexer(text)  
    tokens, error = lex.tokenCreate()

    return tokens, error
