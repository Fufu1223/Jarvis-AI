import streamlit as st
from openai import OpenAI
import json
import os
from typing import List, Dict, Any

# --- 1. 配置与工具区 (The Engine Room) ---

# 定义常量：存档文件名
HISTORY_FILE = "chat_history.json"

def load_history() -> List[Dict[str, Any]]:
    """
    程序启动时：从本地 JSON 文件读取历史记录。
    如果文件不存在，返回空列表。
    """
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # 如果文件损坏（比如空的），就返回空列表，防止报错
            return []
    return []

def save_history(messages: List[Dict[str, Any]]) -> None:
    """
    每次对话后：将内存中的对话记录保存到本地 JSON 文件。
    """
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

def get_strategic_history(full_history: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
    """
    发送给 API 前：截取最近 N 条记录，节省 Token。
    """
    return full_history[-limit:]

# --- 2. 界面设置 (The Frontend) ---

st.title("🤖 Jarvis v3.1 (永久记忆版)")

# 人设库
personas = {
    "普通助手": "你是一个有用的 AI 助手。",
    "Python 专家": "你是一个资深的 Python 全栈工程师。代码必须包含详细中文注释。",
    "雅思口语教练": "你是一个严厉的雅思口语考官。请用英语对话并纠正我的语法。",
    "暴躁老哥": "你是一个脾气暴躁的网友，说话喜欢用反问句，但建议都很中肯。"
}

with st.sidebar:
    st.header("🎭 角色切换")
    selected_role = st.selectbox("选择人设", list(personas.keys()))
    system_prompt = personas[selected_role]
    
    # 添加一个按钮，允许用户手动清空记忆
    if st.button("🗑️ 清空所有记忆"):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)  # 删文件
        st.session_state.messages = [] # 清内存
        st.rerun() # 刷新页面

# --- 3. 核心逻辑 (The Main Loop) ---

# 初始化 API 客户端
if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        api_key=st.secrets["DEEPSEEK_API_KEY"],
        base_url=st.secrets["DEEPSEEK_BASE_URL"]
    )

# 初始化消息记录 (关键修改：不再是 []，而是尝试从文件读取！)
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# 渲染历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 处理用户输入
prompt = st.chat_input("说点什么...")

if prompt:
    # 1. 显示用户输入
    with st.chat_message("user"):
        st.write(prompt)
    
    # 2. 记录到内存 (Session State)
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 3. 立即同步到硬盘 (JSON)
    save_history(st.session_state.messages) 

    # 4. 呼叫 AI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 组装消息：System Prompt + 最近 5 条历史
        messages_to_send = [
            {"role": "system", "content": system_prompt}
        ] + get_strategic_history(st.session_state.messages)

        try:
            stream = st.session_state.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages_to_send,
                stream=True
            )
            
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # 5. 记录 AI 回复到内存
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            # 6. 再次同步到硬盘 (确保 AI 的话也被记住)
            save_history(st.session_state.messages)

        except Exception as e:
            st.error(f"连接失败: {e}")