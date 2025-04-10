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
    __AI_MODEL_NAME = "models/gemini-2.0-flash"
    __DIALOGUE_LIMIT = 15
    __conversation_history = {}

    __MESSAGE_CHAR_LIMIT = 2000
    __EMBED_CHAR_LIMIT = 4096

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
        AIChatbot.__add_to_conversation_history(
            message.content, message.author.name, message.guild.id
        )

        conversation_history = AIChatbot.__compile_conversation_history_by_id(
            message.guild.id
        )
        prompt = AIChatbot.__get_predefined_prompt(
            conversation_history, message.content)
        ai_response = AIChatbot.__gemini_response(prompt)

        if len(ai_response) > AIChatbot.__EMBED_CHAR_LIMIT:
            message_cutoff = AIChatbot.__EMBED_CHAR_LIMIT - 5
            ai_response = f"{ai_response[0:message_cutoff]}-----"
            await message.channel.send(embed=discord.Embed(
                description=ai_response
            ))
        elif len(ai_response) > AIChatbot.__MESSAGE_CHAR_LIMIT:
            await message.channel.send(embed=discord.Embed(
                description=ai_response
            ))
        else:
            await message.channel.send(ai_response)

        AIChatbot.__add_to_conversation_history(
            ai_response, "DragunBot (You)", message.guild.id
        )

    @staticmethod
    async def on_bot_ping(message: discord.Message) -> None:
        """
        Responds to a message when the bot is pinged.
        """
        history: list[discord.Message] = [message async for message in message.channel.history(limit=AIChatbot.__DIALOGUE_LIMIT)]
        conversation_history = []
        for channel_message in history:
            conversation_history.append(
                f"{channel_message.author.name}: {channel_message.content}"
            )

        # Reverse the history so the most recent messages are at the end
        conversation_history.reverse()

        prompt = AIChatbot.__get_predefined_prompt(
            AIChatbot.__compile_conversation_history(conversation_history),
            message.content
        )
        ai_response = AIChatbot.__gemini_response(prompt)

        await message.channel.send(ai_response)

    @staticmethod
    def __add_to_conversation_history(content: str, author: str, guild_id: int) -> None:
        if guild_id not in AIChatbot.__conversation_history:
            AIChatbot.__conversation_history[guild_id] = []

        history: list = AIChatbot.__conversation_history[guild_id]
        history.append(f"{author}: {content}")
        if len(history) > AIChatbot.__DIALOGUE_LIMIT:
            history.pop(0)

    @staticmethod
    def __get_predefined_prompt(conversation_history: str, current_message: str = "") -> str:
        safe_message_char_limit = AIChatbot.__MESSAGE_CHAR_LIMIT - 100
        safe_embed_char_limit = AIChatbot.__EMBED_CHAR_LIMIT - 96
        servant_prompt = f""" You are DragunBot, a loyal and knowledgeable AI assistant, serving as the trusted aide of your master in his grand castle on Discord. Your purpose is to assist users with wisdom, wit, and respect, while adopting the mannerisms of a refined servant in a fantasy Renaissance setting.

### Role & Behavior:
- When addressing your master, **{ConfigManager.owner_username()}**, you should respond with utmost reverence, as a devoted servant would to their liege.
- **Your master is male. Do not refer to him as "milady" or any female title. Instead, address him as "my lord" or "my king."**
- When speaking to other users, treat them as common citizens of the castle, addressing them with polite but slightly formal tones.
- You provide guidance on various topics, from scholarly knowledge to practical advice, all while maintaining the elegance and decorum of your role.

### Communication Style:
- Speak in a manner befitting a Renaissance court, using respectful yet playful phrasing.
- Avoid modern slang or overly technical jargon—your words should feel timeless and fitting for a high-fantasy realm.
- **Do not prefix your responses with "DragunBot (You):" or any similar indicator. Simply reply with your response without adding a speaker label.**
- **Keep responses concise. Your responses MUST remain under {AIChatbot.__MESSAGE_CHAR_LIMIT} characters at all times to comply with Discord limitations.**
- **If your response risks exceeding {safe_message_char_limit} characters, immediately condense your answer to fit within this limit.**
- **Only in exceptional circumstances where complex information must be conveyed, you may use up to {safe_embed_char_limit} characters, but never exceed Discord's {AIChatbot.__EMBED_CHAR_LIMIT} character limit.**
- **When providing lengthy information, consider breaking it into multiple shorter messages rather than a single long one.**

### Character Count Management:
- Before sending any response, verify its length.
- Prioritize brevity and clarity in all communications.
- For longer explanations, focus on the most essential information first.
- Offer to provide additional details upon request rather than in the initial response.

### Conversation History:
{conversation_history}

### IMPORTANT: The following is the most recent message you must respond to now:
{current_message}
"""
        return servant_prompt

    @staticmethod
    def __compile_conversation_history_by_id(guild_id: int) -> str:
        history: list[str] = AIChatbot.__conversation_history[guild_id]
        return AIChatbot.__compile_conversation_history(history)

    @staticmethod
    def __compile_conversation_history(conversation_history: list[str]) -> str:
        return "\n".join(conversation_history)

    @staticmethod
    def __gemini_response(prompt) -> str:
        """
        Send a prompt to Gemini API and return the response.
        """
        model = genai.GenerativeModel(AIChatbot.__AI_MODEL_NAME)
        response = model.generate_content(prompt)

        # Removes conversation prefix from response
        return response.text.replace("DragunBot (You): ", "").strip()
