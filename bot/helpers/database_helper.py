import logging
import os

import discord
import firebase_admin
from firebase_admin import db, credentials


class DatabaseHelper:
    __database_started = False
    __GUILDS_KEY = "/guilds"

    @staticmethod
    def start_database():
        # Makes sure that this method is only called once
        assert DatabaseHelper.__database_started is False
        DatabaseHelper.__database_started = True
        firebase_admin.initialize_app(
            credentials.Certificate({
                'type': os.environ.get('FIREBASE_TYPE'),
                'project_id': os.environ.get('FIREBASE_PROJECT_ID'),
                'private_key_id': os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
                'private_key': os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
                'client_email': os.environ.get('FIREBASE_CLIENT_EMAIL'),
                'client_id': os.environ.get('FIREBASE_CLIENT_ID'),
                'auth_uri': os.environ.get('FIREBASE_AUTH_URI'),
                'token_uri': os.environ.get('FIREBASE_TOKEN_URI'),
                'auth_provider_x509_cert_url': os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
                'client_x509_cert_url': os.environ.get('FIREBASE_CLIENT_X509_CERT_URL'),
            }), {"databaseURL": os.environ.get("FIREBASE_DATABASE_URL")}
        )
        logging.info("Successfully connected to Realtime Firebase Database")

    @staticmethod
    def add_guild(guild_id: int):
        db.reference(DatabaseHelper.__GUILDS_KEY).child(
            {str(guild_id): {
                "counting_channel": None,
                "confessions_channel": None,
                "confessions": {}
            }}
        )
        logging.info(f"Added guild <{guild_id}> to database")

    @staticmethod
    def add_confession(guild_id: int, message: discord.Message):
        assert type(message) is discord.Message
        assert DatabaseHelper.is_guild_exists(guild_id)

        ref = f"{DatabaseHelper.__GUILDS_KEY}/{guild_id}/confessions"
        confession_count = db.reference(ref).get()
        db.reference(ref).child(
            {
                str(confession_count + 1): {
                    "author_id": str(message.author.id),
                    "author": str(message.author.name),
                    "content": message.content
                }
            }
        )
        logging.info(f"Added confession by {message.author.name} to database")

    @staticmethod
    def is_guild_exists(guild_id: int) -> bool:
        return str(guild_id) in db.reference(DatabaseHelper.__GUILDS_KEY).get()
