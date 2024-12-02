import pandas as pd
import logging
from typing import Optional
from kkexpr.expr_functions import *

logger = logging.getLogger(__name__)

def expr_transform(df: pd.DataFrame, expr: str) -> str:
    """Transform column names in expression to DataFrame references."""
    for col in df.columns:
        expr = expr.replace(col, f'df["{col}"]')
    return expr

def calc_expr(df: pd.DataFrame, expr: str) -> Optional[pd.Series]:
    """
    Calculate expression using DataFrame columns.
    
    Args:
        df: Input DataFrame
        expr: Expression string to evaluate
        
    Returns:
        Calculated Series or None if evaluation fails
        
    Raises:
        ValueError: If expression is invalid
    """
    # Return existing column directly
    if expr in df.columns:
        return df[expr]
        
    try:
        transformed_expr = expr_transform(df, expr)
        result = eval(transformed_expr)
        return result
        
    except Exception as e:
        logger.error(f"Failed to evaluate expression '{expr}': {str(e)}")
        raise ValueError(f"Invalid expression: {expr}") from e
