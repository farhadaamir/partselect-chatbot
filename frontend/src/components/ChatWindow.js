import React, { useState, useEffect, useRef } from "react";
import "./ChatWindow.css";
import { getAIMessage } from "../api/api";
import { marked } from "marked";

function ChatWindow() {

  const defaultMessage = [
    {
      role: "assistant",
      content: "PartsAI, at your service!",
    },
  ];
  // use loading state if loading dots implemented

  const [messages, setMessages] = useState(defaultMessage);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false); 
  console.log(messages)
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);


  const handleSend = async () => {
    if (typeof input !== "string" || !input.trim()) return;

    setMessages(prevMessages => [...prevMessages, { role: "user", content: input }]);
    setInput("");

    try {
        const reader = await getAIMessage(input);
        let fullResponse = "";
        setMessages(prevMessages => [...prevMessages, { role: "assistant", content: "" }]);

        for await (const chunk of reader) {
            fullResponse += chunk;

            setMessages(prevMessages => {
                const updatedMessages = [...prevMessages];
                const lastIndex = updatedMessages.length - 1;

                if (updatedMessages[lastIndex].role === "assistant") {
                    updatedMessages[lastIndex].content = fullResponse;
                }

                return updatedMessages;
            });
        }
    } catch (error) {
        console.error("Error displaying message:", error);
        setMessages(prevMessages => [
            ...prevMessages.slice(0, -1),
            { role: "assistant", content: "Error: Could not fetch response." },
        ]);
    }
};


  return (
      <div className="messages-container">
          
   
      {messages.map((message, index) => (
        <div key={index} className={`${message.role}-message-container`}>

          <div className={`message ${message.role}-message`}>

            <div dangerouslySetInnerHTML={{ __html: marked(message.content).replace(/<p>|<\/p>/g, "") }}></div>
          </div>
        </div>
      ))}

          <div ref={messagesEndRef} />
          <div className="input-area">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything!"
              onKeyPress={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              rows="3"
            />
            <button className="send-button" onClick={handleSend} disabled={loading}>
              {loading ? "..." : "Send"}
            </button>
          </div>
      </div>
  );
}

export default ChatWindow;
