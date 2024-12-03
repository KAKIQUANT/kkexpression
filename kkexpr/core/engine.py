import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
from kkexpr.utils import get_logger
from .operators import Operator
from kkexpr.expr.functions import (
    greater, less, cross_up, cross_down,
    correlation, covariance, ma, std,
    ts_max, ts_min, ts_rank, sum, shift, rsi, gt, lt, ge, le
)

logger = get_logger(__name__)

def expr_transform(df: pd.DataFrame, expr: str) -> str:
    """Transform column names in expression to DataFrame references."""
    # Sort columns by length to avoid partial matches
    cols = sorted(df.columns, key=len, reverse=True)
    for col in cols:
        if col == 'pe' or col == 'pb':
            continue
        expr = expr.replace(col, f'df["{col}"]')
    return expr

def calc_expr(df: pd.DataFrame, expr: str) -> pd.DataFrame:
    """Calculate expression using DataFrame."""
    namespace: Dict[str, Any] = {
        'np': np,
        'pd': pd,
        'df': df,
        'log': np.log,
        # Add function references
        'greater': greater,
        'less': less,
        'cross_up': cross_up,
        'cross_down': cross_down,
        'correlation': correlation,
        'covariance': covariance,
        'ma': ma,
        'std': std,
        'ts_max': ts_max,
        'ts_min': ts_min,
        'ts_rank': ts_rank,
        'sum': sum,
        'shift': shift,
        'RSI': rsi,  # Add RSI function
        'gt': gt,    # Add comparison operators
        'lt': lt,
        'ge': ge,
        'le': le
    }
    
    # Add operators to namespace
    for name, op in Operator.registry.items():
        namespace[name] = op
        
    try:
        # Transform column references
        transformed_expr = expr_transform(df, expr)
        
        # Try special cases first
        result = evaluate_complex_expr(df, transformed_expr)
        if result is not None:
            return result
            
        # Convert string comparison to numeric
        if ' > ' in expr:
            left, right = expr.split(' > ')
            # Transform and evaluate left side first
            left_transformed = expr_transform(df, left)
            left_result = eval(left_transformed, namespace)
            return gt(left_result, float(right))
        elif ' < ' in expr:
            left, right = expr.split(' < ')
            # Transform and evaluate left side first
            left_transformed = expr_transform(df, left)
            left_result = eval(left_transformed, namespace)
            return lt(left_result, float(right))
            
        # Evaluate expression
        result = eval(transformed_expr, namespace)
        return result
        
    except Exception as e:
        logger.error(f"Failed to evaluate expression '{expr}': {str(e)}")
        raise ValueError(f"Invalid expression: {expr}")

def evaluate_complex_expr(df: pd.DataFrame, expr: str) -> Optional[pd.DataFrame]:
    """Handle complex expressions that need special processing."""
    # Handle special cases like industry neutralization
    if expr.startswith('INDUSTRY_NEUTRALIZE'):
        from .industry import industry_neutralize
        # Extract inner expression
        inner = expr[19:-1] 
        factor_data = calc_expr(df, inner)
        return industry_neutralize(factor_data, df['industry'])
        
    # Handle cross-sectional operations
    if expr.startswith('CS_'):
        from .cross_section import cs_rank, cs_zscore, cs_demean
        inner = expr[3:]
        if inner.startswith('RANK'):
            return cs_rank(calc_expr(df, inner[5:-1]))
        elif inner.startswith('ZSCORE'):
            return cs_zscore(calc_expr(df, inner[7:-1]))
        elif inner.startswith('DEMEAN'):
            return cs_demean(calc_expr(df, inner[7:-1]))
            
    return None