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
            '((ts_rank(volume, 32) * (1 - ts_rank(((close + high) - low), 16))) * (1 - ts_rank(returns, 32)))'
        )

        # Alpha #2 (simplified)
        names.append('alpha002')
        fields.append(
            'correlation(rank(volume), rank((close - open) / open), 6)'
        )

        # Alpha #3 (simplified)
        names.append('alpha003')
        fields.append('correlation(rank(open), rank(volume), 10)')

        # Alpha #4 (simplified)
        names.append('alpha004')
        fields.append('ts_rank(rank(low), 9)')

        # Alpha #5 (simplified)
        names.append('alpha005')
        fields.append('rank(open - mean(high, 10)) * rank(close - high)')

        # Alpha #6 (simplified)
        names.append('alpha006')
        fields.append('correlation(open, volume, 10)')

        # Alpha #7 (simplified)
        names.append('alpha007')
        fields.append('ts_rank(volume, 5)')

        # Alpha #8 (simplified)
        names.append('alpha008')
        fields.append('rank(sum(returns, 5))')

        # Alpha #9 (simplified)
        names.append('alpha009')
        fields.append('delta(close, 1)')

        # Alpha #10 (simplified)
        names.append('alpha010')
        fields.append('rank(delta(close, 1))')

        return names, fields

    def __str__(self):
        return "WorldQuant 101 Alpha Factors"