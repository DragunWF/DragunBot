# NoSQL Database Structure

## Firebase Realtime Database

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
