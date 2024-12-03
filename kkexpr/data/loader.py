import pandas as pd
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from kkexpr.core.engine import calc_expr
from loguru import logger
from functools import wraps

def catch_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

class CSVDataloader:
    def __init__(self, 
                 path: Path,
                 symbols: List[str],
                 start_date: str = '20190101',
                 end_date: Optional[str] = None):
        self.path = path
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime('%Y%m%d')
        logger.debug(f"Initialized CSVDataloader with path={path}, symbols={symbols}, "
                    f"start_date={start_date}, end_date={end_date}")

    @catch_errors
    def load(self, fields: Optional[List[str]] = None, names: Optional[List[str]] = None) -> pd.DataFrame:
        """Load data from CSV files."""
        logger.debug(f"Loading data with fields={fields}, names={names}")
        
        dfs = []
        for symbol in self.symbols:
            file_path = self.path / f'{symbol}.csv'
            logger.debug(f"Reading file: {file_path}")
            # Read CSV and convert date column
            df = pd.read_csv(file_path)
            # Convert numeric columns to strings
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(str)
            # Convert date string to datetime
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
            df.set_index('date', inplace=True)
            df['symbol'] = symbol
            logger.debug(f"Loaded {symbol} data shape: {df.shape}")
            dfs.append(df)
            
        df = pd.concat(dfs)
        logger.debug(f"Concatenated DataFrame shape: {df.shape}")
        
        # Create MultiIndex correctly
        df = df.set_index('symbol', append=True)
        df = df.swaplevel()  # Make symbol the first level
        df.index.names = ['symbol', 'date']
        df = df.sort_index()
        logger.debug("Index sorted")
        
        # Convert input dates to datetime
        start_date = pd.to_datetime(str(self.start_date), format='%Y%m%d')
        end_date = pd.to_datetime(str(self.end_date), format='%Y%m%d')
        logger.debug(f"Date range: {start_date} to {end_date}")
        
        # Filter by date range
        result = df.loc[(slice(None), slice(start_date, end_date)), :]
        logger.debug(f"Filtered result shape: {result.shape}")
        
        if result.empty:
            logger.error("No data available in the specified date range")
            raise ValueError("No data available in the specified date range.")
        
        if fields and names:
            logger.debug("Processing expressions")
            for field, name in zip(fields, names):
                logger.debug(f"Calculating expression: {field} -> {name}")
                try:
                    result[name] = calc_expr(result, field)
                except Exception as e:
                    logger.exception(f"Error calculating expression '{field}': {str(e)}")
                    raise
        
        logger.debug(f"Final result shape: {result.shape}")
        return result 