from bot.bot import Bot
import asyncio


def main() -> None:
    # For viewers: Most of the bot's code is in the bot directory.
    asyncio(Bot.run())


if __name__ == "__main__":
    main()
