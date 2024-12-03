from typing import List, Tuple
from .alpha import AlphaBase

class AlphaTechnical(AlphaBase):
    """Technical analysis based alpha factors."""
    
    def get_fields_names(self) -> Tuple[List[str], List[str]]:
        names = []
        fields = []
        
        # RSI
        names.append('tech_rsi_14')
        fields.append('rsi(close, 14)')
        
        # MACD
        names.append('tech_macd')
        fields.append('ma(close, 12) - ma(close, 26)')
        
        # Bollinger Bands
        names.append('tech_bb')
        fields.append('(close - ma(close, 20)) / (2 * std(close, 20))')
        
        # OBV
        names.append('tech_obv')
        fields.append('sum(volume * sign(close - delay(close, 1)), 20)')
        
        # ATR
        names.append('tech_atr')
        fields.append('mean(max(high - low, abs(high - delay(close, 1)), abs(low - delay(close, 1))), 14)')
        
        return names, fields 