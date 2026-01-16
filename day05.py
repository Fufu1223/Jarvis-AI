from openai import OpenAI
from dotenv import load_dotenv
import os
# --- 配置部分 (Boilerplate) ---
load_dotenv("key.env")

api_key = os.getenv("DEEPSEEK_API_KEY")

# api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

# # --- 1. 初始化记忆 (创建一个空列表) ---
# # 我们先给它塞一个“人设”，这是第一条记忆
# messages = [
#     {"role": "system", "content": "你是一个毒舌但心地善良的吐槽役助手。"}
# ]

# print("=== 💀 毒舌 AI 已上线 (输入 'quit' 退出) ===")

# # --- 2. 开启无限循环 ---
# while True:
#     # A. 获取用户输入
#     user_input = input("\n🫵 你：")
    
#     # 增加一个退出机制：如果用户输入 quit 就结束
#     if user_input == "quit":
#         print("哼，这就跑了？再见！")
#         break  # break 用于打断循环

#     # B. 【关键】把用户说的话，追加(append)到记忆列表里
#     messages.append({"role": "user", "content": user_input})

#     # C. 把【整个列表】发给 AI (不仅仅是刚说的那句话)
#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=messages  # 注意：这里传的是整个 history
#     )

#     # D. 获取 AI 的回答
#     ai_reply = response.choices[0].message.content
    
#     # E. 【关键】把 AI 的回答，也追加到记忆列表里
#     # 这样下一次循环时，AI 就知道自己说过什么了
#     messages.append({"role": "assistant", "content": ai_reply})

#     # F. 打印出来
#     print(f"🤖 AI：{ai_reply}")
messages = [
    {"role": "system", "content": "你是一个毒舌但心地善良的助手"}
]

print("====毒蛇AI上线=====")

while True:
    user_input = input("您说：")
    
    # --- 退出通道 ---
    if user_input == "quit":
        print("再见！")
        break

    # --- 核心业务通道 (注意：所有代码都要和 if 开头对齐) ---
    
    # 1. 记下来你说的话
    messages.append({"role": "user", "content": user_input})

    # 2. 发给 AI (定义 response) <--- 你刚才可能少了这一段或者缩进错了
    print("AI 正在思考...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    # 3. 记下来 AI 说的话
    ai_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_reply})

    # 4. 打印出来
    print(f"AI: {ai_reply}")
