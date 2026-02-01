import streamlit as st

st.title("🤖 我的第一个 AI 聊天界面")

# --- 1. 初始化聊天记录 (Session State) ---
# 这次我们叫它 'messages'，这是 AI 开发的行业术语
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. 展示历史聊天记录 (核心循环) ---
# 每次刷新页面，都要把“剧本”从头到尾演一遍
for msg in st.session_state.messages:
    # msg["role"] 会自动决定头像 (user 是人头，assistant 是机器人)
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 3. 处理用户输入 ---
# st.chat_input 是终极武器，它自带“自动清空”和“回车发送”
prompt = st.chat_input("说点什么...")

if prompt:  # 如果用户输入了内容 (隐含了 if prompt != "")
    
    # A. 把它显示在界面上 (即时反馈)
    with st.chat_message("user"):
        st.write(prompt)
    
    # B. 把它存进“长期记忆” (Session State)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # --- 4. 模拟 AI 回复 (今天先假装有一个 AI) ---
    response = f"我听到了，你说的是：{prompt} 🤖"
    
    # C. 显示 AI 的回复
    with st.chat_message("assistant"):
        st.write(response)
    
    # D. 把 AI 的回复也存进“长期记忆”
    st.session_state.messages.append({"role": "assistant", "content": response})

# 1. 创建一个名为 "assistant" 的气泡盒子 -> 屏幕上出现 🤖 图标的空盒子
with st.chat_message("assistant"):
    
    # 2. 在盒子里写字 -> 盒子里出现文字
    st.write("我是 AI，你好！")

with st.chat_message("woman"):
    
    # 2. 在盒子里写字 -> 盒子里出现文字
    st.write("我是woman，你好！")