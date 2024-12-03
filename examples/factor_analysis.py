"""
Factor analysis example showing how to:
1. Create a factor
2. Preprocess factor data
3. Analyze factor performance
"""

from kkexpr import Factor
from kkexpr.core.analysis import FactorAnalysis
from kkexpr.core.preprocess import winsorize, standardize, neutralize

def main():
    # Create a value factor
    pb = Factor('pb_ratio')
    pe = Factor('pe_ratio')
    factor = 1/pb + 1/pe
    
    # Execute factor calculation
    symbols = ['000001.SH', '000300.SH']
    start_date = '20230101'
    end_date = '20231231'
    
    factor_data = factor.execute(
        order_book_ids=symbols,
        start_date=start_date,
        end_date=end_date
    )
    
    # Preprocess factor data
    factor_data = winsorize(factor_data)
    factor_data = standardize(factor_data)
    
    # Get returns data (assuming daily returns)
    returns = Factor('close').pct_change().execute(
        order_book_ids=symbols,
        start_date=start_date,
        end_date=end_date
    )
    
    # Create analysis object
    analysis = FactorAnalysis(
        factor_data=factor_data,
        returns=returns,
        quantiles=5,
        periods=[1, 5, 10]
    )
    
    # Calculate metrics
    ic = analysis.calc_ic()
    ic_stats = analysis.calc_ic_stats()
    quantile_returns = analysis.calc_quantile_returns()
    
    print("IC Statistics:")
    print(ic_stats)
    print("\nQuantile Returns:")
    print(quantile_returns)

if __name__ == '__main__':
    main() 