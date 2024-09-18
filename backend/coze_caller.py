import os
import httpx
import logging
import json_validator
import mock_coze

# 获取环境变量
COZE_API_KEY = os.environ.get("COZE_API_TOKEN")

if COZE_API_KEY:
    print(f"Environment variable 'COZE_API_TOKEN' is set to: {COZE_API_KEY}")
else:
    print("The environment variable 'COZE_API_TOKEN' is not set.")


async def request(input_str: str):
    url = "https://api.coze.cn/open_api/v2/chat"
    headers = {
        "Authorization": f"Bearer {COZE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Host": "api.coze.cn",
        "Connection": "keep-alive",
    }
    data = {
        # TODO 会话 ID
        "conversation_id": "123",
        "bot_id": "7402145891815702562",
        # TODO 用户 ID
        "user": "7433",
        "query": f"{input_str}",
        "stream": False,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers, timeout=600)
    logging.info("coze response data:\n%s", response.text)

    return json_validator.validate_and_format_json(response.text)


async def call_agent_app(message: str):

    # 格式化响应内容
    is_valid, result, conversation_id, msg, code, messages, output_key, output_value = (
        await request(message)
    )
    # TODO mock data
    # is_valid, result, conversation_id, msg, code, messages, output_key, output_value = (
    #     mock_coze.tool()
    # )

    if is_valid:
        # print("Conversation ID:", conversation_id)
        # print("Message:", msg)
        # print("Code:", code)
        if output_key and output_value:
            # 初始化 combined_string 用于拼接结果
            combined_string = ""
            # combined_string = f"工作流命中: {output_key}\n"
            keys = [
                "question_types",
                "discourse",
                "question",
                "analysis",
                "source",
                "level",
            ]
            values = [output_value.get(key) for key in keys]
            question_types, discourse, question, analysis, source, level = values
            # 拼接成一个字符串
            item_string = (
                f"types: {question_types} \n"
                f"{discourse} \n"
                f"Question: {question} \n"
                f"Analysis: {analysis} \n"
                f"level: {level} \n\n"
                # f"source: {source} \n\n"
            )

            # 将 item_string 拼接到 combined_string
            combined_string += item_string

        else:
            print("No valid output found.")
    else:
        print("Error:", result)

    return combined_string
