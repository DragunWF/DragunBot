import logging
import os
from enum import Enum

import firebase_admin
from firebase_admin import db, credentials

# Note: I set values to -1 as a default value for numeric values


class Keys(Enum):
    # Guilds Keys
    GUILDS = "/guilds"
    GUILD_NAME = "guild_name"
    CONFESSIONS_CHANNEL = "confessions_channel"
    COUNTING_CHANNEL = "counting_channel"
    CONFESSIONS = "confessions"
    COUNTING = "counting"

    # Counting keys
    LAST_USER_ID = "last_user_id"
    COUNT = "count"
    HIGH_SCORE = "high_score"

    # Users Keys
    USERS = "/users"
    USERNAME = "username"
    TRIVIA_POINTS = "trivia_points"
    TIMES_COUNTED = "times_counted"


class DatabaseHelper:
    __database_started = False

    @staticmethod
    def start_database():
        # Ensures that this method is only called once
        assert DatabaseHelper.__database_started is False
        DatabaseHelper.__database_started = True
        firebase_admin.initialize_app(
            credentials.Certificate({
                "type": os.environ.get("FIREBASE_TYPE"),
                "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
                "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
                "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
                "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
                "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
                "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
                "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
                "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL"),
            }), {"databaseURL": os.environ.get("FIREBASE_DATABASE_URL")}
        )
        logging.info("Successfully connected to Realtime Firebase Database")

    @staticmethod
    def get_guild(guild_id: int) -> dict:
        assert DatabaseHelper.is_guild_exists(
            guild_id) and type(guild_id) is int
        return db.reference(f"{Keys.GUILDS.value}/{guild_id}").get()

    @staticmethod
    def add_guild(guild_name: str, guild_id: int):
        assert type(guild_name) is str and type(guild_id) is int
        db.reference(Keys.GUILDS.value).child(str(guild_id)).set({
            Keys.GUILD_NAME.value: guild_name,
            Keys.COUNTING_CHANNEL.value: -1,
            Keys.CONFESSIONS_CHANNEL.value: -1,
            Keys.CONFESSIONS.value: -1
        })
        logging.info(f"Added guild <{guild_id}> to database")

    @staticmethod
    def update_guild_name(guild_id: int, guild_name: str):
        assert DatabaseHelper.is_guild_exists(guild_id)
        DatabaseHelper.__update_name(guild_id, guild_name, Keys.GUILDS.value)
        logging.info(f"Updated guild name in database for <{guild_id}>")

    @staticmethod
    def is_guild_exists(guild_id: int) -> bool:
        return str(guild_id) in db.reference(Keys.GUILDS.value).get()

    @staticmethod
    def get_users() -> dict:
        return db.reference(Keys.USERS.value).get()

    @staticmethod
    def get_user(user_id: int) -> dict | None:
        assert type(user_id) is int
        users = DatabaseHelper.get_users()
        if not str(user_id) in users:
            return None
        return users[str(user_id)]

    @staticmethod
    def add_user(user_id: int, username: str):
        assert type(user_id) is int and type(username) is str
        db.reference(Keys.USERS.value).child(str(user_id)).set({
            Keys.USERNAME.value: username,
            Keys.TRIVIA_POINTS.value: 0
        })
        logging.info(f"Added user <{user_id}>: {username} to database")

    @staticmethod
    def update_user_name(user_id: int, username: str):
        assert DatabaseHelper.is_user_exists(user_id)
        DatabaseHelper.__update_name(user_id, username, Keys.USERS.value)
        logging.info(f"Update username from user: <@{user_id}>")

    @staticmethod
    def update_user_times_counted(user_id: int):
        assert type(user_id) is int
        user = DatabaseHelper.get_user(user_id)
        if user is None:
            raise Exception("User not found")
        db.reference(f"{Keys.USERS.value}/{user_id}/{Keys.TIMES_COUNTED.value}").set(
            user[Keys.TIMES_COUNTED.value] + 1
        )
        logging.info(
            f'Incremented {Keys.TIMES_COUNTED.value} attribute for user <@{user_id}>'
        )

    @staticmethod
    def add_user_trivia_points(user_id: int, points: int):
        assert type(user_id) is int and type(
            points) is int and DatabaseHelper.is_user_exists(user_id)
        user_ref = db.reference(Keys.USERS.value).child(str(user_id))
        current_points = user_ref.child(Keys.TRIVIA_POINTS.value).get()
        user_ref.update({Keys.TRIVIA_POINTS.value: current_points + points})
        logging.info(f"Added {points} trivia points to <{user_id}>")

    @staticmethod
    def is_user_exists(user_id: int):
        assert type(user_id) is int
        return str(user_id) in db.reference(Keys.USERS.value).get()

    @staticmethod
    def set_counting_channel(guild_id: int, channel_id: int):
        guild_ref = db.reference(Keys.GUILDS.value).child(str(guild_id))
        channel_exists = guild_ref.child(
            Keys.COUNTING_CHANNEL.value).get() != -1
        operation_text = "Set"
        DatabaseHelper.__set_channel(guild_id, channel_id,
                                     Keys.COUNTING_CHANNEL.value)
        if not channel_exists:
            guild_ref.child(Keys.COUNTING.value).set(
                {Keys.LAST_USER_ID.value: -1,
                 Keys.COUNT.value: 0, Keys.HIGH_SCORE.value: 0}
            )
            operation_text = "Moved to"
        logging.info(
            f"{operation_text} <#{channel_id}> as the counting channel for guild: <{guild_id}>"
        )

    @staticmethod
    def update_counting(guild_id: int, user_id: int, count: int):
        assert type(guild_id) is int and type(
            user_id) is int and type(count) is int
        db.reference(Keys.GUILDS.value).child(str(guild_id)).child(Keys.COUNTING.value).update(
            {Keys.LAST_USER_ID.value: user_id, Keys.COUNT.value: count}
        )
        logging.info(
            f"Updated count to {count} for guild <{guild_id}>"
            if count != 1 else f"Resetting count for guild <{guild_id}>"
        )

    @staticmethod
    def get_counting_high_score(guild_id: int) -> int:
        assert type(guild_id) is int
        return db.reference(
            f"{Keys.GUILDS.value}/{guild_id}/{Keys.COUNTING.value}/{Keys.HIGH_SCORE}"
        ).get()

    @staticmethod
    def set_counting_high_score(guild_id: int, high_score: int):
        assert type(guild_id) is int and type(high_score) is int
        db.reference(Keys.GUILDS.value).child(str(guild_id)).child(Keys.COUNTING.value).child(Keys.HIGH_SCORE.value).update(
            {Keys.HIGH_SCORE.value: high_score}
        )
        logging.info(
            f"Updated counting high score for guild: <{guild_id}> to {high_score}"
        )

    @staticmethod
    def set_confessions_channel(guild_id: int, channel_id: int):
        DatabaseHelper.__set_channel(guild_id, channel_id,
                                     Keys.CONFESSIONS_CHANNEL.value)
        logging.info(
            f"Set <#{channel_id}> as confessions channel for guild: <{guild_id}>"
        )

    @staticmethod
    def get_confessions_channel(guild_id: int) -> int | None:
        return DatabaseHelper.__get_channel(guild_id, Keys.CONFESSIONS_CHANNEL.value)

    @staticmethod
    def get_counting_channel(guild_id: int) -> int | None:
        return DatabaseHelper.__get_channel(guild_id, Keys.COUNTING_CHANNEL.value)

    @staticmethod
    def get_counting_data(guild_id: int) -> dict:
        assert type(guild_id) is int
        return db.reference(f"{Keys.GUILDS.value}/{guild_id}/{Keys.COUNTING.value}").get()

    @staticmethod
    def get_confessions_count(guild_id: int) -> int:
        assert type(guild_id) is int
        confession_value = db.reference(
            f"{Keys.GUILDS.value}/{guild_id}/{Keys.CONFESSIONS.value}").get()
        return len(
            list(filter(lambda item: not item is None, confession_value))
        ) if confession_value != -1 else 0

    @staticmethod
    def add_confession(guild_id: int, author_id: int, author: str, content: str):
        assert DatabaseHelper.is_guild_exists(guild_id)
        assert type(guild_id) is int and type(author_id) is int and type(
            author) is str and type(content) is str

        ref = f"{Keys.GUILDS.value}/{guild_id}/{Keys.CONFESSIONS.value}"
        confession_count = DatabaseHelper.get_confessions_count(guild_id)
        db.reference(ref).child(str(confession_count + 1)).set({
            "author_id": str(author_id),
            "author": author,
            "content": content
        })
        logging.info(f"Added confession by {author} to database")

    @staticmethod
    def __update_name(id: int, new_name: str, data_key: str):
        assert type(id) is int and type(
            new_name) is str and type(data_key) is str
        name_key = None
        match data_key:
            case Keys.USERS.value:
                name_key = Keys.USERNAME.value
            case Keys.GUILDS.value:
                name_key = Keys.GUILD_NAME.value
            case _:
                raise Exception(f"Unrecognized data key: {data_key}")
        db.reference(f"{data_key}/{id}/").update({name_key: new_name})

    @staticmethod
    def __set_channel(guild_id: int, channel_id: int, channel_type: str):
        assert type(guild_id) is int and type(channel_id) is int
        db.reference(
            f"{Keys.GUILDS.value}/{guild_id}").child(channel_type).set(
            str(channel_id)
        )

    @staticmethod
    def __get_channel(guild_id: int, channel_type: str) -> int | None:
        assert type(guild_id) is int
        channel_id = db.reference(
            f"{Keys.GUILDS.value}/{guild_id}/{channel_type}"
        ).get()
        if channel_id == -1:
            return None
        return int(channel_id)
