import React from 'react';
import { useNavigate } from 'react-router-dom';

import ChatIcon from '../assets/chat.svg';
import GithubIcon from '../assets/github.svg';
import LinkedinIcon from '../assets/linkedin.svg';


const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  const handleChatClick = () => {
    navigate('/chat');
  };

  return (
    <div className="min-h-screen bg-gray-800 w-full flex flex-col justify-start items-center overflow-x-hidden">


      <section className="gradient-1 text-white w-full">
        <div className=" px-6 py-20 text-center flex flex-col items-center">
          <h1 className="text-5xl font-bold mb-4">HackerEarth AI Bot</h1>
          <p className="text-lg mb-8">An AI bot that answers questions about HackerEarth, its products, services, and mission.</p>
          <button className="bg-white text-2xl black-text font-semibold px-10 py-4 rounded-full hover:bg-gray-200 transition duration-300 relative z-10 flex items-center justify-center space-x-2"
          onClick={handleChatClick}>
            <span>Start Chatting</span>
            <img src={ChatIcon} alt="" className="w-10"/>
          </button>
        </div>
      </section>


      <section className="w-full py-20 white-background px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-800">Features</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Feature One</h3>
            <p className="text-gray-600">Description of feature one.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Feature Two</h3>
            <p className="text-gray-600">Description of feature two.</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Feature Three</h3>
            <p className="text-gray-600">Description of feature three.</p>
          </div>
        </div>
      </section>


      <section className="w-full blue-background text-white py-16">
        <div className=" px-6 text-center">
          <h2 className="text-xl font-bold mb-4">Want to learn more about this project?</h2>
          <a href="https://github.com/AroopBiswal/HackerEarth-AI-Bot" target="_blank" rel="noopener noreferrer">
            <button className="bg-white black-text font-semibold px-8 py-2 rounded-full hover:bg-gray-200 transition duration-300">
              Source Code + README
            </button>
          </a>
        </div>
      </section>


      <footer className="text-white py-3 w-full">
      <div className=" mx-auto px-6 text-center flex flex-row items-center justify-center space-x-4">
        <p>Made by Aroop Biswal</p>
        <a href="https://www.linkedin.com/in/aroopbiswal/" target="_blank" rel="noopener noreferrer" className="hover:text-gray-400">
          <img src={LinkedinIcon} alt="LinkedIn" className="w-6" />
        </a>
        <a href="https://github.com/AroopBiswal" target="_blank" rel="noopener noreferrer" className="hover:text-gray-400">
          <img src={GithubIcon} alt="GitHub" className="w-6" />
        </a>
      </div>
      </footer>
    </div>
  );
};

export default LandingPage;
