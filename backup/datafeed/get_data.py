import akshare as ak
import pandas as pd

from config import DATA_DIR_BASIC, DATA_DIR

# df = ak.futures_display_main_sina()
# print(df)
# df.to_csv(DATA_DIR_BASIC.joinpath('futures.csv'), index=False)

df = pd.read_csv(DATA_DIR_BASIC.joinpath('futures.csv'))
symbols = df['symbol']
for s in symbols:
    df = ak.futures_main_sina(symbol=s)
    df.rename(columns={'日期': 'date', '开盘价': 'open', '最高价': 'high',
                       '最低价': 'low', '收盘价': 'close', '成交量': 'volume', '持仓量':'open interest','动态结算价':'settlement price'}, inplace=True)
    print(s)
    df.to_csv(DATA_DIR.joinpath('futures').joinpath('{}.csv'.format(s)), index=False)
