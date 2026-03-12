# day2_memory.py
import chromadb
from chromadb.config import Settings
from datetime import datetime, timedelta
import hashlib
from typing import List, Dict
import json
from pathlib import Path

class AgentMemory:
    """Agent长期记忆系统"""

    def __init__(self, collection_name: str = "agent_conversations", persist_dir: str = "./chroma_db"):
        # 确保持久化目录存在
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(exist_ok=True)

        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(self.persist_dir)
        ))

        # 创建或获取集合
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "AI Agent对话记忆"}
        )

    def store_conversation(self, user_input: str, agent_response: str,
                          metadata: Dict = None) -> str:
        """存储对话到记忆"""
        # 生成唯一ID
        timestamp = datetime.now().isoformat()
        content_hash = hashlib.md5(
            f"{user_input}{agent_response}".encode()
        ).hexdigest()[:8]

        doc_id = f"{timestamp}_{content_hash}"

        # 准备元数据
        if metadata is None:
            metadata = {}

        metadata.update({
            "timestamp": timestamp,
            "user_input": user_input[:100],  # 截断保存
            "response_length": len(agent_response)
        })

        # 存储到向量数据库
        self.collection.add(
            documents=[agent_response],
            metadatas=[metadata],
            ids=[doc_id]
        )

        return doc_id

    def search_memory(self, query: str, n_results: int = 5) -> List[Dict]:
        """搜索相关记忆"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            memories = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    memory = {
                        "content": doc,
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i]
                    }
                    memories.append(memory)

            return memories
        except Exception as e:
            print(f"记忆搜索失败: {e}")
            return []

    def get_recent_conversations(self, hours: int = 24) -> List[Dict]:
        """获取最近对话"""
        try:
            # 获取所有记忆
            all_data = self.collection.get()

            recent_memories = []
            cutoff_time = datetime.now() - timedelta(hours=hours)

            for i, metadata in enumerate(all_data['metadatas']):
                if 'timestamp' in metadata:
                    memory_time = datetime.fromisoformat(metadata['timestamp'])
                    if memory_time > cutoff_time:
                        recent_memories.append({
                            "content": all_data['documents'][i],
                            "metadata": metadata,
                            "id": all_data['ids'][i]
                        })

            # 按时间排序
            recent_memories.sort(
                key=lambda x: x['metadata'].get('timestamp', ''),
                reverse=True
            )

            return recent_memories[:20]  # 返回最近20条
        except Exception as e:
            print(f"获取最近对话失败: {e}")
            return []

    def cleanup_old_memories(self, days: int = 7):
        """清理旧记忆（保持7天）"""
        try:
            all_data = self.collection.get()
            cutoff_time = datetime.now() - timedelta(days=days)

            ids_to_delete = []
            for i, metadata in enumerate(all_data['metadatas']):
                if 'timestamp' in metadata:
                    memory_time = datetime.fromisoformat(metadata['timestamp'])
                    if memory_time < cutoff_time:
                        ids_to_delete.append(all_data['ids'][i])

            if ids_to_delete:
                self.collection.delete(ids=ids_to_delete)
                print(f"已清理 {len(ids_to_delete)} 条旧记忆")

        except Exception as e:
            print(f"清理记忆失败: {e}")

    def get_memory_stats(self) -> Dict:
        """获取记忆统计信息"""
        try:
            all_data = self.collection.get()
            total_count = len(all_data['ids'])

            # 统计最近对话
            recent_24h = len(self.get_recent_conversations(hours=24))
            recent_7d = len(self.get_recent_conversations(hours=168))

            return {
                "total_conversations": total_count,
                "last_24_hours": recent_24h,
                "last_7_days": recent_7d,
                "collection_name": self.collection.name
            }
        except Exception as e:
            return {"error": f"获取统计信息失败: {str(e)}"}

# 测试代码
if __name__ == "__main__":
    print("🧠 测试记忆系统")
    print("=" * 60)

    memory = AgentMemory(collection_name="test_memory")

    # 测试存储
    print("1. 存储对话记忆...")
    doc_id = memory.store_conversation(
        user_input="今天天气怎么样？",
        agent_response="今天天气晴朗，气温25度，适合外出。",
        metadata={"type": "weather"}
    )
    print(f"   文档ID: {doc_id}")

    doc_id = memory.store_conversation(
        user_input="推荐一部电影",
        agent_response="推荐《肖申克的救赎》，这是一部经典励志电影。",
        metadata={"type": "entertainment"}
    )
    print(f"   文档ID: {doc_id}")

    # 测试搜索
    print("\n2. 搜索相关记忆...")
    results = memory.search_memory("天气", n_results=2)
    print(f"   找到 {len(results)} 条相关记忆")
    for i, mem in enumerate(results, 1):
        print(f"      {i}. {mem['content'][:50]}...")

    # 测试获取最近对话
    print("\n3. 获取最近对话...")
    recent = memory.get_recent_conversations(hours=24)
    print(f"   最近24小时有 {len(recent)} 条对话")

    # 测试统计
    print("\n4. 获取记忆统计...")
    stats = memory.get_memory_stats()
    print(f"   总对话数: {stats.get('total_conversations', 0)}")
    print(f"   最近24小时: {stats.get('last_24_hours', 0)}")
    print(f"   最近7天: {stats.get('last_7_days', 0)}")

    print("\n" + "=" * 60)
    print("✅ 记忆系统测试完成")
