import json


def tool():
    # 读取 JSON 文件
    with open("example-bailian.json", "r") as file:
        json_data = file.read()

    return json.loads(json_data)
