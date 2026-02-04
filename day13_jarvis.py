import streamlit as st
from openai import OpenAI # <--- 1. 引入通讯工具

st.title("🤖 Jarvis v1.0 (已连接大脑)")

# --- A. 初始化 API 客户端 ---
# 这里的 secrets 就像是从那个 toml 文件里读取密码，非常安全
if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url=st.secrets["DEEPSEEK_BASE_URL"]
    )

# --- B. 初始化聊天记录 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- C. 回放历史聊天 ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- D. 处理用户输入 ---
prompt = st.chat_input("请下达指令...")

if prompt:
    # 1. 显示用户的话
    with st.chat_message("user"):
        st.write(prompt)
    # 2. 存入历史
    st.session_state.messages.append({"role": "user", "content": prompt})

    # --- 关键修改：调用真 AI ---
    with st.chat_message("assistant"):
        # 显示一个"思考中..."的转圈圈，体验更好
        with st.spinner("Jarvis 正在思考..."):
            
            try:
                # 3. 发送请求给 DeepSeek
                response = st.session_state.client.chat.completions.create(
                    model="deepseek-chat",  # 或者是 "deepseek-reasoner"
                    messages=st.session_state.messages, # 把之前的聊天记录都发给它，这样它才有上下文
                    stream=False # 今天先学不流式（一次性说完），明天学流式
                )
                
                # 4. 获取 AI 的回复内容
                ai_reply = response.choices[0].message.content
                
                # 5. 显示出来
                st.write(ai_reply)
                
                # 6. 存入历史
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            except Exception as e:
                st.error(f"连接大脑失败: {e}")