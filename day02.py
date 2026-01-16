# # 定义四个变量
# ai_name = "DeepSeek"
# token_count = 100
# price = 0.02
# is_online = True

# # 使用 type() 查看它们的身份
# print(type(ai_name))
# print(type(token_count))
# print(type(price))
# print(type(is_online))

# age = input("请输入你的年龄：")

# # 1. 进门变身：把 str 变成 int
# real_age = int(age) 

# # 2. 现在可以做数学计算了
# next_year = real_age + 1

print("=== AI 提示词生成器 v1.0 ===")

# 1. 获取三个关键变量 (全部是 str)
role = input("你想让 AI 扮演什么角色？(例如：英语老师)：")
topic = input("你要学习的主题是什么？(例如：过去式)：")
level = input("你的当前水平是？(例如：幼儿园)：")
ret = input("你希望ai回复你多少个字：")

# 2. 核心：使用 f-string 组装复杂的 Prompt
# 注意：f-string 支持换行（三引号 f"""..."""），这在 AI 开发中非常常用
final_prompt = f"""
你现在是一位专业的【{role}】。
请用【{level}】的水平，简单易懂地向我解释什么是【{topic}】。
要求：
1. 多用比喻。
2. 只要输出解释，不要废话。
3. 请把字数严格控制在{ret}个字以内
"""

# 3. 输出结果
print("----------------")
print("✅ 生成的提示词如下 (你可以直接复制发给 AI)：")
print(final_prompt)