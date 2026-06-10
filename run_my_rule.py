"""作业 1 验收脚本：把 my_rules.my_forecast 挂进 chapter15 系统，做三项检查。

运行（在仓库根目录）：
    $env:PYTHONIOENCODING='utf-8'; .venv\Scripts\python.exe run_my_rule.py
"""

import logging

logging.disable(logging.CRITICAL)  # 压制冗长日志

from systems.provided.futures_chapter15.basesystem import futures_system
from systems.trading_rules import TradingRule

# YAML 三要素的代码版：function（点路径）/ data（stage 方法的字符串引用）/ other_args
my_rule = TradingRule(
    dict(
        function="my_rules.my_forecast",
        data=["rawdata.get_daily_prices", "rawdata.daily_returns_volatility"],
        other_args=dict(N=20),
    )
)

# 入口：构建 System。此刻不算任何东西（惰性），首次取数才触发计算链
system = futures_system(trading_rules=dict(my_rule=my_rule))

# ---- 检查 1：输出是连续值，不是二元信号 ----
raw_corn = system.rules.get_raw_forecast("CORN", "my_rule").dropna()
print("=== 检查 1：CORN 预测值分布（应是连续分布，不是只有 ±1 两个值）===")
print(raw_corn.describe())
print(f"不同取值个数：{raw_corn.round(4).nunique()}（二元信号只会有 2 个）\n")

# ---- 检查 2 + 3：自然标度 → 自推 scalar；跨品种标度应接近 ----
print("=== 检查 2/3：自然标度与 scalar（CORN 与 SOFR 应接近，证明波动率标准化正确）===")
for instr in ["CORN", "SOFR"]:
    raw = system.rules.get_raw_forecast(instr, "my_rule").dropna()
    natural = raw.abs().mean()
    print(f"{instr:6s} 自然标度 = {natural:.3f}  →  scalar = 10/{natural:.3f} = {10 / natural:.2f}")

# ---- 顺手把 CORN 的预测曲线存成图（Windows 下不弹窗，直接看 PNG）----
ax = raw_corn.plot(title="my_rule raw forecast - CORN", figsize=(12, 4))
ax.figure.savefig("homework1_corn_forecast.png", dpi=120, bbox_inches="tight")
print("\n图已保存：homework1_corn_forecast.png")
