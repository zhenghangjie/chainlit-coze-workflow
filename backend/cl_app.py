import chainlit as cl
import json
import logging
import demo
import coze_caller
import bailian_caller

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


@cl.step(type="tool")
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )
    await cl.Message(
        content=json.dumps({"coze": "Hello coze", "bailian": "Hello bailian"})
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    coze_answer = "扣子正在生成..."
    bailian_answer = "百炼正在生成..."
    final_answer = await cl.Message(
        content=json.dumps({"coze": coze_answer, "bailian": bailian_answer})
    ).send()

    # Call coze agent
    await cl.sleep(2)
    coze_answer = await coze_caller.call_agent_app(message.content)
    final_answer.content = json.dumps(
        {
            "coze": coze_answer,
            "bailian": bailian_answer,
        }
    )
    await final_answer.update()
    # Call bailian agent
    await cl.sleep(2)
    bailian_answer = bailian_caller.call_agent_app(message.content)
    final_answer.content = json.dumps(
        {
            "coze": coze_answer,
            "bailian": bailian_answer,
        }
    )
    await final_answer.update()
