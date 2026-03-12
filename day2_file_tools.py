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

    @staticmethod
    def write_csv(data: List[Dict], output_path: str) -> str:
        """写入CSV文件"""
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False, encoding='utf-8')

            return f"CSV文件已保存到: {output_path}"
        except Exception as e:
            return f"保存CSV失败: {str(e)}"

    @staticmethod
    def append_to_csv(data: Dict, file_path: str) -> str:
        """追加数据到CSV文件"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # 检查文件是否存在
            if file_path.exists():
                df = pd.read_csv(file_path, encoding='utf-8')
                df_new = pd.DataFrame([data])
                df = pd.concat([df, df_new], ignore_index=True)
            else:
                df = pd.DataFrame([data])

            df.to_csv(file_path, index=False, encoding='utf-8')

            return f"数据已追加到: {file_path}"
        except Exception as e:
            return f"追加数据失败: {str(e)}"

# 测试代码
if __name__ == "__main__":
    print("📁测试文件处理工具")
    print("=" * 60)

    processor = FileProcessor()

    # 测试创建示例CSV文件
    sample_data = [
        {"date": "2024-01-01", "product": "A", "sales": 100},
        {"date": "2024-01-02", "product": "B", "sales": 150},
        {"date": "2024-01-03", "product": "A", "sales": 120},
    ]

    print("1. 创建示例CSV文件...")
    result = processor.write_csv(sample_data, "./test_data.csv")
    print(f"   {result}")

    print("\n2. 读取CSV文件...")
    result = processor.read_csv("./test_data.csv")
    print(f"   {result}")

    print("\n3. 测试JSON文件...")
    json_data = {"test": "data", "value": 123}
    result = processor.write_report(json_data, "./test_report.json")
    print(f"   {result}")

    result = processor.read_json("./test_report.json")
    print(f"   {result}")

    print("\n4. 追加数据到CSV...")
    new_data = {"date": "2024-01-04", "product": "C", "sales": 200}
    result = processor.append_to_csv(new_data, "./test_data.csv")
    print(f"   {result}")

    result = processor.read_csv("./test_data.csv")
    print(f"   {result}")

    print("\n" + "=" * 60)
    print("✅ 文件处理工具测试完成")

    # 清理测试文件
    import os
    try:
        os.remove("./test_data.csv")
        os.remove("./test_report.json")
        print("🗑️  测试文件已清理")
    except:
        pass