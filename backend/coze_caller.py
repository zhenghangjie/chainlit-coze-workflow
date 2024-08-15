import os
import httpx
import logging
import json_validator

# 获取环境变量
COZE_API_KEY = os.environ.get("COZE_API_TOKEN")

if COZE_API_KEY:
    print(f"Environment variable 'COZE_API_TOKEN' is set to: {COZE_API_KEY}")
else:
    print("The environment variable 'COZE_API_TOKEN' is not set.")


async def call_agent_app(input_str: str):
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
        # TODO 会话 ID
        "conversation_id": "111",
        "bot_id": "7402145891815702562",
        # TODO 用户 ID
        "user": "7433",
        "query": f"{input_str}",
        "stream": False,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers, timeout=600)

    logging.info("response data:\n%s", response.text)

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
            combined_string = f"工作流命中: {output_key}\n"
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
                    f"{discourse} \n"
                    f"{question} \n"
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