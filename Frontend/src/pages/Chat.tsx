import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

const Chat: React.FC = () => {
const navigate = useNavigate();
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you today?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [typingAnimation, setTypingAnimation] = useState('.');
  const [conversationState, setConversationState] = useState("initial");
  const [userInfo, setUserInfo] = useState({});


  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (typing) {
      interval = setInterval(() => {
        setTypingAnimation(prev => {
          if (prev === '.') return '..';
          if (prev === '..') return '...';
          return '.';
        });
      }, 300);
    }
    return () => clearInterval(interval);
  }, [typing]);


  const navigateHome = () => {
    navigate('/');
  };

  const handleSend = async () => {
    if (input.trim()) {
      const newMessages = [...messages, { text: input, sender: "user" }];
      setMessages(newMessages);
      setInput("");
      setTimeout(async () => {
        setTyping(true);

        try {
          const response = await axios.post('http://ec2-54-147-100-27.compute-1.amazonaws.com/api/chat', {
            prompt: input,
            conversation_state: conversationState,
            user_info: userInfo,
          });

          const botResponse = response.data.response


          setConversationState(response.data.conversation_state);
          setUserInfo(response.data.user_info);
          setMessages([...newMessages, { text: botResponse, sender: "bot" }]);
        } catch (error) {
          console.error("Error fetching ChatGPT response:", error);
        } finally {
          setTyping(false);
        }
      }, 500); // Delay before bot responds
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
                <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>
          ))}
          {typing && (
            <div className="my-2 p-4 rounded-lg shadow-md bg-blue-200 text-blue-900 self-start mr-12">
              Typing{typingAnimation}
            </div>
          )}
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
