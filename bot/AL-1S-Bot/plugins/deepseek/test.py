from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

client = OpenAI(api_key="sk-2d24c5d2a2314d61a56cef7c0dc99294", base_url="https://api.deepseek.com")
message: list[ChatCompletionMessageParam] = [{"role": "system", "content": "你是猫娘"}]
while True:
    user = input("text here: ")
    if user == "exit":
        break
    message.append({"role": "user", "content": user})
    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = message,
    )
    
    print(response.choices[0].message.content)
    ai_reply = response.choices[0].message.content
    message.append({"role": "assistant", "content": ai_reply})