# DragunBot

## Description

Welcome to DragunBot, a versatile Discord bot designed to enhance server experience with a wide range of features! Whether you're looking for fun and games, useful information, detailed stats, efficient logging, powerful automation, or seamless API integration, DragunBot has got you covered.

To explore the full list of available commands, simply type `/help`.

**Note:** This Discord bot is still in development... There are more features to come!

## Scripts

### Run the bot

Use `python3` at the start of the command for Linux or macOS.

```shell
python "bot/bot.py"
```

### Install `requirements.txt`

```shell
pipenv install -r requirements.txt
```

### Update `requirements.txt`

```shell
pipenv requirements > requirements.txt
```

## APIs Used

- [ZenQuotes](https://zenquotes.io/)
- [The Trivia API](https://the-trivia-api.com/)
- [CodeWars API](https://dev.codewars.com/)

## NoSQL Database Structure

**Database:** Firebase Realtime Database

```json
{
  "guilds": {
    "guild_id": {
      "guild_name": "name of the guild",
      "counting_channel": "channel_id",
      "confessions_channel": "channel_id",
      "confessions": {
        "confession_id": {
          "author_id": "id",
          "author": "author",
          "content": "message content"
        }
      },
      "counting": {
        "last_user_id": "user id of the last one who counted",
        "count": 0
      }
    }
  },
  "users": {
    "user_id": {
      "username": "name",
      "trivia_points": 0,
      "times_counted": 0
    }
  }
}
```
