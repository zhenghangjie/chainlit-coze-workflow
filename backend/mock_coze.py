import json_validator
def tool():
    # 读取 JSON 文件
    with open("example-coze.json", "r") as file:
        json_data = file.read()

    # 调用函数
    return json_validator.validate_and_format_json(json_data)
