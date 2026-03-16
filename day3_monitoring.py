# day3_monitoring.py
import time
import psutil
from datetime import datetime
from typing import Dict
import json
from pathlib import Path

class PerformanceMonitor:
    """性能监控器"""

    def __init__(self, log_dir: str = "./logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.metrics_file = self.log_dir / "metrics.jsonl"

    def collect_metrics(self) -> Dict:
        """收集系统指标"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent if psutil.disk_usage('/') else 0,
            "network_sent": psutil.net_io_counters().bytes_sent if psutil.net_io_counters() else 0,
            "network_recv": psutil.net_io_counters().bytes_recv if psutil.net_io_counters() else 0,
        }

        return metrics

    def save_metrics(self, metrics: Dict):
        """保存指标到文件"""
        with open(self.metrics_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(metrics, ensure_ascii=False) + '\n')

    def get_recent_metrics(self, minutes: int = 60) -> list:
        """获取最近的指标"""
        if not self.metrics_file.exists():
            return []

        recent_metrics = []
        cutoff_time = datetime.now().timestamp() - minutes * 60

        with open(self.metrics_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    metric = json.loads(line.strip())
                    metric_time = datetime.fromisoformat(metric['timestamp']).timestamp()
                    if metric_time > cutoff_time:
                        recent_metrics.append(metric)
                except Exception:
                    continue

        return recent_metrics

    def get_summary(self, minutes: int = 60) -> Dict:
        """获取摘要统计"""
        metrics = self.get_recent_metrics(minutes)

        if not metrics:
            return {}

        cpu_values = [m['cpu_percent'] for m in metrics]
        memory_values = [m['memory_percent'] for m in metrics]

        summary = {
            "avg_cpu": sum(cpu_values) / len(cpu_values),
            "max_cpu": max(cpu_values),
            "avg_memory": sum(memory_values) / len(memory_values),
            "max_memory": max(memory_values),
            "total_requests": len(metrics)
        }

        return summary

# 在Streamlit应用中集成监控
def render_monitoring_dashboard():
    """渲染监控面板"""
    import streamlit as st
    import pandas as pd

    monitor = PerformanceMonitor()

    st.header("📊 系统监控")

    # 实时指标
    current_metrics = monitor.collect_metrics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "CPU使用率",
            f"{current_metrics['cpu_percent']:.1f}%",
            delta=f"{current_metrics['cpu_percent'] - 50:.1f}%"
        )

    with col2:
        st.metric(
            "内存使用率",
            f"{current_metrics['memory_percent']:.1f}%",
            delta=f"{current_metrics['memory_percent'] - 50:.1f}%"
        )

    with col3:
        st.metric(
            "磁盘使用率",
            f"{current_metrics['disk_percent']:.1f}%",
            delta=f"{current_metrics['disk_percent'] - 50:.1f}%"
        )

    with col4:
        st.metric(
            "请求数量",
            monitor.get_summary(minutes=60).get('total_requests', 0)
        )

    # 保存当前指标
    monitor.save_metrics(current_metrics)

    # 历史趋势图
    if st.checkbox("显示历史趋势"):
        metrics = monitor.get_recent_metrics(minutes=60)

        if metrics:
            df = pd.DataFrame(metrics)
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            st.line_chart(df.set_index('timestamp')[['cpu_percent', 'memory_percent']])