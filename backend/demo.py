import json
import json_validator
def demo_tool(params):
    # 读取 JSON 文件
    with open("example.json", "r") as file:
        json_data = file.read()

    # 调用函数
    is_valid, result, conversation_id, msg, code, messages, output_key, output_value = (
        json_validator.validate_and_format_json(json_data)
    )

    if is_valid:
        # print("Valid JSON data:")
        # print(result)
        print("Conversation ID:", conversation_id)
        print("Message:", msg)
        print("Code:", code)

        # 处理 messages 列表
        if messages:
            print("Messages:")
            for message in messages:
                print("Message object:", message)
        else:
            print("No messages found.")

        # 输出 content_json 中的输出键和值
        if output_key and output_value:
            combined_string = f"收到消息：{params}\n---\n下面是一份测试数据\n---\n"
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
