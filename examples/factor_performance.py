"""
Factor performance example showing how to:
1. Calculate factor performance metrics
2. Create performance reports
3. Analyze factor exposures
"""

from kkexpr import Factor
from kkexpr.core.performance import (
    calc_sharpe_ratio,
    calc_sortino_ratio,
    calc_max_drawdown,
    calc_factor_metrics
)

def main():
    # Create and calculate factor
    factor = Factor('close/MA(close, 20)')
    
    symbols = ['000001.SH', '000300.SH']
    start_date = '20230101'
    end_date = '20231231'
    
    factor_data = factor.execute(
        order_book_ids=symbols,
        start_date=start_date,
        end_date=end_date
    )
    
    # Calculate factor returns
    long_short_returns = factor_data.groupby(level='date').apply(
        lambda x: x.sort_values().iloc[-10:].mean() - x.sort_values().iloc[:10].mean()
    )
    
    # Calculate performance metrics
    metrics = calc_factor_metrics(long_short_returns)
    
    print("Factor Performance Metrics:")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Sortino Ratio: {metrics['sortino_ratio']:.2f}")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
    print(f"Annual Return: {metrics['annual_return']:.2%}")
    print(f"Win Rate: {metrics['win_rate']:.2%}")

if __name__ == '__main__':
    main() 