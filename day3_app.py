# day3_app.py
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
import time

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(
    page_title="AI智能助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .assistant-message {
        background-color: #f3e5f5;
    }
</style>
""", unsafe_allow_html=True)

# 初始化DeepSeek模型
@st.cache_resource
def init_deepseek_model():
    """初始化DeepSeek模型（缓存以提高性能）"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        st.error("❌ 请设置DEEPSEEK_API_KEY环境变量")
        st.stop()

    return ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=api_key,
        openai_api_base="https://api.deepseek.com",
        temperature=0.7,
    )

# 初始化Agent
@st.cache_resource
def init_agent(llm):
    """初始化Agent"""
    from langchain_core.tools import tool

    # 定义工具
    @tool
    def get_current_time(location: str = "") -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @tool
    def calculator(expression: str) -> str:
        """计算数学表达式"""
        try:
            import ast
            node = ast.parse(expression, mode='eval')
            for node in ast.walk(node):
                if isinstance(node, (ast.Call, ast.Attribute)):
                    raise ValueError("不允许函数调用")
            result = eval(expression, {"__builtins__": {}}, {})
            return f"{expression} = {result}"
        except Exception as e:
            return f"计算错误：{e}"

    tools = [get_current_time, calculator]

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt="你是一个有帮助的AI助手，可以使用工具来回答用户的问题。",
    )

# 侧边栏
def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.title("🤖 AI智能助手")
        st.write("---")

        # 系统提示词
        st.subheader("⚙️ 系统设置")
        system_prompt = st.text_area(
            "系统提示词",
            value="你是一个有帮助的AI助手，可以使用工具来回答用户的问题。",
            height=100,
            help="定义AI助手的角色和行为"
        )

        # 模型温度
        temperature = st.slider(
            "创造性（Temperature）",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="值越高，回答越有创造性"
        )

        st.write("---")

        # 使用统计
        st.subheader("📊 使用统计")
        if 'message_count' not in st.session_state:
            st.session_state.message_count = 0
        st.metric("消息数量", st.session_state.message_count)

        # 清除对话
        if st.button("🗑️ 清除对话"):
            st.session_state.messages = []
            st.session_state.message_count = 0
            st.rerun()

        st.write("---")

        # 关于
        st.subheader("ℹ️ 关于")
        st.write("""
        **技术栈**：
        - LangChain
        - DeepSeek
        - Streamlit

        **作者**：公众号:AI实战导航站
        """)

    return system_prompt, temperature

# 添加流式输出功能
def stream_response(agent, messages):
    """流式输出回复"""
    try:
        # 调用Agent
        inputs = {"messages": messages}
        response = agent.invoke(inputs)

        # 提取回复内容
        response_messages = response.get("messages", [])
        full_response = ""

        # 获取最后一条有内容的消息（AI的回复）
        for msg in reversed(response_messages):
            if hasattr(msg, 'content') and msg.content:
                full_response = msg.content
                break

        if not full_response:
            full_response = "抱歉，我没有生成回复。"

        # 模拟流式输出
        response_placeholder = st.empty()
        displayed_text = ""

        for char in full_response:
            displayed_text += char
            response_placeholder.markdown(displayed_text + "▌")
            time.sleep(0.01)  # 模拟打字效果

        response_placeholder.markdown(displayed_text)
        return full_response

    except Exception as e:
        error_msg = f"❌ 发生错误：{str(e)}"
        return error_msg

# 主函数
def main():
    """主函数"""
    # 渲染侧边栏
    system_prompt, temperature = render_sidebar()

    # 初始化模型和Agent
    try:
        llm = init_deepseek_model()
        agent = init_agent(llm)
    except Exception as e:
        st.error(f"❌ 初始化失败：{e}")
        st.stop()

    # 主标题
    st.title("💬 AI智能对话助手")
    st.write("基于LangChain和DeepSeek的智能Agent，支持工具调用和多轮对话")

    # 初始化会话状态
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 显示历史消息
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 用户输入
    if prompt := st.chat_input("请输入您的问题..."):
        # 显示用户消息
        with st.chat_message("user"):
            st.markdown(prompt)

        # 添加到历史
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.message_count += 1

        # AI回复
        with st.chat_message("assistant"):
            assistant_reply = stream_response(agent, st.session_state.messages)

            # 添加到历史
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_reply
            })

if __name__ == "__main__":
    main()