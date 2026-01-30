import streamlit as st
import time

#显示标题
st.title("复读机助手")

#显示侧边栏
user_input = st.sidebar.text_input("请输入")

#放置一个按钮 展示用户输入文字
if st.button("开始复读"):
    st.write(f"你刚才输入了: {user_input}")
