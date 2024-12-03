from typing import List, Tuple
from .alpha import AlphaBase

class AlphaMomentum(AlphaBase):
    """Momentum-based alpha factors."""
    
    def get_fields_names(self) -> Tuple[List[str], List[str]]:
        """Get momentum factor fields and names."""
        names = []
        fields = []
        
        # Price momentum
        names.append('mom_price_1m')
        fields.append('close/delay(close, 20) - 1')
        
        names.append('mom_price_3m')
        fields.append('close/delay(close, 60) - 1')
        
        # Volume momentum
        names.append('mom_volume_1m')
        fields.append('volume/ma(volume, 20) - 1')
        
        # Volatility momentum
        names.append('mom_vol_1m')
        fields.append('std(returns, 20)')
        
        # High-low range momentum
        names.append('mom_range_1m')
        fields.append('mean((high-low)/close, 20)')
        
        return names, fields 