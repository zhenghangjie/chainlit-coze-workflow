# validator 基础类
import json

def validate_and_format_json(json_data):
    try:
        # 尝试解析 JSON 字符串
        data = json.loads(json_data)
        
        # 确保 data 是字典类型
        if not isinstance(data, dict):
            raise ValueError("Parsed JSON is not a dictionary.")
        
        # 提取 conversation_id、msg 和 code
        # https://www.coze.cn/docs/developer_guides/chat#5c545459
        conversation_id = data.get('conversation_id')
        msg = data.get('msg')
        code = data.get('code')
        
        # 提取 messages 列表
        # https://www.coze.cn/docs/developer_guides/chat#2ae561e5
        messages = data.get('messages')
        
        # 查找第一个 type 为 'answer' 的对象
        answer_message = next((message for message in messages if message.get('type') == 'answer'), None)
        
        # 从找到的对象中提取 content 字段
        content = answer_message.get('content') if answer_message else None
        
        # 尝试将 content 转换为标准 JSON 结构
        content_json = None
        if content:
            try:
                content_json = json.loads(content)
            except json.JSONDecodeError as e:
                return False, f"Invalid JSON in content: {e}", None, None, None, None, None, None, None
        
        # 检查 long_recall_output、non_recall_output 和 short_recall_output
        output_key = None
        output_value = None
        
        # 遍历三个可能的键
        for key in ['long_recall_output', 'non_recall_output', 'short_recall_output']:
            if key in content_json and content_json[key]:
                output_key = key
                output_value = content_json[key]
                break
        
        # 返回原始数据和 conversation_id、msg、code、messages、output_key、output_value
        return True, data, conversation_id, msg, code, messages, output_key, output_value
    
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in file: {e}", None, None, None, None, None, None, None
    except KeyError:
        return False, "Missing required keys in JSON.", None, None, None, None, None, None, None
    except StopIteration:
        return False, "No 'answer' type message found.", None, None, None, None, None, None, None
    except Exception as e:
        return False, f"An error occurred: {e}", None, None, None, None, None, None, None