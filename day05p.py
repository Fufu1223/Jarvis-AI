import os
from dotenv import load_dotenv

load_dotenv()

secret_code = os.getenv("SECRET_CODE")

print(secret_code)

users = [{"name": "A"}, {"name": "B"}]

for user in users:

    name = user.get("name")

    print(f"{name}")

