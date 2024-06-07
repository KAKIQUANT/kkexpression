from kkexpr import Factor

def test_factor():
    factor_str = "(RANK(CORRELATION(((HIGH * 0.876703) + (CLOSE * (1 - 0.876703))), ADV(30), 10))**RANK(CORRELATION(TS_RANK(((HIGH + LOW) / 2), 4), TS_RANK(VOLUME, 10), 7)))".lower()
    print(factor_str)
    factor = Factor(factor_str)

    print(factor)

def test_simple_factor():
    # open_factor = Factor('open')
    # close_factor = Factor('close')
    # high_factor = Factor('high')
    # low_factor = Factor('low')

    # # Example usage
    # f = (close_factor - open_factor) / (high_factor - low_factor)
    # print(f)
    f = Factor("ts_rank(close - open / high - low)")
    Factor.execute_factor(f, ["000001.XSHE"], "2020-01-01", "2020-01-10")
if __name__ == '__main__':
    test_simple_factor()