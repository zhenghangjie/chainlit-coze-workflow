import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { v4 as uuidv4 } from "uuid";
import { Rate } from 'antd';

import {
  useChatInteract,
  useChatMessages,
  IStep,
} from "@chainlit/react-client";
import { useState, useRef, useEffect } from "react";

export function Playground() {
  const [inputValue, setInputValue] = useState("");
  // 上一次输入
  const [prevInputValue, setPrevInputValue] = useState("");
  const { sendMessage } = useChatInteract();
  const { messages } = useChatMessages();

  const cozeMessageListRef = useRef<HTMLDivElement>(null);
  const blMessageListRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    const content = inputValue.trim();
    if (content) {
      const message = {
        name: "user",
        type: "user_message" as const,
        output: content,
      };
      sendMessage(message, []);
      setPrevInputValue(inputValue)
      setInputValue("");
    }
  };

  const scrollToBottom = () => {
    if (cozeMessageListRef.current && blMessageListRef.current) {
      cozeMessageListRef.current.scrollTop = cozeMessageListRef.current.scrollHeight;
      blMessageListRef.current.scrollTop = blMessageListRef.current.scrollHeight;
    }
  };

  const handleClick = (value: number, info: string) => {
    console.log('评分等级:', value);
    console.log('上一次输入:', prevInputValue);
    console.log('当前输出:', info);
  };

  const renderMessage = (message: IStep, source: string) => {
    const dateOptions: Intl.DateTimeFormatOptions = {
      hour: "2-digit",
      minute: "2-digit",
    };
    const date = new Date(message.createdAt).toLocaleTimeString(
      undefined,
      dateOptions
    );
    let info
    try {
      info = JSON.parse(message.output)[source]
    } catch (error) {
      info = message.output
    }
    return (
      <div key={message.id} className="flex flex-col">
        <div className="w-20 text-sm text-green-500 p-2">{message.name}</div>
        <div className="flex-1 border rounded-lg p-2">
          <p className="text-black dark:text-white whitespace-pre-wrap">{info}</p>
          <div className="flex justify-between">
            <small className="text-xs text-gray-500">{date}</small>
            {message.name === 'Assistant' ? (
              <div
                className="flex items-center"
                // onClick={() => { handleClick(info) }}
              >
                <span className="text-xs text-gray-500 mr-1">评价此次结果</span>
                <Rate allowHalf onChange={(value) => { handleClick(value, info) }} />
              </div>
            ) : null}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 flex flex-col overflow-hidden h-lvh">
      <div className="flex flex-row flex-1 overflow-auto">
        <div className="flex-1 overflow-auto p-6" ref={cozeMessageListRef}>
          <div className="space-y-4">
            {messages.map((message) => renderMessage(message, 'coze'))}
          </div>
        </div>
        <div className="flex-1 overflow-auto p-6" ref={blMessageListRef}>
          <div className="space-y-4">
            {messages.map((message) => renderMessage(message, 'bailian'))}
          </div>
        </div>
      </div>
      <div className="border-t p-4 bg-white dark:bg-gray-800">
        <div className="flex items-center space-x-2">
          <Input
            autoFocus
            className="flex-1"
            id="message-input"
            placeholder="Type a message"
            value={inputValue || '按照人设要求，生成一段短对话英语听力题，对话内容限制在20到40词，统计对话内容的次数和问答次数'}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyUp={(e) => {
              if (e.key === "Enter") {
                handleSendMessage();
              }
            }}
          />
          <Button onClick={handleSendMessage} type="submit">
            Send
          </Button>
        </div>
      </div>
    </div>
  );
}
