# day2_agent.py
import os

#引入搜索功能
from day2_utils.day2_tools import web_search
#文件读写工具

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


# 1. 加载环境变量
load_dotenv()

# 2. 初始化DeepSeek模型
def init_deepseek_model():
    """初始化DeepSeek模型"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请设置DEEPSEEK_API_KEY环境变量")

    # DeepSeek兼容OpenAI API格式
    return ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=api_key,
        openai_api_base="https://api.deepseek.com",
        temperature=0.7,
    )

# 3. 定义工具
def get_current_time(location: str = "") -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def summarize_text(text: str) -> str:
    """总结文本内容"""
    # 这里先简单返回，Day 2会完善
    return f"总结：{text[:100]}..."


# 4. 创建工具列表
tools = [get_current_time, summarize_text,web_search]

# 5. 主函数
def main():
    print("🎯 欢迎使用你的第一个AI Agent！")
    print("=" * 50)

    # 初始化模型
    print("正在初始化DeepSeek模型...")
    llm = init_deepseek_model()

    # 创建Agent
    print("创建Agent中...")
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="你是一个有帮助的AI助手，可以使用工具来回答用户的问题。",
    )

    print("✅ Agent创建成功！")
    print("=" * 50)

    # 测试对话
    while True:
        try:
            user_input = input("\n🤖 你想问什么？（输入'退出'结束）: ")

            if user_input.lower() in ['退出', 'exit', 'quit']:
                print("👋 再见！")
                break

            if not user_input.strip():
                continue

            print("\n" + "=" * 50)
            print("🤖 AI Agent回复：")

            # 使用新的 API 调用方式
            inputs = {"messages": [{"role": "user", "content": user_input}]}
            response = agent.invoke(inputs)

            # 获取所有消息并打印
            messages = response.get("messages", [])
            for msg in messages:
                if hasattr(msg, 'content') and msg.content:
                    print(msg.content)

            print("\n" + "=" * 50)

        except KeyboardInterrupt:
            print("\n👋 用户中断，再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误：{e}")
            print("请检查：1. API密钥 2. 网络连接 3. 输入格式")

if __name__ == "__main__":
    main()