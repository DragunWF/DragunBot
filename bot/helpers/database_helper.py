import os
import firebase_admin
from firebase_admin import db, credentials
from dotenv import load_dotenv


class DatabaseHelper:
    __database_started = False

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

    @staticmethod
    def add_guild():
        pass
