import streamlit as st

st.subheader("自动清空的备忘录 🧹")

# --- 1. 初始化列表 ---
if 'my_list' not in st.session_state:
    st.session_state.my_list = []

# --- 2. 定义一个“干活”的函数 (Callback) ---
# 这个函数平时不运行，只有被“召唤”时才运行
def add_and_clear():
    # A. 从 session_state 里拿到输入框的值 (通过 key)
    new_item = st.session_state.input_key
    
    # B. 如果有内容，就加到列表里
    if new_item:
        st.session_state.my_list.append(new_item)
        
    # C. 【关键一步】把输入框绑定的变量清空！
    st.session_state.input_key = ""

# --- 3. UI 布局 ---

# 注意 A：加了 key="input_key"。
# 这意味着：st.session_state.input_key 就代表了这个输入框的内容
st.text_input("请输入文本", key="input_key")

# 注意 B：加了 on_click=add_and_clear。
# 这意味着：点击按钮时，不要只是刷新，先去执行 add_and_clear 函数！
st.button("添加到列表", on_click=add_and_clear)

# --- 4. 显示结果 ---
st.write("---")
for item in st.session_state.my_list:
    st.write(f"✅ {item}")