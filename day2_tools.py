# day2_tools.py
# day2_tools.py
import aiohttp
import asyncio
from typing import List, Dict
import json

class WebSearchTool:
    """网络搜索工具（使用DuckDuckGo）"""

    def __init__(self):
        self.base_url = "https://duckduckgo.com/"

    async def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """异步搜索网络信息"""
        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_results(data, max_results)
                    else:
                        return [{"error": f"搜索失败: {response.status}"}]
        except Exception as e:
            return [{"error": f"搜索异常: {str(e)}"}]

    def _parse_results(self, data: Dict, max_results: int) -> List[Dict]:
        """解析搜索结果"""
        results = []

        # 提取摘要
        if data.get("AbstractText"):
            results.append({
                "title": "摘要",
                "content": data["AbstractText"],
                "url": data.get("AbstractURL", "")
            })

        # 提取相关主题
        for topic in data.get("RelatedTopics", [])[:max_results]:
            if isinstance(topic, dict) and "Text" in topic:
                results.append({
                    "title": topic.get("Name", "相关主题"),
                    "content": topic["Text"],
                    "url": topic.get("FirstURL", "")
                })

        return results[:max_results]

# 同步包装器（兼容LangChain）
def web_search(query: str) -> str:
    """同步搜索函数"""
    tool = WebSearchTool()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(tool.search(query))
        return json.dumps(results, ensure_ascii=False, indent=2)
    finally:
        loop.close()

# 测试代码
if __name__ == "__main__":
    print("🔍 测试网络搜索工具")
    print("=" * 60)

    result = web_search("AI Agent搜索一篇最热门的文章")
    print(result)


    print("✅ 搜索测试完成")