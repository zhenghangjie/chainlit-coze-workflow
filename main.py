import chainlit as cl
import httpx
import json
import json_validator

import os

# 获取环境变量
COZE_API_KEY = os.environ.get("COZE_API_KEY")

if COZE_API_KEY:
    print(f"Environment variable 'YOUR_ENV_VAR' is set to: {COZE_API_KEY}")
else:
    print("The environment variable 'YOUR_ENV_VAR' is not set.")


@cl.step(type="tool")
async def tool():
    # return 'coze'
    url = "https://api.coze.cn/open_api/v2/chat"
    headers = {
        "Authorization": f"Bearer {COZE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Host": "api.coze.cn",
        "Connection": "keep-alive",
    }
    data = {
        "conversation_id": "111",
        "bot_id": "7402145891815702562",
        "user": "7433",
        "query": "生成一段短对话",
        "stream": False,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers, timeout=600)

    # 格式化响应内容
    is_valid, result, conversation_id, msg, code, messages, output_key, output_value = (
        json_validator.validate_and_format_json(response.text)
    )
    if is_valid:
        # print("Conversation ID:", conversation_id)
        # print("Message:", msg)
        # print("Code:", code)
        if output_key and output_value:
            # 初始化一个空字符串用于拼接结果
            combined_string = ""
            for item in output_value:
                # 尝试解析 content 为 JSON 字典
                content_dict = item.get("content", {})

                # 获取各个属性
                question_types = content_dict.get("question_types", [])
                discourse = content_dict.get("discourse", "")
                question = content_dict.get("question", "")
                analysis = content_dict.get("analysis", "")
                source = content_dict.get("source", "")

                # 拼接成一个字符串
                item_string = (
                    f"题型: {question_types} \n"
                    f"语篇: {discourse} \n"
                    f"提问: {question} \n"
                    f"解析: {analysis} \n"
                    f"来源: {source} \n\n"
                )

                # 将 item_string 拼接到 combined_string
                combined_string += item_string
        else:
            print("No valid output found.")
    else:
        print("Error:", result)

    return combined_string


async def tool_fake():
    # Fake tool
    await cl.sleep(2)
    return "Response from the tool!"


@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends back an intermediate response from the tool, followed by the final answer.

    Args:
        message: The user's message.

    Returns:
        None.
    """
    final_answer = await cl.Message(
        content=f"收到指令: {message.content} \n内容正在生成中...",
    ).send()

    # Call the tool
    final_answer.content = await tool()

    await final_answer.update()
