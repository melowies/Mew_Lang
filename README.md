# Mew Language Calculator

This is a simple calculator program built using Python's Tkinter library. It's designed to parse and evaluate basic arithmetic expressions in a custom syntax.

## Features

- Supports addition (+), subtraction (-), multiplication (*), and division (/) operations.
- Handles integer and floating-point numbers.
- Parses expressions enclosed within parentheses.
- Provides error handling for illegal characters, incorrect expressions, and missing '|' at the end of expressions.
- Displays parsed tokens and the result of the calculation.

## Usage

1. Clone the repository to your local machine.
2. Make sure you have Python installed.
3. Run the `main.py` file using Python.
4. Enter the expression in the input field and click the "Calculate" button.
5. View the result and parsed tokens in their respective fields.

## Example Expressions

- `1+2*3`: Evaluates to `7`.
- `10 / (2 + 3)`: Evaluates to `2.0`.
- `5.5 * (4 - 2.5)`: Evaluates to `11.0`.

## Custom Syntax

- `&`: Addition operator.
- `%`: Subtraction operator.
- `#`: Multiplication operator.
- `!`: Division operator.
- `(` and `)`: Enclose expressions to define precedence.

## Notes

- Ensure that each expression ends with the '|' symbol to indicate the end of the input.
- Only one dot (.) is allowed in floating-point numbers.
- Spaces and tabs are ignored.
