from datetime import datetime
from typing import List, Union

def validate_date(date: Union[str, datetime]) -> None:
    """Validate date format."""
    if isinstance(date, str):
        try:
            datetime.strptime(date, '%Y%m%d')
        except ValueError:
            raise ValueError("Date must be in YYYYMMDD format")

def validate_symbols(symbols: List[str]) -> None:
    """Validate symbol format."""
    if not symbols:
        raise ValueError("Symbols list cannot be empty")
    for symbol in symbols:
        if not isinstance(symbol, str):
            raise TypeError(f"Symbol must be string, got {type(symbol)}")
