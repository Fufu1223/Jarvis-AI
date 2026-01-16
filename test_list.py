# 1. 创建一个空列表 (用方括号 [])
chat_history = [] 

print("一开始的本子：", chat_history)

# 2. 往里加东西 (用 .append 指令)
chat_history.append("我是第一句")
chat_history.append("我是第二句")

print("现在的本子：", chat_history)

# 3. 怎么取出第一句？ (用索引 [0])
print("第一句是：", chat_history[0])