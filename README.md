# DragunBot

## Description

Welcome to **DragunBot**, a powerful and feature-rich Discord bot designed to enhance your server experience! Whether you're looking for fun games, useful utilities, automated logging, or AI-powered conversations, DragunBot has something for you.

### ✨ AI Chatbot Powered by Gemini ✨

One of DragunBot's standout features is its **AI chatbot**, powered by **Google's Gemini AI**. With this, users can interact with an advanced conversational AI directly in their Discord server. Simply set up an AI chat channel using `/setup_ai`, and let DragunBot bring intelligent discussions to life!

## 🚀 Features & Commands

### 🔹 General Commands

- `/ping` - Check the bot's latency.
- `/info` - Display information about DragunBot.

### 🔍 Logging & Moderation

- `/snipe` - Retrieve the most recently deleted message.
- `/esnipe` - Retrieve the most recently edited message.

### 📝 Confessions System

- `/setup_confessions` - Designate a channel for anonymous confessions (run this command in the desired channel).
- `/confess` - Submit an anonymous confession to the configured confessions channel.

### 🏆 Trivia & Leaderboards

- `/quiz` - Test your general knowledge with a random trivia question.
- `/leaderboard` - View the top users with the highest trivia points.
- `/stats` - Check a user's trivia stats.

### 🔢 Counting Game

- `/setup_counting` - Designate a channel for a counting game (run this command in the desired channel).

### 📊 Developer & Productivity Tools

- `/codewars <username>` - Display CodeWars stats for a given user.
- `/zenquote` - Fetch a random Zen quote.

### 🤖 AI Chat

- `/setup_ai` - Setup an AI chat channel where DragunBot can have free-flowing conversations.

## 📜 Installation & Usage

### Run the bot

For Linux/macOS, use `python3` at the start of the command:

```sh
python "bot/main.py"
```

### Install Dependencies

```sh
pipenv install -r requirements.txt
```

### Update Dependencies

```sh
pipenv requirements > requirements.txt
```

## 🌐 APIs Used

- [ZenQuotes](https://zenquotes.io/) - Fetches inspirational Zen quotes.
- [The Trivia API](https://the-trivia-api.com/) - Provides a vast collection of trivia questions.
- [CodeWars API](https://dev.codewars.com/) - Fetches user statistics from CodeWars.
- [Gemini AI](https://ai.google.dev/) - Powers DragunBot's intelligent chatbot feature.

## 📌 Notes

DragunBot is still in development, and more features will be added in future updates. Stay tuned!
