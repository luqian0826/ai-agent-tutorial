# day2_memory_agent.py
from day2_memory import AgentMemory
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import json

load_dotenv()

class MemoryEnhancedAgent:
    """带记忆的Agent"""

    def __init__(self, agent_name: str = "default"):
        self.agent_name = agent_name
        self.memory = AgentMemory(collection_name=f"{agent_name}_memory")

        # 初始化模型
        self.llm = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
            openai_api_base="https://api.deepseek.com",
            temperature=0.7
        )

        # LangChain对话记忆
        self.conversation_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # 创建基础工具
        tools = [
            Tool(
                name="get_memory",
                func=self._get_memory_str,
                description="获取相关的历史记忆"
            )
        ]

        # 创建Agent
        self.agent = create_agent(
            model=self.llm,
            tools=tools,
            system_prompt=f"""你是一个有帮助的AI助手，名字叫{agent_name}。
            你会记住用户的对话历史，并提供连贯的回答。
            你可以搜索相关的历史记忆来更好地理解用户的意图。"""
        )

    def _get_memory_str(self, query: str) -> str:
        """获取记忆的字符串形式"""
        memories = self.memory.search_memory(query, n_results=3)

        if not memories:
            return "没有找到相关的历史记忆。"

        result = "相关历史记忆：\n"
        for i, mem in enumerate(memories, 1):
            result += f"{i}. {mem['content'][:150]}...\n"

        return result

    def run_with_memory(self, user_input: str) -> str:
        """带记忆的运行"""
        # 1. 搜索相关记忆
        relevant_memories = self.memory.search_memory(user_input, n_results=2)

        # 2. 构建增强的提示词
        enhanced_prompt = self._build_enhanced_prompt(user_input, relevant_memories)

        # 3. 执行Agent
        try:
            inputs = {"messages": [{"role": "user", "content": enhanced_prompt}]}
            response = self.agent.invoke(inputs)

            # 获取回复
            messages = response.get("messages", [])
            agent_response = ""
            for msg in messages:
                if hasattr(msg, 'content') and msg.content:
                    agent_response += msg.content

            # 4. 存储到记忆
            self.memory.store_conversation(
                user_input=user_input,
                agent_response=agent_response,
                metadata={
                    "agent_name": self.agent_name,
                    "query_type": self._classify_query(user_input)
                }
            )

            # 5. 更新对话记忆
            self.conversation_memory.save_context(
                {"input": user_input},
                {"output": agent_response}
            )

            return agent_response

        except Exception as e:
            return f"发生错误: {str(e)}"

    def _build_enhanced_prompt(self, user_input: str,
                              memories: list) -> str:
        """构建增强提示词"""
        base_prompt = user_input

        if memories:
            memory_context = "\n\n相关历史对话：\n"
            for i, memory in enumerate(memories[:2], 1):
                memory_context += f"{i}. {memory['content'][:200]}...\n"

            base_prompt = memory_context + "\n当前问题：" + user_input

        return base_prompt

    def _classify_query(self, query: str) -> str:
        """分类查询类型"""
        query_lower = query.lower()

        if any(word in query_lower for word in ['价格', 'cost', '多少钱']):
            return "price_inquiry"
        elif any(word in query_lower for word in ['分析', 'analyze', 'report']):
            return "analysis"
        elif any(word in query_lower for word in ['搜索', 'search', 'find']):
            return "search"
        elif any(word in query_lower for word in ['帮助', 'help', '怎么']):
            return "help"
        else:
            return "general"

    def get_conversation_summary(self, hours: int = 24) -> Dict:
        """获取对话摘要"""
        recent_conversations = self.memory.get_recent_conversations(hours)

        summary = {
            "total_conversations": len(recent_conversations),
            "query_types": {},
            "common_topics": [],
            "timeline": []
        }

        # 统计查询类型
        for conv in recent_conversations:
            query_type = conv['metadata'].get('query_type', 'unknown')
            summary['query_types'][query_type] = \
                summary['query_types'].get(query_type, 0) + 1

        # 提取时间线
        for conv in recent_conversations[:10]:
            summary['timeline'].append({
                "time": conv['metadata'].get('timestamp', ''),
                "query": conv['metadata'].get('user_input', '')[:50]
            })

        return summary

# 测试代码
if __name__ == "__main__":
    print("💬 测试记忆增强Agent")
    print("=" * 60)

    agent = MemoryEnhancedAgent(agent_name="测试助手")

    # 模拟对话
    conversations = [
        "我叫张三，是一名程序员",
        "我正在学习AI Agent开发",
        "推荐一些学习资料",
        "我刚才提到我的名字了吗？"
    ]

    for i, user_input in enumerate(conversations, 1):
        print(f"\n{i}. 用户: {user_input}")
        response = agent.run_with_memory(user_input)
        print(f"   AI: {response[:100]}...")

    # 获取对话摘要
    print("\n" + "=" * 60)
    print("📊 对话摘要:")
    summary = agent.get_conversation_summary(hours=1)
    print(f"   总对话数: {summary['total_conversations']}")
    print(f"   查询类型: {summary['query_types']}")

    # 获取记忆统计
    print("\n🧠 记忆统计:")
    stats = agent.memory.get_memory_stats()
    print(f"   总记忆数: {stats.get('total_conversations', 0)}")

    print("\n" + "=" * 60)
    print("✅ 记忆增强Agent测试完成")