import time

def fake_ai_brain(question):
    print("🤖 AI 正在思考中...")
    time.sleep(2)
    return "我听到了你的问题：" + question

print("=== AI 客服启动 ===")
user_input = input("请输入你的问题：")
answer = fake_ai_brain(user_input)
print("----------------")
print("AI 回答：" + answer)