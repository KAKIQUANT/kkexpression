import pandas as pd
from kkexpr.expr_functions.expr_utils import calc_by_symbol


@calc_by_symbol
def label(se: pd.Series, period: int):
    return se.shift(period) / se - 1
