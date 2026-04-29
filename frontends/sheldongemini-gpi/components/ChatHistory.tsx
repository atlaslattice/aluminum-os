
import React, { useEffect, useRef } from 'react';
import { ChatMessage } from '../types';
import ChatMessageBubble from './ChatMessageBubble';

interface ChatHistoryProps {
  messages: ChatMessage[];
}

const ChatHistory: React.FC<ChatHistoryProps> = ({ messages }) => {
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
      {messages.map((msg, index) => (
        <ChatMessageBubble key={index} message={msg} />
      ))}
      <div ref={endOfMessagesRef} />
    </main>
  );
};

export default ChatHistory;
