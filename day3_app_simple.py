# day3_app_simple.py - 简化版主应用（不依赖PyTorch）
import os
import streamlit as st
from dotenv import load_dotenv
import requests
import json

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

def call_deepseek_api(messages, temperature=0.7):
    """调用DeepSeek API"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        return "❌ 请设置DEEPSEEK_API_KEY环境变量"

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": temperature
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ 调用API失败：{str(e)}"

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
            value="你是一个有帮助的AI助手。",
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
        - DeepSeek API
        - Streamlit

        **作者**：公众号:AI实战导航站
        """)

        # Python版本提示
        st.write("---")
        st.warning("⚠️ 当前使用简化版（不依赖PyTorch）")
        st.info("💡 完整功能需要Python 3.10或3.11")

    return system_prompt, temperature

# 流式输出
def stream_response(messages, temperature):
    """流式输出回复"""
    try:
        response = call_deepseek_api(messages, temperature)

        # 模拟流式输出
        response_placeholder = st.empty()
        displayed_text = ""

        for char in response:
            displayed_text += char
            response_placeholder.markdown(displayed_text + "▌")
            import time
            time.sleep(0.01)

        response_placeholder.markdown(displayed_text)
        return response

    except Exception as e:
        error_msg = f"❌ 发生错误：{str(e)}"
        return error_msg

# 主函数
def main():
    """主函数"""
    # 渲染侧边栏
    system_prompt, temperature = render_sidebar()

    # 主标题
    st.title("💬 AI智能对话助手")
    st.write("基于DeepSeek API的智能助手（简化版）")

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
            assistant_reply = stream_response(st.session_state.messages, temperature)

            # 添加到历史
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_reply
            })

if __name__ == "__main__":
    main()