import numpy as np
import pandas as pd

from .expr_utils import *


@calc_by_symbol
def sign(se: pd.Series):
    return np.sign(se)


@calc_by_symbol
def signed_power(se: pd.Series, a):
    return np.where(se < 0, -np.abs(se) ** a, np.abs(se) ** a)

@calc_by_symbol
def log(se: pd.Series):
    return np.log(se)


@calc_by_symbol
def abs(se):
    return np.abs(se)


def scale(x, a=1):
    """
    Scales the array x such that the sum of the absolute values equals a.

    Parameters:
    x (array-like): The input array to be scaled.
    a (float, optional): The target sum of absolute values. Default is 1.

    Returns:
    numpy.ndarray: The scaled array.
    """
    import numpy as np
    x = np.array(x)  # 确保输入是numpy数组
    sum_abs_x = np.sum(np.abs(x))  # 计算x的绝对值之和
    if sum_abs_x == 0:
        raise ValueError("The sum of absolute values of x is zero, cannot scale by a non-zero value.")
    scale_factor = a / sum_abs_x  # 计算缩放因子
    return x * scale_factor  # 应用缩放因子

def decay_linear(series, window):
    """
    对输入的时间序列进行线性衰减。

    :param series: 输入的时间序列。
    :param window: 衰减的窗口大小。
    :return: 衰减后的序列。
    """
    weights = np.arange(1, window + 1)
    decay = np.convolve(series, weights, 'valid') / np.sum(weights)
    return decay