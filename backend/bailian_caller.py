import os
from http import HTTPStatus
from dashscope import Application
import logging
import mock_bailian
import json

# 获取环境变量
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_TOKEN")

if DASHSCOPE_API_KEY:
    print(f"Environment variable 'DASHSCOPE_API_TOKEN' is set to: {DASHSCOPE_API_KEY}")
else:
    print("The environment variable 'DASHSCOPE_API_TOKEN' is not set.")


def request(input_str):
    response = Application.call(
        app_id="fc8c05aa44cd47c0bc13233fd0ca4538",
        prompt=input_str,
        api_key=DASHSCOPE_API_KEY,
    )

    if response.status_code != HTTPStatus.OK:
        return "request_id=%s, code=%s, message=%s\n" % (
            response.request_id,
            response.status_code,
            response.message,
        )
    else:
        return response.output.text


def call_agent_app(input_str: str):
    rendered_items = ""
    try:
        # 尝试解析 JSON 字符串
        # message = request(input_str)
        # logging.info("bailian response data:\n%s", message)
        # data = json.loads(message)
        # TODO mock data
        data = mock_bailian.tool()

        
        # 确保 data 是字典类型
        if not isinstance(data, dict):
            raise ValueError("Parsed JSON is not a dictionary.")
        content = data.get("content")
        items = data.get("items")
        

        for item in items:
            rendered_item = (
                f"Question: {item['stem']}\n"
                f"Options:\n"
                + "\n".join(
                    f"  {key}: {value}" for key, value in item["options"].items()
                )
                + f"\nAnswer: {item['answer']}\n"
                f"Analysis Topic: {item['analysis']['topic']}\n"
                f"Analysis Details: {item['analysis']['details']}\n\n"
            )
        rendered_items += rendered_item
        return (
            f"{content} \n"
            # 循环渲染 items
            f"{rendered_items}"
        )

    except json.JSONDecodeError as e:
        logging.error("bailian response error:\n%s", e)
        rendered_items = f"Invalid JSON: {e}"

    return rendered_items
