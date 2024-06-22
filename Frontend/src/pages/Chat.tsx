import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Chat: React.FC = () => {
const navigate = useNavigate();
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you today?", sender: "bot" },
    { text: "I need help with my HackerEarth account.", sender: "user" },
  ]);
  const [input, setInput] = useState("");

  const navigateHome = () => {
    navigate('/');
  };

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: "user" }]);
      setInput("");

      setTimeout(() => {
        setMessages(prevMessages => [...prevMessages, { text: "I'm here to help!", sender: "bot" }]);
      }, 1000);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
       <header className="blue-background text-white p-4 flex items-center justify-between shadow-lg">
        <h1 className="text-2xl font-bold hover:bg-white hover:blue-text transition-colors duration-300 px-4 py-2 rounded-full"
        onClick={navigateHome}>
          HackerEarth AI Bot
        </h1>
      </header>
      <div className="flex-grow p-4 overflow-auto">
        <div className="max-w-xl mx-auto">
          {messages.map((msg, index) => (
            <div key={index} className={`my-2 p-4 rounded-lg shadow-md ${msg.sender === "bot" ? "bg-blue-200 text-blue-900 self-start mr-12" : "bg-green-200 text-green-900 ml-12"}`}>
                {msg.text}
            </div>
          ))}
        </div>
      </div>
      <div className="bg-white p-4 w-full flex items-center justify-center">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          className="flex-grow p-2 border rounded-lg mr-2 max-w-2xl"
          placeholder="Type your message..."
        />
        <button
          onClick={handleSend}
          className="blue-background text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
