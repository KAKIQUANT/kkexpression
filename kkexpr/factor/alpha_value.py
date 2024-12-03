from typing import List, Tuple
from .alpha import AlphaBase

class AlphaValue(AlphaBase):
    """Value-based alpha factors."""
    
    def get_fields_names(self) -> Tuple[List[str], List[str]]:
        names = []
        fields = []
        
        # Price ratios
        names.append('value_hl_ratio')
        fields.append('high/low')
        
        names.append('value_co_ratio')
        fields.append('close/open')
        
        # Moving averages
        names.append('value_ma_ratio')
        fields.append('close/ma(close, 20)')
        
        # Volume price
        names.append('value_vwap')
        fields.append('sum(close * volume, 5) / sum(volume, 5)')
        
        # Price momentum
        names.append('value_momentum')
        fields.append('close/delay(close, 5) - 1')
        
        return names, fields 