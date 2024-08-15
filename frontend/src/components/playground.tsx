import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { v4 as uuidv4 } from "uuid";

import {
  useChatInteract,
  useChatMessages,
  IStep,
} from "@chainlit/react-client";
import { useState } from "react";

export function Playground() {
  const [inputValue, setInputValue] = useState("");
  const { sendMessage } = useChatInteract();
  const { messages } = useChatMessages();

  const handleSendMessage = () => {
    const content = inputValue.trim();
    if (content) {
      const message = {
        name: "user",
        type: "user_message" as const,
        output: content,
      };
      sendMessage(message, []);
      setInputValue("");
    }
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
    console.log(message)
    let info
    try {
      info = JSON.parse(message.output)[source]
    } catch (error) {
      info = message.output
    }
    return (
      <div key={message.id} className="flex items-start space-x-2">
        <div className="w-20 text-sm text-green-500">{message.name}</div>
        <div className="flex-1 border rounded-lg p-2">
          <p className="text-black dark:text-white whitespace-pre-wrap">{info}</p>
          <small className="text-xs text-gray-500">{date}</small>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 flex flex-col">
      <div className="flex flex-row flex-1 overflow-auto">
        <div className="flex-1 overflow-auto p-6">
          <div className="space-y-4">
            {messages.map((message) => renderMessage(message, 'coze'))}
          </div>
        </div>
        <div className="flex-1 overflow-auto p-6">
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
            value={inputValue || '生成一段短对话英语听力题'}
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
