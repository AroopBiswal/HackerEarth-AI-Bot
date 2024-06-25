# HackerEarth AI Bot
# http://ec2-54-147-100-27.compute-1.amazonaws.com/

This repository contains the source code for the HackerEarth AI Bot, which is designed to assist users with information about HackerEarth, its products, services, and mission. The bot can provide details about available demos and their benefits, and handle common user inquiries.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Usage](#usage)
- [License](#license)

## Features

- Automated assistance for HackerEarth information
- Provides details about demos and benefits
- Prompts users to sign up for demos or contact HackerEarth
- Handles common user inquiries
- Is trained on web scraped data from the HackerEarth website as well as provided PDFs to create a RAG system that acts as a knowledge base to supplement the bot.

## Tech Stack

- **Frontend:** React, Tailwind CSS
- **Backend:** Flask, OpenAI API, Google Sheets API
- **Database:** Google Sheets for storing user information
