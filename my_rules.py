"""
作业 1：自己写一条交易规则（第一课作业，书 p121 附近）

规则契约（参照 systems/provided/rules/ewmac.py 第 79 行的 ewmac，它就是标准答案的"形"）：
- 规则 = 纯函数 f(数据..., 参数...) -> pd.Series，输出是连续值，不能是 +1/-1 二元信号
- price: 拼接后的 adjusted price，日频 pd.Series（来自 rawdata.get_daily_prices）
- vol:   日"价格单位"波动率，不是百分比波动率（来自 rawdata.daily_returns_volatility）
- 输出必须除以 vol 做波动率标准化 —— 这样 CORN（价格几百）和 SOFR（价格 ~99）
  的预测值才在同一标度上，这正是验收要检查的第 3 点
"""

import pandas as pd


def my_forecast(price: pd.Series, vol: pd.Series, N: int = 20) -> pd.Series:
    """价格相对 N 日均线的偏离，再除以波动率。

    TODO（作业，约 3 行）：
      1. 算 N 日均线（简单均线 rolling(N).mean()，或 ewm(span=N).mean()，自选并能说出理由）
      2. 偏离 = price - 均线
      3. return 偏离 / vol
    """
    raise NotImplementedError("作业：在这里实现你的规则")
