# day2_file_tools.py
import pandas as pd
import json
import csv
from pathlib import Path
from typing import Union, List, Dict
import chardet

class FileProcessor:
    """文件处理工具"""

    @staticmethod
    def read_csv(file_path: str) -> str:
        """读取CSV文件"""
        try:
            # 自动检测编码
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding']

            df = pd.read_csv(file_path, encoding=encoding)
            return df.to_string()
        except Exception as e:
            return f"读取CSV失败: {str(e)}"

    @staticmethod
    def read_json(file_path: str) -> str:
        """读取JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return json.dumps(data, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"读取JSON失败: {str(e)}"

    @staticmethod
    def write_report(data: Dict, output_path: str) -> str:
        """写入分析报告"""
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return f"报告已保存到: {output_path}"
        except Exception as e:
            return f"保存报告失败: {str(e)}"

# 导出函数，使它们可以直接作为模块函数使用
read_csv = FileProcessor.read_csv
read_json = FileProcessor.read_json
write_report = FileProcessor.write_report