import ast
import re
from typing import List, Union
import pandas as pd
from kkexpr.expr import calc_expr
from kkdatac import get_price
# Define the get_dependencies function
def get_dependencies(expression: str) -> List[str]:
    # Use regex to find all factor names in the expression
    # Assuming factor names are alphanumeric and may contain underscores
    factor_pattern = re.compile(r'\b[a-zA-Z_]\w*\b')
    matches = factor_pattern.findall(expression)
    # Remove duplicates by converting to a set, then back to a list
    dependencies = list(set(matches))
    return dependencies

# Define the expression_tree function
class ExprNode:
    def __init__(self, value: Union[str, ast.AST], left: 'ExprNode' = None, right: 'ExprNode' = None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        if self.left and self.right:
            return f'({self.left} {self.value} {self.right})'
        return str(self.value)

def expression_tree(expression: str) -> ExprNode:
    # Parse the expression into an abstract syntax tree (AST)
    expr_ast = ast.parse(expression, mode='eval').body

    def build_tree(node: ast.AST) -> ExprNode:
        if isinstance(node, ast.BinOp):
            left = build_tree(node.left)
            right = build_tree(node.right)
            op = type(node.op).__name__
            return ExprNode(op, left, right)
        elif isinstance(node, ast.Name):
            return ExprNode(node.id)
        elif isinstance(node, ast.Constant):
            return ExprNode(node.value)
        elif isinstance(node, ast.UnaryOp):
            operand = build_tree(node.operand)
            op = type(node.op).__name__
            return ExprNode(op, operand)
        elif isinstance(node, ast.Call):
            func = node.func.id
            args = [build_tree(arg) for arg in node.args]
            return ExprNode(func, *args)
        else:
            raise TypeError(f'Unsupported AST node type: {type(node)}')

    return build_tree(expr_ast)

class Factor:
    def __init__(self, expression: str):
        self.expression = expression
        self.dependencies = get_dependencies(expression)
        self.expr = expression_tree(expression)

    def __repr__(self):
        return self.expression
    
    def __str__(self):
        return self.expression
    
    def __add__(self, other):
        if isinstance(other, Factor):
            return Factor(f'({self} + {other})')
        return Factor(f'({self} + {other})')
    
    def __sub__(self, other):
        if isinstance(other, Factor):
            return Factor(f'({self} - {other})')
        return Factor(f'({self} - {other})')
    
    def __mul__(self, other):
        if isinstance(other, Factor):
            return Factor(f'({self} * {other})')
        return Factor(f'({self} * {other})')
    
    def __truediv__(self, other):
        if isinstance(other, Factor):
            return Factor(f'({self} / {other})')
        return Factor(f'({self} / {other})')

    def __pow__(self, other):
        if isinstance(other, Factor):
            return Factor(f'({self} ** {other})')
        return Factor(f'({self} ** {other})')

    def get_dependencies(self, expression: str) -> List[str]:
        return get_dependencies(expression)
    
    def expression_tree(self, expression: str):
        return expression_tree(expression)
    
    @staticmethod
    def execute_factor(factor, order_book_ids, start_date, end_date):
        df = get_price(order_book_ids, start_date, end_date)
        return calc_expr(df, Factor.expression)

if __name__ == '__main__':
    # Predefined factors
    open_factor = Factor('open')
    close_factor = Factor('close')
    high_factor = Factor('high')
    low_factor = Factor('low')

    # Example usage
    f = (close_factor - open_factor) / (high_factor - low_factor)

    # Execute the factor calculation
    result = Factor.execute_factor(f, ['000001.XSHE', '600000.XSHG'], '2022-01-01', '2022-12-31')
    print(result)