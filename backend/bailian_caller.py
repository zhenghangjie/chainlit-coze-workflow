import os
from http import HTTPStatus
from dashscope import Application

# 获取环境变量
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_TOKEN")

if DASHSCOPE_API_KEY:
    print(f"Environment variable 'DASHSCOPE_API_TOKEN' is set to: {DASHSCOPE_API_KEY}")
else:
    print("The environment variable 'DASHSCOPE_API_TOKEN' is not set.")


def call_agent_app(input_str: str):
    # return 'bailian_caller'
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
