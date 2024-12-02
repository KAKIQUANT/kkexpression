import ast
import re
from typing import List, Union, Optional
import pandas as pd
from datetime import datetime
from kkexpr.core.engine import calc_expr
from kkdatac import get_price
from kkexpr.utils import validate_date, validate_symbols
from kkexpr.expr.functions import *

class ExprNode:
    """Node in expression parse tree."""
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def evaluate(self, data):
        evaluated_args = [arg.evaluate(data) if isinstance(arg, ExprNode) else arg for arg in self.args]
        return self.func(*evaluated_args)

    def __repr__(self):
        if self.left and self.right:
            return f'({self.left} {self.value} {self.right})'
        return str(self.value)

class Factor:
    """
    A class representing a financial factor with expression evaluation capabilities.
    """
    
    def __init__(self, expression: str):
        """
        Initialize Factor with an expression.
        
        Args:
            expression: Factor calculation expression
        """
        self.expression = expression
        self.dependencies = self._get_dependencies()
        self.expr = self._build_expression_tree()

    def _get_dependencies(self) -> List[str]:
        """Get list of factor dependencies from expression."""
        factor_pattern = re.compile(r'\b[a-zA-Z_]\w*\b')
        matches = factor_pattern.findall(self.expression)
        return list(set(matches))

    def _build_expression_tree(self) -> ExprNode:
        """Build expression parse tree."""
        try:
            expr_ast = ast.parse(self.expression, mode='eval').body
            
            def build_tree(node):
                try:
                    if isinstance(node, ast.BinOp):
                        func = get_func(node)
                        return ExprNode(func, build_tree(node.left), build_tree(node.right))
                    elif isinstance(node, ast.Call):
                        func = get_func(node)
                        args = [build_tree(arg) for arg in node.args]
                        return ExprNode(func, *args)
                    elif isinstance(node, (ast.Name, ast.Constant)):
                        func = get_func(node)
                        return ExprNode(func)
                    else:
                        raise TypeError(f'Unsupported AST node type: {type(node)}')
                except Exception as e:
                    raise ValueError(f"Invalid expression part: {ast.dump(node)}") from e
                    
            return build_tree(expr_ast)
        except Exception as e:
            raise ValueError(f"Invalid expression: {self.expression}") from e

    def execute(self, 
                order_book_ids: List[str],
                frequency: str,
                start_date: Union[str, datetime],
                end_date: Union[str, datetime]) -> pd.Series:
        """Execute factor calculation."""
        validate_symbols(order_book_ids)
        validate_date(start_date)
        validate_date(end_date)
        
        df = get_price(
            order_book_ids=order_book_ids,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date
        )
        
        if df is None or df.empty:
            raise ValueError("No data returned from get_price")
        
        return calc_expr(df, self.expression)

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

def get_func(node):
    """Get function from AST node."""
    if isinstance(node, ast.BinOp):
        op_map = {
            ast.Add: lambda x, y: x + y,
            ast.Sub: lambda x, y: x - y,
            ast.Mult: lambda x, y: x * y,
            ast.Div: lambda x, y: x / y,
            ast.Pow: lambda x, y: x ** y,
        }
        return op_map[type(node.op)]
    elif isinstance(node, ast.Name):
        return lambda x: x[node.id]
    elif isinstance(node, ast.Constant):
        return lambda: node.value
    elif isinstance(node, ast.Call):
        return globals()[node.func.id]
    else:
        raise TypeError(f'Unsupported AST node type: {type(node)}')
        raise TypeError(f'Unsupported AST node type: {type(node)}')