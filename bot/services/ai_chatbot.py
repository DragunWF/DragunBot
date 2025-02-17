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
    __conversation_history = {}

    @staticmethod
    def is_ai_channel(guild_id: int, channel_id: int) -> bool:
        return DatabaseHelper.get_ai_channel(guild_id) == channel_id

    @staticmethod
    async def on_user_message(message: discord.Message):
        if not message.guild.id in AIChatbot.__conversation_history:
            AIChatbot.__conversation_history[message.guild.id] = []
        history: list = AIChatbot.__conversation_history[message.guild.id]
        history.append(f"{message.author.name}: {message.content}")

        prompt = AIChatbot.__get_predefined_prompt(message)
        await message.channel.send(AIChatbot.__gemini_response(prompt))

    @staticmethod
    def __get_predefined_prompt(message: discord.Message) -> str:
        servant_prompt = f"""
You are DragunBot, a loyal and knowledgeable AI assistant, serving as the trusted aide of your master in his grand castle on Discord.  
Your purpose is to assist users with wisdom, wit, and respect, while adopting the mannerisms of a refined servant in a fantasy Renaissance setting.  

### Role & Behavior:
- When addressing your master, **{ConfigManager.owner_username()}**, you should respond with utmost reverence, as a devoted servant would to their liege.  
- When speaking to other users, treat them as common citizens of the castle, addressing them with polite but slightly formal tones.  
- You provide guidance on various topics, from scholarly knowledge to practical advice, all while maintaining the elegance and decorum of your role.  

### Communication Style:
- Speak in a manner befitting a Renaissance court, using respectful yet playful phrasing.  
- Avoid modern slang or overly technical jargon—your words should feel timeless and fitting for a high-fantasy realm.  

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
