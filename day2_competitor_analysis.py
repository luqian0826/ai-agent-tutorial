# day2_competitor_analysis.py
from day2_team import ai_team
from day2_file_tools import FileProcessor
from day2_memory import AgentMemory
from datetime import datetime
from pathlib import Path
import json

class CompetitorAnalysisSystem:
    """竞品分析系统"""

    def __init__(self):
        self.file_processor = FileProcessor()
        self.memory = AgentMemory("competitor_analysis")
        self.output_dir = Path("./competitor_reports")
        self.output_dir.mkdir(exist_ok=True)

    def analyze_product(self, product_name: str,
                       save_report: bool = True) -> dict:
        """分析竞品"""

        print(f"🎯 开始分析: {product_name}")
        print("=" * 60)

        # 1. 运行AI团队分析
        try:
            result = ai_team.kickoff(inputs={"product_name": product_name})

            # 2. 保存分析结果
            report_data = {
                "product_name": product_name,
                "analysis_date": datetime.now().isoformat(),
                "analysis_result": str(result),
                "status": "completed"
            }

            if save_report:
                self._save_report(product_name, report_data)

            # 3. 存储到记忆
            self.memory.store_conversation(
                user_input=f"分析产品: {product_name}",
                agent_response=str(result),
                metadata={
                    "product_name": product_name,
                    "analysis_type": "competitor_analysis"
                }
            )

            print("=" * 60)
            print("✅ 分析完成！")

            return report_data

        except Exception as e:
            error_msg = f"分析失败: {str(e)}"
            print(f"❌ {error_msg}")

            error_data = {
                "product_name": product_name,
                "analysis_date": datetime.now().isoformat(),
                "error": error_msg,
                "status": "failed"
            }

            return error_data

    def _save_report(self, product_name: str, report_data: dict):
        """保存报告"""
        # 清理产品名称作为文件名
        safe_name = "".join(c for c in product_name
                          if c.isalnum() or c in (' ', '-', '_')).strip()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp}.json"
        filepath = self.output_dir / filename

        self.file_processor.write_report(report_data, str(filepath))
        print(f"📄 报告已保存: {filepath}")

    def batch_analyze(self, product_list: list) -> list:
        """批量分析"""
        print(f"🔄 开始批量分析 {len(product_list)} 个产品")
        print("=" * 60)

        results = []
        for i, product in enumerate(product_list, 1):
            print(f"\n[{i}/{len(product_list)}] 分析: {product}")
            result = system.analyze_product(product)
            results.append(result)

        print("\n" + "=" * 60)
        print("✅ 批量分析完成！")

        # 生成汇总报告
        self._generate_batch_summary(results)

        return results

    def _generate_batch_summary(self, results: list):
        """生成批量分析汇总"""
        summary = {
            "total_products": len(results),
            "successful": sum(1 for r in results if r.get("status") == "completed"),
            "failed": sum(1 for r in results if r.get("status") == "failed"),
            "analysis_date": datetime.now().isoformat(),
            "products": [r.get("product_name") for r in results]
        }

        summary_path = self.output_dir / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.file_processor.write_report(summary, str(summary_path))

        print(f"\n📊 汇总报告: {summary_path}")
        print(f"   成功: {summary['successful']}")
        print(f"   失败: {summary['failed']}")

    def get_analysis_history(self) -> list:
        """获取分析历史"""
        reports = list(self.output_dir.glob("*.json"))
        history = []

        for report_file in reports:
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history.append({
                        "file": report_file.name,
                        "product": data.get("product_name"),
                        "date": data.get("analysis_date"),
                        "status": data.get("status")
                    })
            except:
                continue

        # 按时间排序
        history.sort(key=lambda x: x.get("date", ""), reverse=True)

        return history

# 测试代码
if __name__ == "__main__":
    print("🏢 测试竞品分析系统")
    print("=" * 60)

    system = CompetitorAnalysisSystem()

    # 单个产品分析
    print("\n1️⃣ 单个产品分析:")
    result = system.analyze_product("MacBook Pro 14")
    print(f"   状态: {result.get('status', 'unknown')}")

    # 查看分析历史
    print("\n2️⃣ 查看分析历史:")
    history = system.get_analysis_history()
    print(f"   历史记录数: {len(history)}")
    for i, h in enumerate(history[:5], 1):
        print(f"      {i}. {h['product']} - {h['date']}")

    # 批量分析示例（可选）
    # print("\n3️⃣ 批量分析示例:")
    # products = [
    #     "iPhone 15 Pro",
    #     "Samsung Galaxy S24",
    #     "Google Pixel 8"
    # ]
    # system.batch_analyze(products)

    print("\n" + "=" * 60)
    print("✅ 竞品分析系统测试完成")