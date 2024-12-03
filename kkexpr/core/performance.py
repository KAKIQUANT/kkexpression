import pandas as pd
import numpy as np
from typing import Optional

def calc_sharpe_ratio(returns: pd.Series, 
                     risk_free: Optional[float] = 0.0,
                     periods_per_year: int = 252) -> float:
    """Calculate annualized Sharpe ratio."""
    excess_ret = returns - risk_free
    return np.sqrt(periods_per_year) * excess_ret.mean() / excess_ret.std()

def calc_sortino_ratio(returns: pd.Series,
                      risk_free: Optional[float] = 0.0,
                      periods_per_year: int = 252) -> float:
    """Calculate Sortino ratio."""
    excess_ret = returns - risk_free
    downside_std = np.sqrt(np.mean(np.minimum(excess_ret, 0) ** 2))
    return np.sqrt(periods_per_year) * excess_ret.mean() / downside_std

def calc_max_drawdown(returns: pd.Series) -> float:
    """Calculate maximum drawdown."""
    cum_returns = (1 + returns).cumprod()
    rolling_max = cum_returns.expanding().max()
    drawdowns = cum_returns / rolling_max - 1
    return drawdowns.min()

def calc_factor_metrics(factor_returns: pd.Series) -> pd.Series:
    """Calculate comprehensive factor performance metrics."""
    metrics = pd.Series({
        'total_return': (1 + factor_returns).prod() - 1,
        'annual_return': factor_returns.mean() * 252,
        'annual_volatility': factor_returns.std() * np.sqrt(252),
        'sharpe_ratio': calc_sharpe_ratio(factor_returns),
        'sortino_ratio': calc_sortino_ratio(factor_returns),
        'max_drawdown': calc_max_drawdown(factor_returns),
        'win_rate': (factor_returns > 0).mean(),
        'skewness': factor_returns.skew(),
        'kurtosis': factor_returns.kurtosis()
    })
    return metrics 