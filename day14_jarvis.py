import streamlit as st
from openai import OpenAI # <--- 1. 引入通讯工具

st.title("🤖 Jarvis v2.0 (流式打字机版)")

# --- A. 初始化 API (和昨天一样) ---
if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url=st.secrets["DEEPSEEK_BASE_URL"]
    )

# --- B. 初始化记忆 (和昨天一样) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- C. 回放历史 (和昨天一样) ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- D. 处理新消息 (核心修改区) ---
prompt = st.chat_input("请下达指令...")

if prompt:
    # 1. 显示用户的话
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. 调用 AI (流式版)
    with st.chat_message("assistant"):
        # 创建一个空的容器（占位符），等会儿我们要往这里面一点点填字
        message_placeholder = st.empty()
        full_response = ""  # 先准备一个空字符串，用来拼凑完整的回复

        try:
            # --- 关键改动 1: stream=True ---
            response = st.session_state.client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.messages,
                stream=True  # <--- 打开水龙头，让水流出来！
            )
            
            # --- 关键改动 2: 循环接收数据流 ---
            for chunk in response:
                # 从数据碎片中提取文字
                # 注意：流式模式下，内容在 delta.content 里，而不是 message.content
                content = chunk.choices[0].delta.content
                
                # 如果这一片有内容 (有时候是空的，比如结尾)
                if content:
                    full_response += content  # 拼接到总回复里
                    # 实时显示！加个 "▌" 模拟光标效果，看起来更酷
                    message_placeholder.markdown(full_response + "▌")
            
            # --- 循环结束 ---
            # 最后把光标去掉，显示最终的完整回复
            message_placeholder.markdown(full_response)
            
            # 3. 存入记忆 (存的是拼凑好的完整句子)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"出错了: {e}")