"""
作业 1：自己写的第一条交易规则（第一课作业，规则风格：趋势跟随）

规则契约（与 systems/provided/rules/ewmac.py 第 79 行的 ewmac 完全同构）：
- 规则 = 纯函数 f(数据..., 参数...) -> pd.Series，输出连续值，不是 +1/-1 二元信号
- price: 拼接后的 adjusted price，日频 pd.Series（来自 rawdata.get_daily_prices）
- vol:   日"价格单位"波动率，不是百分比波动率（来自 rawdata.daily_returns_volatility）
- 输出除以 vol 做波动率标准化，使不同品种的预测值落在同一标度上
"""

import pandas as pd


def my_forecast(price: pd.Series, vol: pd.Series, N: int = 20) -> pd.Series:
    """价格相对 N 日简单均线的偏离，再除以波动率。

    结构上是 ewmac 的近亲：
        ewmac      = fast_ewma(Lfast) - slow_ewma(Lslow)，再除 vol
        my_forecast = price            - sma(N)，          再除 vol
    即"fast 均线"退化为价格本身（窗口=1），所以这是一条很快的趋势规则，
    速度大致介于 ewmac2_8 与 ewmac8_32 之间。

    price > 均线 → 正预测（做多）；price < 均线 → 负预测（做空）；
    偏离越大信号越强 —— 连续值，天然携带强弱信息。
    """
    # min_periods=1：起始段用已有的数据算均线，而不是前 N 天全是 NaN
    # （与 ewmac.py:120 的 ewm(span=..., min_periods=1) 同一处理方式）
    sma = price.rolling(N, min_periods=1).mean()

    raw_forecast = price - sma

    # vol.ffill()：波动率序列偶有缺失日，向前填充最近一个已知值，
    # 避免预测序列产生不必要的 NaN（与 ewmac.py:124 完全一致）
    return raw_forecast / vol.ffill()
