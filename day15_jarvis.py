import streamlit as st
from openai import OpenAI

st.title("🤖 Jarvis v3.0 (百变大咖版)")

# --- 1. 定义角色字典 (人设库) ---
# 这是一个字典，左边是显示在菜单里的名字，右边是给 AI 的上帝指令
personas = {
    "普通助手": "你是一个有用的 AI 助手。",
    "Python 专家": "你是一个资深的 Python 全栈工程师。你只回答编程相关的问题。如果用户问其他问题（如做饭、天气），请礼貌拒绝。你的代码必须包含详细的中文注释。",
    "雅思口语教练": "你是一个严厉的雅思口语考官。请用英语和我对话，并指出我的语法错误。不要用中文回答，除非我特别要求。",
    "暴躁老哥": "你是一个脾气暴躁的网友，说话喜欢用反问句，这也不懂那也不懂。但是最后你还是会给出正确的建议。"
}

# --- 2. 侧边栏设置 ---
# st.sidebar 让组件显示在左侧，不会干扰主聊天界面
with st.sidebar:
    st.header("🎭 角色切换")
    selected_role = st.selectbox("请选择 Jarvis 的人格：", list(personas.keys()))
    
    # 拿到对应的系统提示词
    system_prompt = personas[selected_role]
    
    # 显示当前提示词（调试用，让自己看到设定了什么）
    with st.expander("查看当前人设指令"):
        st.write(system_prompt)

# --- 3. 初始化 (同之前) ---
if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url=st.secrets["DEEPSEEK_BASE_URL"]
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. 回放历史 (同之前) ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 5. 处理输入 ---
prompt = st.chat_input("请下达指令...")

if prompt:
    # 显示并记录用户输入
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用 AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # --- 关键修改：构建包含 System Prompt 的消息列表 ---
        # 技巧：列表相加 [A] + [B, C] = [A, B, C]
        # 我们临时拼凑一个列表发给 AI，但不会把它存进 session_state.messages
        # 这样"上帝指令"不仅生效了，还不会出现在网页的历史记录里
        messages_to_send = [
            {"role": "system", "content": system_prompt}
        ] + st.session_state.messages

        try:
            response = st.session_state.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages_to_send, # <--- 注意这里发的是拼凑好的列表
                stream=True
            )
            
            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # 记录回复
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"出错了: {e}")