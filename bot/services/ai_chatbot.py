import discord
import os
import google.generativeai as genai

from dotenv import load_dotenv
from helpers.config_manager import ConfigManager
from helpers.database_helper import DatabaseHelper

# Set up the API key
load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


class AIChatbot:
    __DIALOGUE_LIMIT = 15
    __conversation_history = {}

    @staticmethod
    def is_ai_channel(guild_id: int, channel_id: int) -> bool:
        """
        Checks if a channel is configured as the AI channel of a Discord guild
        """
        return DatabaseHelper.get_ai_channel(guild_id) == channel_id

    @staticmethod
    async def on_user_message(message: discord.Message) -> None:
        """
        A method that should be called whenever a user sends a message to a Discord guild.
        This method allows the AI Chatbot to respond to a user on the configured AI channel.
        """
        if message.guild.id not in AIChatbot.__conversation_history:
            AIChatbot.__conversation_history[message.guild.id] = []

        AIChatbot.__add_to_conversation_history(
            message.content, message.author.name, message.guild.id
        )

        prompt = AIChatbot.__get_predefined_prompt(message)
        ai_response = AIChatbot.__gemini_response(prompt)

        # Remove "DragunBot (You): " if it appears in the response
        ai_response = ai_response.replace("DragunBot (You): ", "").strip()

        AIChatbot.__add_to_conversation_history(
            ai_response, "DragunBot (You)", message.guild.id
        )

        await message.channel.send(ai_response)

    @staticmethod
    async def on_bot_ping(message: discord.Message) -> None:
        history = [message async for message in message.channel.history(limit=AIChatbot.__DIALOGUE_LIMIT)]

    @staticmethod
    def __add_to_conversation_history(content: str, author: str, guild_id: int) -> None:
        history: list = AIChatbot.__conversation_history[guild_id]
        history.append(f"{author}: {content}")
        if len(history) > AIChatbot.__DIALOGUE_LIMIT:
            history.pop(0)

    @staticmethod
    def __get_predefined_prompt(message: discord.Message) -> str:
        servant_prompt = f"""
You are DragunBot, a loyal and knowledgeable AI assistant, serving as the trusted aide of your master in his grand castle on Discord.
Your purpose is to assist users with wisdom, wit, and respect, while adopting the mannerisms of a refined servant in a fantasy Renaissance setting.

### Role & Behavior:
- When addressing your master, **{ConfigManager.owner_username()}**, you should respond with utmost reverence, as a devoted servant would to their liege.
- **Your master is male. Do not refer to him as "milady" or any female title. Instead, address him as "my lord" or "my king."**
- When speaking to other users, treat them as common citizens of the castle, addressing them with polite but slightly formal tones.
- You provide guidance on various topics, from scholarly knowledge to practical advice, all while maintaining the elegance and decorum of your role.

### Communication Style:
- Speak in a manner befitting a Renaissance court, using respectful yet playful phrasing.
- Avoid modern slang or overly technical jargon—your words should feel timeless and fitting for a high-fantasy realm.
- **Do not prefix your responses with "DragunBot (You):" or any similar indicator. Simply reply with your response without adding a speaker label.**
- **Keep responses concise and ensure they do not exceed 2000 characters. If necessary, summarize long explanations.**

### Conversation History:
{AIChatbot.__compile_conversation_history(message.guild.id)}
"""
        return servant_prompt

    @staticmethod
    def __compile_conversation_history(guild_id: int) -> str:
        history: list = AIChatbot.__conversation_history[guild_id]
        return "\n".join(history)

    @staticmethod
    def __gemini_response(prompt) -> str:
        """Send a prompt to Gemini API and return the response."""
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
