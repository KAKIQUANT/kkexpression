from typing import List, Tuple
from .alpha import AlphaBase

class AlphaVolatility(AlphaBase):
    """Volatility-based alpha factors."""
    
    def get_fields_names(self) -> Tuple[List[str], List[str]]:
        names = []
        fields = []
        
        # Basic volatility
        names.append('vol_std_20')
        fields.append('std(returns, 20)')
        
        names.append('vol_std_60')
        fields.append('std(returns, 60)')
        
        # Parkinson volatility
        names.append('vol_park_20')
        fields.append('std((high-low)/close, 20)')
        
        # Garman-Klass volatility
        names.append('vol_gk_20')
        fields.append('mean(log(high/low)**2, 20)')
        
        # Volume-adjusted volatility
        names.append('vol_volume_20')
        fields.append('std(returns * log(volume), 20)')
        
        return names, fields 