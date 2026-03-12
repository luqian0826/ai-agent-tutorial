# day2_analysis_tools.py
import numpy as np
from typing import List, Dict
import statistics

class DataAnalyzer:
    """数据分析工具"""

    @staticmethod
    def analyze_sales_data(data: List[Dict]) -> Dict:
        """分析销售数据"""
        if not data:
            return {"error": "数据为空"}

        try:
            # 提取销售额
            sales = [float(item.get('sales', 0)) for item in data if 'sales' in item]

            if not sales:
                return {"error": "没有找到销售数据"}

            analysis = {
                "total_sales": sum(sales),
                "average_sales": statistics.mean(sales),
                "max_sales": max(sales),
                "min_sales": min(sales),
                "sales_count": len(sales),
                "growth_rate": DataAnalyzer._calculate_growth(sales),
                "recommendations": DataAnalyzer._generate_recommendations(sales)
            }

            return analysis
        except Exception as e:
            return {"error": f"分析失败: {str(e)}"}

    @staticmethod
    def _calculate_growth(sales: List[float]) -> float:
        """计算增长率"""
        if len(sales) < 2:
            return 0.0

        recent = sales[-7:] if len(sales) >= 7 else sales
        previous = sales[-14:-7] if len(sales) >= 14 else sales[:len(recent)]

        if not previous:
            return 0.0

        avg_recent = statistics.mean(recent)
        avg_previous = statistics.mean(previous)

        if avg_previous == 0:
            return 0.0

        return (avg_recent - avg_previous) / avg_previous * 100

    @staticmethod
    def _generate_recommendations(sales: List[float]) -> List[str]:
        """生成建议"""
        recommendations = []

        if len(sales) >= 7:
            recent_trend = np.polyfit(range(len(sales[-7:])), sales[-7:], 1)[0]

            if recent_trend > 0:
                recommendations.append("销售呈上升趋势，建议增加库存")
            else:
                recommendations.append("销售下降，建议进行促销活动")

        if len(sales) >= 30:
            volatility = statistics.stdev(sales[-30:]) / statistics.mean(sales[-30:])
            if volatility > 0.3:
                recommendations.append("销售波动较大，建议分析原因")

        return recommendations

    @staticmethod
    def analyze_products(data: List[Dict]) -> Dict:
        """分析产品数据"""
        if not data:
            return {"error": "数据为空"}

        try:
            # 按产品分组统计
            product_stats = {}

            for item in data:
                product = item.get('product', 'unknown')
                sales = float(item.get('sales', 0))

                if product not in product_stats:
                    product_stats[product] = {
                        "total_sales": 0,
                        "count": 0,
                        "dates": []
                    }

                product_stats[product]["total_sales"] += sales
                product_stats[product]["count"] += 1
                product_stats[product]["dates"].append(item.get('date', ''))

            # 计算平均值和排名
            results = []
            for product, stats in product_stats.items():
                avg_sales = stats["total_sales"] / stats["count"]
                results.append({
                    "product": product,
                    "total_sales": stats["total_sales"],
                    "average_sales": avg_sales,
                    "count": stats["count"]
                })

            # 按总销售额排序
            results.sort(key=lambda x: x["total_sales"], reverse=True)

            return {
                "total_products": len(results),
                "top_product": results[0] if results else None,
                "product_rankings": results
            }
        except Exception as e:
            return {"error": f"分析失败: {str(e)}"}

# 测试代码
if __name__ == "__main__":
    print("📊 测试数据分析工具")
    print("=" * 60)

    analyzer = DataAnalyzer()

    # 测试销售数据分析
    print("1. 测试销售数据分析...")
    sales_data = [
        {"date": "2024-01-01", "sales": 100},
        {"date": "2024-01-02", "sales": 120},
        {"date": "2024-01-03", "sales": 110},
        {"date": "2024-01-04", "sales": 130},
        {"date": "2024-01-05", "sales": 140},
        {"date": "2024-01-06", "sales": 125},
        {"date": "2024-01-07", "sales": 150},
        {"date": "2024-01-08", "sales": 160},
        {"date": "2024-01-09", "sales": 145},
        {"date": "2024-01-10", "sales": 170},
    ]

    result = analyzer.analyze_sales_data(sales_data)
    print(f"   总销售额: {result.get('total_sales', 0)}")
    print(f"   平均销售额: {result.get('average_sales', 0):.2f}")
    print(f"   增长率: {result.get('growth_rate', 0):.2f}%")
    print(f"   建议: {', '.join(result.get('recommendations', []))}")

    # 测试产品分析
    print("\n2. 测试产品分析...")
    product_data = [
        {"date": "2024-01-01", "product": "A", "sales": 100},
        {"date": "2024-01-02", "product": "B", "sales": 150},
        {"date": "2024-01-03", "product": "A", "sales": 120},
        {"date": "2024-01-04", "product": "C", "sales": 200},
        {"date": "2024-01-05", "product": "B", "sales": 180},
        {"date": "2024-01-06", "product": "A", "sales": 130},
    ]

    result = analyzer.analyze_products(product_data)
    print(f"   产品总数: {result.get('total_products', 0)}")
    print(f"   热门产品: {result.get('top_product', {}).get('product', 'N/A')}")
    print("   产品排名:")
    for i, p in enumerate(result.get('product_rankings', [])[:3], 1):
        print(f"      {i}. {p['product']}: ¥{p['total_sales']}")

    print("\n" + "=" * 60)
    print("✅ 数据分析工具测试完成")