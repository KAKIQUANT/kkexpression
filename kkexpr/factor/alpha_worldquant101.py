from typing import List, Tuple
from .alpha import AlphaBase

class WorldQuant101(AlphaBase):
    """WorldQuant 101 Alpha Factors implementation."""
    
    def get_fields_names(self) -> Tuple[List[str], List[str]]:
        """Get WorldQuant 101 factor fields and names."""
        names = []
        fields = []

        # Alpha #1
        names.append('alpha001')
        fields.append(
            '(rank(ts_argmax(signed_power((returns < 0 ? std(returns, 20) : close), 2.), 5)) - 0.5)'
        )

        # Alpha #2
        names.append('alpha002')
        fields.append(
            '(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))'
        )

        # Alpha #3
        names.append('alpha003')
        fields.append('(-1 * correlation(rank(open), rank(volume), 10))')

        # Add remaining alphas...
        # Copy remaining implementations from original file

        return names, fields