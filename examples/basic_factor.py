"""
Basic factor example showing how to:
1. Create simple factors
2. Use arithmetic operations
3. Execute factor calculation
"""

from kkexpr import Factor
import pandas as pd

def main():
    # Create a simple price-based factor
    close = Factor('close')
    open_ = Factor('open')
    high = Factor('high')
    low = Factor('low')
    
    # Create a factor using arithmetic operations
    f = (close - open_) / (high - low)
    
    # Execute factor calculation
    start_date = '20230101'
    end_date = '20231231'
    symbols = ['000001.SH', '000300.SH', '000905.SH']
    
    result = f.execute(
        order_book_ids=symbols,
        start_date=start_date,
        end_date=end_date
    )
    
    print("Factor calculation result:")
    print(result.head())

if __name__ == '__main__':
    main() 