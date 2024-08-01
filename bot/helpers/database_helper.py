import logging
import os
from enum import Enum

import firebase_admin
from firebase_admin import db, credentials

# Note: I set values to -1 as a default value


class Tables(Enum):
    # Guilds Keys
    GUILDS = "/guilds"
    GUILD_NAME = "guild_name"
    CONFESSIONS_CHANNEL = "confessions_channel"
    COUNTING_CHANNEL = "counting_channel"
    CONFESSIONS = "confessions"

    # Users Keys
    USERS = "/users"
    USERNAME = "username"
    TRIVIA_POINTS = "trivia_points"


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
    def add_guild(guild_name: str, guild_id: int):
        assert type(guild_name) is str and type(guild_id) is int
        db.reference(Tables.GUILDS.value).child(str(guild_id)).set({
            Tables.GUILD_NAME.value: guild_name,
            Tables.COUNTING_CHANNEL.value: -1,
            Tables.CONFESSIONS_CHANNEL.value: -1,
            Tables.CONFESSIONS.value: -1
        })
        logging.info(f"Added guild <{guild_id}> to database")

    @staticmethod
    def is_guild_exists(guild_id: int) -> bool:
        return str(guild_id) in db.reference(Tables.GUILDS.value).get()

    @staticmethod
    def get_users() -> dict:
        return db.reference(Tables.USERS.value).get()

    @staticmethod
    def add_user(user_id: int, username: str):
        assert type(user_id) is int and type(username) is str
        db.reference(Tables.USERS.value).child(str(user_id)).set({
            Tables.USERNAME.value: username,
            Tables.TRIVIA_POINTS.value: 0
        })
        logging.info(f"Added user <{user_id}>: {username} to database")

    @staticmethod
    def add_user_trivia_points(user_id: int, points: int):
        assert type(user_id) is int and type(points) is int
        if not DatabaseHelper.is_user_exists(user_id):
            DatabaseHelper.add_user(user_id)
        user_ref = db.reference(Tables.USERS).child(
            str(user_id)).child(Tables.TRIVIA_POINTS.value)
        current_points = user_ref.get()
        user_ref.child(Tables.TRIVIA_POINTS.value).set(current_points + points)
        logging.info(f"Added {points} trivia points to <{user_id}>")

    @staticmethod
    def is_user_exists(user_id: int):
        assert type(user_id) is int
        return str(user_id) in db.reference(Tables.USERS.value).get()

    @staticmethod
    def set_confessions_channel(guild_id: int, channel_id: int):
        assert type(channel_id) is int
        assert type(guild_id) is int
        db.reference(
            f"{Tables.GUILDS.value}/{guild_id}").child(Tables.CONFESSIONS_CHANNEL.value).set(
            str(channel_id)
        )

    @staticmethod
    def get_confessions_channel(guild_id: int) -> int | None:
        assert type(guild_id) is int
        channel_id = db.reference(
            f"{Tables.GUILDS.value}/{guild_id}/{Tables.CONFESSIONS_CHANNEL.value}"
        ).get()
        if channel_id == -1:
            return None
        return int(channel_id)

    @staticmethod
    def get_confessions_count(guild_id: int) -> int:
        assert type(guild_id) is int
        confession_value = db.reference(
            f"{Tables.GUILDS.value}/{guild_id}/{Tables.CONFESSIONS.value}").get()
        return len(
            list(filter(lambda item: not item is None, confession_value))
        ) if confession_value != -1 else 0

    @staticmethod
    def add_confession(guild_id: int, author_id: int, author: str, content: str):
        assert DatabaseHelper.is_guild_exists(guild_id)
        assert type(guild_id) is int and type(author_id) is int and type(
            author) is str and type(content) is str

        ref = f"{Tables.GUILDS.value}/{guild_id}/{Tables.CONFESSIONS.value}"
        confession_count = DatabaseHelper.get_confessions_count(guild_id)
        db.reference(ref).child(str(confession_count + 1)).set({
            "author_id": str(author_id),
            "author": author,
            "content": content
        })
        logging.info(f"Added confession by {author} to database")
