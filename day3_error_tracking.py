# day3_error_tracking.py
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import traceback

class ErrorTracker:
    """错误追踪器"""

    def __init__(self, log_dir: str = "./logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # 配置日志
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """配置日志记录器"""
        logger = logging.getLogger('ai_agent')
        logger.setLevel(logging.INFO)

        # 清除已有的handlers
        logger.handlers.clear()

        # 文件处理器
        log_file = self.log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def log_error(self, error: Exception, context: Optional[dict] = None):
        """记录错误"""
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }

        self.logger.error(f"Error occurred: {error_info}")

        # 保存到独立的错误文件
        error_file = self.log_dir / "errors.jsonl"
        with open(error_file, 'a', encoding='utf-8') as f:
            import json
            f.write(json.dumps(error_info, ensure_ascii=False) + '\n')

    def log_request(self, user_input: str, response: str, duration: float):
        """记录请求"""
        self.logger.info(
            f"Request: duration={duration:.2f}s, "
            f"input_length={len(user_input)}, "
            f"response_length={len(response)}"
        )

    def get_recent_errors(self, hours: int = 24) -> list:
        """获取最近的错误"""
        error_file = self.log_dir / "errors.jsonl"
        if not error_file.exists():
            return []

        recent_errors = []
        cutoff_time = datetime.now().timestamp() - hours * 3600

        with open(error_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    error = json.loads(line.strip())
                    error_time = datetime.fromisoformat(error['timestamp']).timestamp()
                    if error_time > cutoff_time:
                        recent_errors.append(error)
                except Exception:
                    continue

        return recent_errors

# 使用示例
if __name__ == "__main__":
    error_tracker = ErrorTracker()

    try:
        # 测试代码
        result = 1 / 0
    except Exception as e:
        error_tracker.log_error(e, context={"user_input": "test input"})

    print("错误已记录到日志文件")