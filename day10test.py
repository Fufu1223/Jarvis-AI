import json

# 1. 模拟 AI 发过来的原始数据（注意：这是红色的字符串！）
raw_text = '{"city": "上海", "date": "今天"}'

print(f"变身前，它是: {type(raw_text)}") 
# 输出: <class 'str'> (字符串，没法用 .get)

# 2. 执行那行关键代码！
args = json.loads(raw_text)

print(f"变身后，它是: {type(args)}") 
# 输出: <class 'dict'> (字典，可以用 .get 了！)

# 3. 验证一下
print(args.get("city"))  # 输出: 上海