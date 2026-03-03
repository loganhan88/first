from __future__ import annotations

import argparse
import logging
import time

import schedule

from market_sentiment.pipeline import SentimentPipeline


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def run_daily(hour: int = 8, minute: int = 0) -> None:
    pipeline = SentimentPipeline()

    def _job() -> None:
        report = pipeline.run_once()
        print(
            f"[{report.timestamp.isoformat()}] 市场情绪: {report.label}, 分数: {report.score}, 样本: {report.sample_size}"
        )

    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(_job)
    print(f"已启动定时任务：每天 {hour:02d}:{minute:02d} 运行")

    while True:
        schedule.run_pending()
        time.sleep(1)


def run_once() -> None:
    pipeline = SentimentPipeline()
    report = pipeline.run_once()
    print(
        f"[{report.timestamp.isoformat()}] 市场情绪: {report.label}, 分数: {report.score}, 样本: {report.sample_size}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="市场情绪评分系统")
    parser.add_argument("--once", action="store_true", help="只运行一次")
    parser.add_argument("--hour", type=int, default=8, help="每日执行小时")
    parser.add_argument("--minute", type=int, default=0, help="每日执行分钟")
    return parser.parse_args()


if __name__ == "__main__":
    setup_logging()
    args = parse_args()
    if args.once:
        run_once()
    else:
        run_daily(args.hour, args.minute)
