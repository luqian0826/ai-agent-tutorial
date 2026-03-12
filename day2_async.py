# day2_async.py
import asyncio
import time
from typing import List, Dict

class AsyncAnalyzer:
    """异步分析器"""

    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def analyze_single_product(self, product_name: str) -> Dict:
        """异步分析单个产品"""
        async with self.semaphore:
            print(f"🔄 开始分析: {product_name}")
            start_time = time.time()

            try:
                # 模拟API调用（实际替换为真实API）
                await asyncio.sleep(2)  # 模拟网络延迟

                result = {
                    "product": product_name,
                    "status": "success",
                    "analysis_time": time.time() - start_time,
                    "data": f"分析结果数据..."  # 实际数据
                }

                print(f"✅ 完成: {product_name} ({result['analysis_time']:.2f}s)")
                return result

            except Exception as e:
                print(f"❌ 失败: {product_name} - {str(e)}")
                return {
                    "product": product_name,
                    "status": "failed",
                    "error": str(e)
                }

    async def batch_analyze(self, product_list: List[str]) -> List[Dict]:
        """批量异步分析"""
        print(f"🚀 开始异步批量分析 ({len(product_list)} 个产品)")
        print(f"⚡ 并发数: {self.max_concurrent}")
        print("=" * 60)

        start_time = time.time()

        # 创建所有任务
        tasks = [self.analyze_single_product(product)
                for product in product_list]

        # 并发执行
        results = await asyncio.gather(*tasks)

        total_time = time.time() - start_time

        print("=" * 60)
        print(f"✅ 批量分析完成！")
        print(f"⏱️ 总耗时: {total_time:.2f}s")
        print(f"📊 成功: {sum(1 for r in results if r['status'] == 'success')}")
        print(f"❌ 失败: {sum(1 for r in results if r['status'] == 'failed')}")

        return results

    async def analyze_with_timeout(self, product_name: str, timeout: float = 5.0) -> Dict:
        """带超时的分析"""
        try:
            result = await asyncio.wait_for(
                self.analyze_single_product(product_name),
                timeout=timeout
            )
            return result
        except asyncio.TimeoutError:
            print(f"⏰ 超时: {product_name}")
            return {
                "product": product_name,
                "status": "timeout",
                "error": f"Analysis timeout after {timeout} seconds"
            }

# 性能对比测试
async def performance_comparison():
    """性能对比"""
    products = [f"Product_{i}" for i in range(1, 11)]

    print("📊 性能对比测试")
    print("=" * 60)

    # 同步执行
    print("\n1️⃣ 同步执行:")
    start = time.time()
    for product in products:
        await asyncio.sleep(2)  # 模拟每个任务2秒
    sync_time = time.time() - start
    print(f"   耗时: {sync_time:.2f}s")

    # 异步执行（并发3）
    print("\n2️⃣ 异步执行（并发3）:")
    analyzer = AsyncAnalyzer(max_concurrent=3)
    await analyzer.batch_analyze(products)

    # 异步执行（并发5）
    print("\n3️⃣ 异步执行（并发5）:")
    analyzer = AsyncAnalyzer(max_concurrent=5)
    await analyzer.batch_analyze(products)

    # 计算加速比
    async_time_3 = (10 / 3) * 2  # 理论值
    async_time_5 = (10 / 5) * 2  # 理论值

    print(f"\n📈 性能提升:")
    print(f"   并发3: 加速 {sync_time/async_time_3:.2f}x")
    print(f"   并发5: 加速 {sync_time/async_time_5:.2f}x")

# 实际应用示例
async def real_world_analysis():
    """实际应用分析"""
    print("\n🌍 实际应用场景")
    print("=" * 60)

    # 模拟真实产品列表
    products = [
        "iPhone 15 Pro",
        "Samsung Galaxy S24",
        "Google Pixel 8",
        "Xiaomi 14",
        "OnePlus 12"
    ]

    analyzer = AsyncAnalyzer(max_concurrent=3)
    results = await analyzer.batch_analyze(products)

    # 汇总结果
    print("\n📋 分析结果汇总:")
    for result in results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"   {status_icon} {result['product']}: {result['status']}")

# 超时处理测试
async def timeout_test():
    """超时处理测试"""
    print("\n⏰ 超时处理测试")
    print("=" * 60)

    analyzer = AsyncAnalyzer(max_concurrent=2)

    products = ["快速产品", "慢速产品", "超时产品"]

    tasks = [
        analyzer.analyze_with_timeout(products[0], timeout=5.0),
        analyzer.analyze_with_timeout(products[1], timeout=5.0),
        analyzer.analyze_with_timeout(products[2], timeout=1.0)  # 1秒超时
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    print("\n结果:")
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"   {i+1}. 异常: {str(result)}")
        else:
            print(f"   {i+1}. {result['product']}: {result['status']}")

# 主测试函数
async def main():
    """主测试函数"""
    print("🚀 异步处理演示")
    print("=" * 60)
    print()

    # 性能对比
    await performance_comparison()

    # 实际应用
    await real_world_analysis()

    # 超时处理
    await timeout_test()

    print("\n" + "=" * 60)
    print("✅ 异步处理演示完成")

# 运行测试
if __name__ == "__main__":
    asyncio.run(main())