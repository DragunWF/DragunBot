import logging
import os

import discord
import firebase_admin
from firebase_admin import db, credentials


class DatabaseHelper:
    __database_started = False
    __GUILDS = "/guilds"

    @staticmethod
    def start_database():
        # Makes sure that this method is only called once
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
        db.reference(DatabaseHelper.__GUILDS).child(str(guild_id)).set({
            "guild_name": guild_name,
            "counting_channel": -1,
            "confessions_channel": -1,
            "confessions": -1
        })
        logging.info(f"Added guild <{guild_id}> to database")

    @staticmethod
    def is_guild_exists(guild_id: int) -> bool:
        return str(guild_id) in db.reference(DatabaseHelper.__GUILDS).get()

    @staticmethod
    def set_confessions_channel(guild_id: int, channel_id: int):
        assert type(channel_id) is int
        assert type(guild_id) is int
        db.reference(
            f"{DatabaseHelper.__GUILDS}/{guild_id}").child("confessions_channel").set(
            str(channel_id)
        )

    @staticmethod
    def get_confessions_channel(guild_id: int) -> int | None:
        assert type(guild_id) is int
        channel_id = db.reference(
            f"{DatabaseHelper.__GUILDS}/{guild_id}/confessions_channel"
        ).get()
        if channel_id == -1:
            return None
        return int(channel_id)

    @staticmethod
    def add_confession(guild_id: int, author_id: int, author: str, content: str):
        assert DatabaseHelper.is_guild_exists(guild_id)

        ref = f"{DatabaseHelper.__GUILDS}/{guild_id}/confessions"
        confession_count = len(db.reference(ref).get())
        db.reference(ref).child(str(confession_count + 1)).set({
            "author_id": str(author_id),
            "author": author,
            "content": content
        })
        logging.info(f"Added confession by {author} to database")
