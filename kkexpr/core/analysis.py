import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
class FactorAnalysis:
    """Factor analysis engine following RQFactor's API."""
    
    def __init__(self,
                 factor_data: pd.DataFrame,
                 returns: pd.DataFrame,
                 groups: Optional[pd.DataFrame] = None,
                 quantiles: int = 5,
                 periods: List[int] = [1, 5, 10],
                 benchmark: Optional[str] = None):
        self.factor_data = factor_data
        self.returns = returns
        self.groups = groups
        self.quantiles = quantiles
        self.periods = periods
        self.benchmark = benchmark
        
    def calc_ic(self) -> pd.DataFrame:
        """Calculate factor IC."""
        ic_data = []
        for period in self.periods:
            fwd_ret = self.returns.shift(-period)
            ic = pd.Series(dtype=float)
            for date in self.factor_data.index.unique(level='date'):
                f = self.factor_data.xs(date, level='date')
                r = fwd_ret.xs(date, level='date')
                ic[date] = f.corr(r)
            ic_data.append(ic)
        return pd.concat(ic_data, axis=1, keys=[f'period_{p}' for p in self.periods])
        
    def calc_quantile_returns(self) -> pd.DataFrame:
        """Calculate returns by factor quantile."""
        labels = [f'Q{i+1}' for i in range(self.quantiles)]
        factor_quantile = pd.qcut(self.factor_data, self.quantiles, labels=labels)
        
        returns_by_q = []
        for period in self.periods:
            fwd_ret = self.returns.shift(-period)
            q_rets = fwd_ret.groupby(factor_quantile).mean()
            returns_by_q.append(q_rets)
            
        return pd.concat(returns_by_q, axis=1, keys=[f'period_{p}' for p in self.periods])
        
    def calc_turnover(self) -> pd.DataFrame:
        """Calculate factor quantile turnover."""
        labels = [f'Q{i+1}' for i in range(self.quantiles)]
        factor_quantile = pd.qcut(self.factor_data, self.quantiles, labels=labels)
        
        prev_quantile = factor_quantile.shift(1)
        turnover = (factor_quantile != prev_quantile).groupby(factor_quantile).mean()
        
        return turnover 

    def calc_factor_returns(self) -> pd.DataFrame:
        """Calculate factor returns using portfolio approach."""
        # Long-short portfolio returns
        labels = [f'Q{i+1}' for i in range(self.quantiles)]
        factor_quantile = pd.qcut(self.factor_data, self.quantiles, labels=labels)
        
        returns_by_period = []
        for period in self.periods:
            fwd_ret = self.returns.shift(-period)
            top_ret = fwd_ret[factor_quantile == labels[-1]].mean()
            bot_ret = fwd_ret[factor_quantile == labels[0]].mean()
            ls_ret = top_ret - bot_ret
            returns_by_period.append(ls_ret)
            
        return pd.DataFrame(returns_by_period, 
                           index=[f'period_{p}' for p in self.periods],
                           columns=['returns'])

    def calc_ic_stats(self) -> pd.DataFrame:
        """Calculate IC statistics."""
        ic = self.calc_ic()
        stats = pd.DataFrame({
            'ic_mean': ic.mean(),
            'ic_std': ic.std(),
            'ic_ir': ic.mean() / ic.std(),
            'ic_skew': ic.skew(),
            'ic_kurtosis': ic.kurtosis(),
            'ic_pos_pct': (ic > 0).mean()
        })
        return stats

    def calc_quantile_stats(self) -> pd.DataFrame:
        """Calculate quantile statistics."""
        q_rets = self.calc_quantile_returns()
        stats = pd.DataFrame({
            'mean': q_rets.mean(),
            'std': q_rets.std(),
            'sharpe': q_rets.mean() / q_rets.std(),
            'hit_rate': (q_rets > 0).mean()
        })
        return stats