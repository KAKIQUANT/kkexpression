from typing import List, Tuple
from .alpha import AlphaBase

class Alpha158(AlphaBase):
    """Alpha158 factor implementation."""
    
    def get_fields_names(self) -> Tuple[List[str], List[str]]:
        """Get Alpha158 factor fields and names."""
        fields = []
        names = []

        # Price volume features
        fields += [
            "(close-open)/open",
            "(high-low)/open",
            "(close-open)/(high-low+1e-12)",
            "(high-greater(open, close))/open",
            "(high-greater(open, close))/(high-low+1e-12)",
            "(less(open, close)-low)/open",
            "(less(open, close)-low)/(high-low+1e-12)",
            "(2*close-high-low)/open",
            "(2*close-high-low)/(high-low+1e-12)",
        ]
        names += [
            "KMID",
            "KLEN",
            "KMID2",
            "KUP",
            "KUP2",
            "KLOW",
            "KLOW2",
            "KSFT",
            "KSFT2",
        ]

        # Price features
        feature = ["OPEN", "HIGH", "LOW", "CLOSE"]
        windows = range(5)
        for field in feature:
            field = field.lower()
            fields += [
                f"shift({field}, {d})/close" if d != 0 else f"{field}/close" 
                for d in windows
            ]
            names += [field.upper() + str(d) for d in windows]

        # Volume features
        fields += [
            f"shift(volume, {d})/(volume+1e-12)" if d != 0 else "volume/(volume+1e-12)" 
            for d in windows
        ]
        names += ["VOLUME" + str(d) for d in windows]

        # Rolling features
        windows = [5, 10, 20, 30, 60]
        
        # Returns
        fields += [f"shift(close, {d})/close" for d in windows]
        names += [f"ROC{d}" for d in windows]

        # Moving averages
        fields += [f"mean(close, {d})/close" for d in windows]
        names += [f"MA{d}" for d in windows]

        # Volatility
        fields += [f"std(close, {d})/close" for d in windows]
        names += [f"STD{d}" for d in windows]

        # Max/Min
        fields += [f"ts_max(high, {d})/close" for d in windows]
        names += [f"MAX{d}" for d in windows]

        fields += [f"ts_min(low, {d})/close" for d in windows]
        names += [f"MIN{d}" for d in windows]

        # Quantiles
        fields += [f"quantile(close, {d}, 0.8)/close" for d in windows]
        names += [f"QTLU{d}" for d in windows]

        fields += [f"quantile(close, {d}, 0.2)/close" for d in windows]
        names += [f"QTLD{d}" for d in windows]

        # RSV
        fields += [
            f"(close-ts_min(low, {d}))/(ts_max(high, {d})-ts_min(low, {d})+1e-12)" 
            for d in windows
        ]
        names += [f"RSV{d}" for d in windows]

        # More features...
        # Add remaining features from original implementation

        return fields, names