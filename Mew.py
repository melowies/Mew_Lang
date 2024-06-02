import tkinter as tk
from tkinter import messagebox

# CONSTANTS
NUMERIC_DIGITS = '0123456789'

class Position:
    def __init__(self, index, line_number, column_number):
        self.index = index
        self.line_number = line_number
        self.column_number = column_number

    def advance(self, current_character=None):
        self.index += 1
        self.column_number += 1
        if current_character == '\n':
            self.line_number += 1
            self.column_number = 0

    def copy(self):
        return Position(self.index, self.line_number, self.column_number)
    
# ERRORS
class Error:
    def __init__(self, error_name, details, start_position, end_position):
        self.error_name = error_name
        self.details = details
        self.start_position = start_position
        self.end_position = end_position

    def as_string(self):
        return f'{self.error_name}: {self.details}'

class IllegalCharError(Error):
    def __init__(self, details, start_position, end_position):
        super().__init__('Illegal Character', details, start_position, end_position)

class DotError(Error):
    def __init__(self, details, start_position, end_position):
        super().__init__('Float numbers cannot have multiple dots', details, start_position, end_position)

class WrongEndError(Error):
    def __init__(self, details, start_position, end_position):
        super().__init__('The expressions must end with "|" symbol', details, start_position, end_position)

# TOKENS
class TokenType:
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    LEFT_PARENTHESIS = 'LEFT_PARENTHESIS'
    RIGHT_PARENTHESIS = 'RIGHT_PARENTHESIS'
    END_SYMBOL = 'END_SYMBOL'

class Token:
    def __init__(self, type_, value=None, start_position=None, end_position=None):
        self.type = type_
        self.value = value
        if start_position:
            self.start_position = start_position.copy()
            self.end_position = start_position.copy()
            self.end_position.advance()
        if end_position:
            self.end_position = end_position.copy()

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

# LEXEME
class Lexeme:
    def __init__(self, text):
        self.text = text
        self.position = Position(-1, 0, -1)
        self.current_character = None
        self.advance()

    def advance(self):
        self.position.advance(self.current_character)
        self.current_character = self.text[self.position.index] if self.position.index < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_character is not None:
            if self.current_character in ' \t':
                self.advance()
            elif self.current_character in NUMERIC_DIGITS:
                tokens.append(self.make_number())
            elif self.current_character == '&':
                tokens.append(Token(TokenType.PLUS, start_position=self.position))
                self.advance()
            elif self.current_character == '%':
                tokens.append(Token(TokenType.MINUS, start_position=self.position))
                self.advance()
            elif self.current_character == '#':
                tokens.append(Token(TokenType.MULTIPLY, start_position=self.position))
                self.advance()
            elif self.current_character == '!':
                tokens.append(Token(TokenType.DIVIDE, start_position=self.position))
                self.advance()
            elif self.current_character == '(':
                tokens.append(Token(TokenType.LEFT_PARENTHESIS, start_position=self.position))
                self.advance()
            elif self.current_character == ')':
                tokens.append(Token(TokenType.RIGHT_PARENTHESIS, start_position=self.position))
                self.advance()
            elif self.current_character == '.':
                start_position = self.position.copy()
                character = self.current_character
                self.advance()
                return [], DotError("'" + character + "'", start_position, self.position)
            elif self.current_character == '|':
                tokens.append(Token(TokenType.END_SYMBOL, start_position=self.position))
                self.advance()
                break
            else:
                start_position = self.position.copy()
                character = self.current_character
                self.advance()
                return [], IllegalCharError("'" + character + "'", start_position, self.position)
            
        if len(self.text) == 0 or self.text[-1] != '|':
            start_position = self.position.copy()
            end_position = self.position.copy()
            return [], WrongEndError("You should add '|' at the end of your expression.", start_position, end_position)

        return tokens, None

    def make_number(self):
        number_string = ''
        dot_count = 0
        start_position = self.position.copy()

        while self.current_character is not None and (self.current_character in NUMERIC_DIGITS or (dot_count == 0 and self.current_character == '.')):
            if self.current_character == '.':
                if dot_count > 1:
                    Lexeme.make_number(self.current_character)
                dot_count += 1
                number_string += '.'
            else:
                number_string += self.current_character
            self.advance()

        if dot_count == 0:
            return Token(TokenType.INTEGER, int(number_string), start_position, self.position)
        else:
            return Token(TokenType.FLOAT, float(number_string), start_position, self.position)

# PARSER
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]

    def factor(self):
        token = self.current_token
        if token.type in (TokenType.INTEGER, TokenType.FLOAT):
            self.advance()
            return token.value
        elif token.type == TokenType.LEFT_PARENTHESIS:
            self.advance()
            result = self.expr()
            if self.current_token.type == TokenType.RIGHT_PARENTHESIS:
                self.advance()
                return result

    def term(self):
        result = self.factor()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.advance()
                result *= self.factor()
            elif token.type == TokenType.DIVIDE:
                self.advance()
                result /= self.factor()

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.advance()
                result += self.term()
            elif token.type == TokenType.MINUS:
                self.advance()
                result -= self.term()

        return result

    def parse(self):
        result = self.expr()
        if self.current_token.type != TokenType.END_SYMBOL:
            raise Exception("Expected END_SYMBOL at the end of the expression")
        return result

# RUN
def run_calculator(text):
    lexeme = Lexeme(text)
    tokens, error = lexeme.make_tokens()
    if error:
        return None, tokens, None, error

    parser = Parser(tokens)
    try:
        result = parser.parse()
        result_type = TokenType.INTEGER if isinstance(result, int) else TokenType.FLOAT
        return result, tokens, result_type, None
    except Exception as e:
        return None, tokens, None, Error("Parsing Error", str(e), None, None)

# MAIN
def main():
    root = tk.Tk()
    root.title("Mew Language Calculator")

    def on_calculate():
        text = input_field.get()
        result, tokens, result_type, error = run_calculator(text)

        if error:
            messagebox.showerror("Error", error.as_string())
            return

        result_field.config(state=tk.NORMAL)
        result_field.delete(1.0, tk.END)
        result_field.insert(tk.END, f"Result: {result} ({result_type})")
        result_field.config(state=tk.DISABLED)

        tokens_field.config(state=tk.NORMAL)
        tokens_field.delete(1.0, tk.END)
        for token in tokens:
            tokens_field.insert(tk.END, f"{token}\n")
        tokens_field.config(state=tk.DISABLED)

    frame = tk.Frame(root)
    frame.pack(pady=20)

    input_label = tk.Label(frame, text="Enter expression:")
    input_label.grid(row=0, column=0, padx=10)

    input_field = tk.Entry(frame, width=50)
    input_field.grid(row=0, column=1, padx=10)

    calculate_button = tk.Button(frame, text="Calculate", command=on_calculate)
    calculate_button.grid(row=0, column=2, padx=10)

    result_label = tk.Label(frame, text="Result:")
    result_label.grid(row=1, column=0, padx=10)

    result_field = tk.Text(frame, height=2, width=50, state=tk.DISABLED)
    result_field.grid(row=1, column=1, padx=10)

    tokens_label = tk.Label(frame, text="Tokens:")
    tokens_label.grid(row=2, column=0, padx=10)

    tokens_field = tk.Text(frame, height=10, width=50, state=tk.DISABLED)
    tokens_field.grid(row=2, column=1, padx=10)

    root.mainloop()

if __name__ == '__main__':
    main()
