"use client";

import React, {
  useState,
  useRef,
  useEffect,
  FormEvent,
  KeyboardEvent,
  useContext,
} from "react";
import { MessageSquare, Send, X, Loader2, Bot } from "lucide-react";
import { AuthContext } from "@/app/AuthContext";
import useAxiosPublic from "@/hooks/AxiosPublic";
import BeautifyLLMOutput from "@/misc/LlmOutputParser";

interface ChatMessage {
  id: number;
  text: string;
  sender: "user" | "bot";
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: Date.now(), text: "Hello! How can I help you today?", sender: "bot" },
  ]);
  const [inputValue, setInputValue] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { currentUser, getIdToken } = useContext(AuthContext)!;
  const axiosPublic = useAxiosPublic();

  async function getLLMResponse(query: string): Promise<string> {
    console.log("Simulating API call for query:", query);
    const token = await getIdToken();
    const userId = currentUser?.uid;
    try {
      const response = await axiosPublic.post(
        "/api/v1/ai/chat",
        {
          question: query,
          session_id: userId,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status !== 200) {
        throw new Error(`API Error: ${response.statusText}`);
      }
      const data = await response;
      return data.data.answer || "Sorry, I couldn't get a response.";
    } catch (error) {
      console.error("API Call failed:", error);
      return "Sorry, I encountered an error trying to reach the AI.";
    }
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
      inputRef.current?.focus();
    }
  }, [messages, isOpen]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  const handleSendMessage = async (e?: FormEvent) => {
    if (e) e.preventDefault();
    const query = inputValue.trim();
    if (!query || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now(),
      text: query,
      sender: "user",
    };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);
    scrollToBottom();

    try {
      const botResponseText = await getLLMResponse(query);
      const botMessage: ChatMessage = {
        id: Date.now() + 1,
        text: botResponseText,
        sender: "bot",
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Failed to get bot response:", error);
      const errorMessage: ChatMessage = {
        id: Date.now() + 1,
        text: "Sorry, something went wrong. Please try again.",
        sender: "bot",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setTimeout(() => {
        inputRef.current?.focus();
        scrollToBottom();
      }, 0);
    }
  };

  const handleKeyPress = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Chat Trigger Button*/}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className={`fixed bottom-5 right-5 z-50 bg-gradient-to-br from-blue-500 to-blue-600 text-white p-4 rounded-full shadow-xl hover:from-blue-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75 transition-all duration-300 ease-in-out transform hover:scale-110 ${
            !currentUser ? "hidden" : ""
          }`}
          aria-label="Open Chat"
        >
          <MessageSquare size={24} />
        </button>
      )}

      {/* Chat Window */}
      <div
        className={`fixed bottom-20 right-5 z-50 w-80 md:w-96 h-[500px] bg-white rounded-lg shadow-2xl flex flex-col transition-all duration-300 ease-in-out transform ${
          isOpen
            ? "opacity-100 translate-y-0"
            : "opacity-0 translate-y-4 pointer-events-none"
        }`}
      >
        {/* Header*/}
        <div className="flex justify-between items-center p-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-t-lg shadow-sm">
          <h3 className="font-semibold text-lg">Chat With Your Files</h3>
          <button
            onClick={toggleChat}
            className="text-white hover:text-gray-200 focus:outline-none"
            aria-label="Close Chat"
          >
            <X size={20} />
          </button>
        </div>

        {/* Message Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div className="flex items-end max-w-[80%] gap-2">
                {message.sender === "bot" && (
                  <div className="flex-shrink-0 w-7 h-7 bg-blue-500 rounded-full flex items-center justify-center text-white mb-1">
                    <Bot size={16} />
                  </div>
                )}
                <div
                  className={`px-3 py-2 rounded-xl ${
                    message.sender === "user"
                      ? "bg-blue-500 text-white rounded-br-none"
                      : "bg-gray-200 text-gray-800 rounded-bl-none"
                  }`}
                  style={{
                    wordBreak: "break-word",
                    overflowWrap: "break-word",
                  }}
                >
                  {message.sender === "bot" ? (
                    <BeautifyLLMOutput text={message.text} />
                  ) : (
                    message.text
                  )}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex items-end max-w-[80%] gap-2">
                <div className="flex-shrink-0 w-7 h-7 bg-blue-500 rounded-full flex items-center justify-center text-white mb-1">
                  <Bot size={16} />
                </div>
                <div className="px-3 py-2 rounded-xl bg-gray-200 text-gray-500 rounded-bl-none">
                  <Loader2 className="w-5 h-5 animate-spin inline-block" />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <form
          onSubmit={handleSendMessage}
          className="p-3 border-t border-gray-200 bg-white rounded-b-lg"
        >
          <div className="flex items-center space-x-2">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition duration-200"
              disabled={isLoading}
              autoComplete="off"
            />
            <button
              type="submit"
              className={`p-2 rounded-full text-white transition-colors duration-200 ${
                isLoading || !inputValue.trim()
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-blue-500 hover:bg-blue-600"
              }`}
              disabled={isLoading || !inputValue.trim()}
              aria-label="Send Message"
            >
              <Send size={20} />
            </button>
          </div>
        </form>
      </div>
    </>
  );
};

export default Chatbot;
