# day2_cache.py
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import time

class AnalysisCache:
    """分析结果缓存"""

    def __init__(self, cache_dir: str = "./cache",
                 cache_duration_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_duration = cache_duration_hours * 3600  # 转换为秒

        # 统计信息
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0
        }

    def _get_cache_key(self, query: str) -> str:
        """生成缓存键"""
        return hashlib.md5(query.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{cache_key}.json"

    def get(self, query: str) -> Optional[Dict]:
        """获取缓存"""
        cache_key = self._get_cache_key(query)
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            self.stats["misses"] += 1
            return None

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # 检查是否过期
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            age_seconds = (datetime.now() - cache_time).total_seconds()

            if age_seconds > self.cache_duration:
                # 过期，删除缓存
                cache_path.unlink()
                self.stats["misses"] += 1
                return None

            self.stats["hits"] += 1
            return cache_data['data']

        except Exception as e:
            print(f"❌ 读取缓存失败: {e}")
            self.stats["misses"] += 1
            return None

    def set(self, query: str, data: Dict):
        """保存到缓存"""
        cache_key = self._get_cache_key(query)
        cache_path = self._get_cache_path(cache_key)

        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "data": data
        }

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            self.stats["sets"] += 1
        except Exception as e:
            print(f"❌ 保存缓存失败: {e}")

    def clear(self, query: str = None):
        """清理缓存"""
        if query:
            # 清理单个产品缓存
            cache_key = self._get_cache_key(query)
            cache_path = self._get_cache_path(cache_key)
            if cache_path.exists():
                cache_path.unlink()
                print(f"🗑️  已清理缓存: {query}")
        else:
            # 清理所有缓存
            count = 0
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
                count += 1
            print(f"🗑️  已清理所有缓存 ({count} 个文件)")
            # 重置统计
            self.stats = {"hits": 0, "misses": 0, "sets": 0}

    def get_stats(self) -> Dict:
        """获取缓存统计"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "sets": self.stats["sets"],
            "hit_rate": f"{hit_rate:.2f}%",
            "total_requests": total_requests
        }

    def cleanup_expired(self):
        """清理过期缓存"""
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)

                cache_time = datetime.fromisoformat(cache_data['timestamp'])
                age_seconds = (datetime.now() - cache_time).total_seconds()

                if age_seconds > self.cache_duration:
                    cache_file.unlink()
                    count += 1
            except:
                continue

        if count > 0:
            print(f"🗑️  已清理 {count} 个过期缓存")

# 集成到分析系统
class CachedAnalyzer:
    """带缓存的异步分析器"""

    def __init__(self, max_concurrent: int = 3, cache_duration_hours: int = 24):
        self.cache = AnalysisCache(cache_duration_hours=cache_duration_hours)
        self.max_concurrent = max_concurrent

    async def analyze_with_cache(self, product_name: str) -> Dict:
        """带缓存的分析"""
        # 1. 尝试从缓存获取
        cached_result = self.cache.get(product_name)
        if cached_result:
            print(f"✅ 从缓存加载: {product_name}")
            return cached_result

        # 2. 缓存未命中，执行分析
        print(f"🔄 执行分析: {product_name}")
        # 这里调用实际的分析逻辑
        result = await self._actual_analysis(product_name)

        # 3. 保存到缓存
        self.cache.set(product_name, result)

        return result

    async def _actual_analysis(self, product_name: str) -> Dict:
        """实际分析逻辑（模拟）"""
        await asyncio.sleep(2)  # 模拟分析耗时
        return {
            "product": product_name,
            "status": "success",
            "data": f"分析结果...",
            "timestamp": datetime.now().isoformat()
        }

# 测试缓存效果
async def test_cache():
    """测试缓存"""
    import asyncio

    analyzer = CachedAnalyzer()

    print("🧪 缓存测试")
    print("=" * 60)

    # 第一次分析（未命中缓存）
    print("\n1️⃣ 第一次分析（缓存未命中）:")
    start = time.time()
    await analyzer.analyze_with_cache("iPhone 15")
    elapsed = time.time() - start
    print(f"   耗时: {elapsed:.2f}s")

    # 第二次分析（命中缓存）
    print("\n2️⃣ 第二次分析（缓存命中）:")
    start = time.time()
    await analyzer.analyze_with_cache("iPhone 15")
    elapsed = time.time() - start
    print(f"   耗时: {elapsed:.2f}s")

    # 查看缓存统计
    print("\n3️⃣ 缓存统计:")
    stats = analyzer.cache.get_stats()
    print(f"   命中: {stats['hits']}")
    print(f"   未命中: {stats['misses']}")
    print(f"   命中率: {stats['hit_rate']}")

    # 性能对比
    print("\n4️⃣ 性能对比:")
    products = ["Product_A", "Product_B", "Product_C"]

    # 无缓存
    print("   无缓存:")
    start = time.time()
    for product in products:
        await analyzer._actual_analysis(product)
    no_cache_time = time.time() - start
    print(f"   耗时: {no_cache_time:.2f}s")

    # 有缓存（第二次）
    print("   有缓存:")
    start = time.time()
    for product in products:
        await analyzer.analyze_with_cache(product)
    cache_time = time.time() - start
    print(f"   耗时: {cache_time:.2f}s")

    print(f"\n   加速比: {no_cache_time/cache_time:.2f}x")

# 主测试函数
async def main():
    """主测试函数"""
    print("⚡ 缓存机制演示")
    print("=" * 60)
    print()

    # 测试缓存
    await test_cache()

    # 清理测试
    print("\n🧹 清理测试缓存...")
    cache = AnalysisCache()
    cache.clear()

    print("\n" + "=" * 60)
    print("✅ 缓存机制演示完成")

# 运行测试
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())