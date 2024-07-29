import logging
from flask import Flask
from threading import Thread, Event

from .config_manager import ConfigManager


class Server:
    def __init__(self):
        self.app = Flask('')
        self._stop_event = Event()

        @self.app.route('/')
        def home():
            return f"{ConfigManager.bot_name()} is running!"

    def __run(self):
        while not self._stop_event.is_set():
            self.app.run(host='0.0.0.0', port=8080, use_reloader=False)
        logging.info("Flask server stopped.")

    def keep_alive(self):
        self._stop_event.clear()
        self.thread = Thread(target=self.__run)
        self.thread.start()
        logging.info("Flask server is now running!")
