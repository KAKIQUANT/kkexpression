import pandas as pd
from kkexpr.expr_functions import *
from loguru import logger

def expr_transform(df, expr):
    # close/shift(close,5) -1
    for col in df.columns:
        expr = expr.replace(col, 'df["{}"]'.format(col))
    return expr

@logger.catch
def calc_expr(df: pd.DataFrame, expr: str):  # correlation(rank(open),rank(volume))
    # 列若存在，就直接返回
    if expr in list(df.columns):
        return df[expr]

    expr = expr_transform(df, expr)

    try:
        se = eval(expr)
        return se
    except Exception as e:
        logger.error(e)
        import traceback
        traceback.print_exc()
        raise NameError('{}——eval异常'.format(expr))
