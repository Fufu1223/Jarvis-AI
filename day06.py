# with open("data.txt", "a", encoding="utf-8") as f:
#     f.write("系统启动成功\n")  # ✅ 前面有 4 个空格 (Tab)

# with open("data.txt", "r", encoding="utf-8") as f:
#     for line in f:
#         print(line.strip())

# try:

#     with open("secret.txt", "r", encoding="utf-8") as f:
#         for line in f:
#             print(line.strip())

# except FileNotFoundError:
#     print("[系统警告] 日志文件丢失，即将创建新文件...")

# import json

# chat_history = [{"user": "我", "msg": "你好"}, {"user": "AI", "msg": "在的"}]

# with open("memory.json", "w", encoding="utf-8") as f:

#     json.dump(chat_history, f, ensure_ascii=False, indent=4)

import json

with open("memory.json", "r", encoding="utf-8") as f:
    
    history = json.load(f)

for context in history:
    users = context.get("user")
    msgs = context.get("msg")

    print(f"{users}:{msgs}")







