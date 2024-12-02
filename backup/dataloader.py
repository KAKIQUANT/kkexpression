from pathlib import Path
from typing import List, Optional
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Dataloader:
    """Base class for loading financial data."""

    def __init__(self, 
                 path: Path,
                 symbols: List[str],
                 start_date: str = '20100101',
                 end_date: Optional[str] = None):
        """
        Initialize dataloader.
        
        Args:
            path: Data directory path
            symbols: List of symbols to load
            start_date: Start date string (YYYYMMDD)
            end_date: End date string (YYYYMMDD), defaults to today
        """
        self.validate_inputs(path, symbols, start_date, end_date)
        
        self.symbols = symbols
        self.path = path
        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime('%Y%m%d')

    @staticmethod
    def validate_inputs(path: Path,
                       symbols: List[str], 
                       start_date: str,
                       end_date: Optional[str]) -> None:
        """Validate input parameters."""
        if not path.exists():
            raise ValueError(f"Path does not exist: {path}")
            
        if not symbols:
            raise ValueError("Symbols list cannot be empty")
            
        try:
            datetime.strptime(start_date, '%Y%m%d')
            if end_date:
                datetime.strptime(end_date, '%Y%m%d')
        except ValueError:
            raise ValueError("Dates must be in YYYYMMDD format")
