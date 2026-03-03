# 市场情绪评分系统（Market Sentiment Scoring）

该系统每天自动抓取主流媒体市场新闻（RSS），对新闻标题+摘要进行情绪分析，输出金融市场**乐观/悲观分数**（-100 到 100），并写入历史记录。

## 功能概览

- 自动抓取多家媒体新闻源（可配置）
- 基于中英金融词典进行情绪评分
- 按媒体权重聚合为日度市场情绪分数
- 输出情绪标签：`very_bearish / bearish / neutral / bullish / very_bullish`
- 历史结果以 JSONL 保存，便于后续接入看板或模型训练

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

单次运行：

```bash
python main.py --once
```

每天定时运行（默认每天 08:00）：

```bash
python main.py
```

自定义定时：

```bash
python main.py --hour 9 --minute 30
```

## 配置

编辑 `config/sources.yaml`：

- `sources`: 新闻源列表（name/type/url/weight）
- `max_articles_per_source`: 每源每日抓取上限
- `score_bands`: 情绪标签阈值

## 输出

历史记录保存到：

- `data/sentiment_history.jsonl`

每行是一条日度快照，包含：

- 时间戳
- 总分与标签
- 样本数
- 每篇文章的细粒度评分

## 扩展建议

- 增加评论源（如 Reddit、YouTube、财经社区 API）
- 用 FinBERT / 多语种 Transformer 替代词典法
- 增加事件权重（央行、非农、财报季）
- 对接仪表盘（Streamlit/Grafana）
