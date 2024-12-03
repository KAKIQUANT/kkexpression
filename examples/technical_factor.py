"""
Technical factor example showing how to:
1. Use built-in technical indicators
2. Combine multiple indicators
3. Create trading signals
"""

from kkexpr import Factor
from kkexpr.expr.functions import cross_up, cross_down

def main():
    # Create moving averages
    close = Factor('close')
    ma5 = Factor('MA(close, 5)')
    ma20 = Factor('MA(close, 20)')
    
    # Create RSI
    rsi = Factor('RSI(close, 14)')
    
    # Create trading signals
    buy_signal = cross_up(ma5, ma20) & (rsi < 70)
    sell_signal = cross_down(ma5, ma20) | (rsi > 80)
    
    # Execute factor calculation
    symbols = ['000001.SH', '000300.SH']
    start_date = '20230101'
    end_date = '20231231'
    
    signals = buy_signal.execute(
        order_book_ids=symbols,
        start_date=start_date,
        end_date=end_date
    )
    
    print("Trading signals:")
    print(signals.head())

if __name__ == '__main__':
    main() 