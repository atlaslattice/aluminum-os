
import React from 'react';
import { ChatMessage, MessageRole } from '../types';
import { UserIcon, SheldonIcon, LoadingIndicator } from './Icons';

interface ChatMessageBubbleProps {
  message: ChatMessage;
}

const ChatMessageBubble: React.FC<ChatMessageBubbleProps> = ({ message }) => {
  const isUser = message.role === MessageRole.USER;
  const isLoading = message.role === MessageRole.MODEL && message.text === '';

  const wrapperClasses = isUser ? 'justify-end' : 'justify-start';
  const bubbleClasses = isUser
    ? 'bg-blue-600 rounded-br-none'
    : 'bg-gray-700 rounded-bl-none';
  const icon = isUser ? <UserIcon /> : <SheldonIcon />;

  // A very basic markdown-to-html renderer
  const renderText = (text: string) => {
    const bolded = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    const italicized = bolded.replace(/\*(.*?)\*/g, '<em>$1</em>');
    const codeBlock = italicized.replace(/```([\s\S]*?)```/g, '<pre class="bg-gray-800 p-2 rounded-md my-2 overflow-x-auto"><code>$1</code></pre>');
    const inlineCode = codeBlock.replace(/`(.*?)`/g, '<code class="bg-gray-800 px-1 py-0.5 rounded text-sm">$1</code>');
    return { __html: inlineCode.replace(/\n/g, '<br />') };
  };

  return (
    <div className={`flex items-end gap-3 w-full ${wrapperClasses}`}>
      {!isUser && <div className="flex-shrink-0">{icon}</div>}
      <div
        className={`max-w-xs md:max-w-xl lg:max-w-2xl px-4 py-3 rounded-2xl text-white shadow-md ${bubbleClasses}`}
      >
        {isLoading ? (
          <LoadingIndicator />
        ) : (
          <p className="text-sm md:text-base leading-relaxed break-words prose-invert" dangerouslySetInnerHTML={renderText(message.text)} />
        )}
      </div>
      {isUser && <div className="flex-shrink-0">{icon}</div>}
    </div>
  );
};

export default ChatMessageBubble;
