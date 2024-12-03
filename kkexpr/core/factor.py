import numpy as np
import pandas as pd
from typing import List, Union, Optional, Dict, Any
from datetime import datetime
from kkexpr.utils import validate_date, validate_symbols
from .preprocess import winsorize, standardize, neutralize
from .engine import calc_expr

class Factor:
    """A class representing a financial factor with expression evaluation capabilities."""
    
    def __init__(self, expression: str):
        """
        Initialize Factor with an expression.
        
        Args:
            expression: Factor calculation expression or factor name
        """
        self.expression = expression
        self.dependencies = self._get_dependencies()
        self._preprocess_pipeline: List[Dict[str, Any]] = []
        
    def add_preprocessing(self, func_name: str, **kwargs) -> 'Factor':
        """Add preprocessing step."""
        self._preprocess_pipeline.append({
            'func': func_name,
            'kwargs': kwargs
        })
        return self
        
    def winsorize(self, method: str = 'mad', n_std: float = 3) -> 'Factor':
        """Add winsorization step."""
        return self.add_preprocessing('winsorize', method=method, n_std=n_std)
        
    def standardize(self) -> 'Factor':
        """Add standardization step."""
        return self.add_preprocessing('standardize')
        
    def neutralize(self, groups: pd.DataFrame, 
                  style_factors: Optional[pd.DataFrame] = None) -> 'Factor':
        """Add neutralization step."""
        return self.add_preprocessing('neutralize', 
                                    groups=groups, 
                                    style_factors=style_factors)
    
    def execute(self, 
                order_book_ids: List[str],
                start_date: Union[str, datetime],
                end_date: Union[str, datetime],
                frequency: str = '1d',
                test_data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Execute factor calculation.
        
        Args:
            order_book_ids: List of security IDs
            start_date: Start date
            end_date: End date 
            frequency: Data frequency ('1d', '1m' etc)
            test_data: Optional test data DataFrame
            
        Returns:
            DataFrame with factor values
        """
        validate_symbols(order_book_ids)
        validate_date(start_date)
        validate_date(end_date)
        
        if test_data is not None:
            df = test_data
        else:
            from kkdatac import get_price
            df = get_price(
                order_book_ids=order_book_ids,
                frequency=frequency, 
                start_date=start_date,
                end_date=end_date
            )
            
        if df is None or df.empty:
            raise ValueError("No data returned")
            
        # Calculate raw factor
        result = calc_expr(df, self.expression)
        
        # Apply preprocessing steps
        for step in self._preprocess_pipeline:
            func_name = step['func']
            kwargs = step['kwargs']
            
            if func_name == 'winsorize':
                result = winsorize(result, **kwargs)
            elif func_name == 'standardize':
                result = standardize(result)
            elif func_name == 'neutralize':
                result = neutralize(result, **kwargs)
                
        return result

    def __add__(self, other):
        return Factor(f"({self.expression} + {other})")
        
    def __sub__(self, other):
        return Factor(f"({self.expression} - {other})")
        
    def __mul__(self, other):
        return Factor(f"({self.expression} * {other})")
        
    def __truediv__(self, other):
        return Factor(f"({self.expression} / {other})")
        
    def __pow__(self, other):
        return Factor(f"({self.expression} ** {other})")
        
    def __str__(self):
        return self.expression
        
    def _get_dependencies(self) -> List[str]:
        """Get list of factor dependencies."""
        import re
        pattern = r'\b[a-zA-Z_]\w*\b'
        return list(set(re.findall(pattern, self.expression)))

# Register operators with Factor class after definition
from .operators import Operator, register_operator
for name, op in Operator.registry.items():
    setattr(Factor, name, op)