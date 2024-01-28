"""
chatgpt.py
-----------

This module contains the implementation of a Telegram bot that uses the OpenAI chat GPT API 
to generate responses to user messages.

Usage:
1. Set up a Telegram bot and obtain its token.
2. Set up an OpenAI account and obtain an API key.
3. Set the environment variables "TOKEN" and "OPENAI_API_KEY" 
    to the bot token and OpenAI API key, respectively.
4. Run this script to start the bot.

Note: This implementation uses the aiogram, openai library to interact with the Telegram API 
and the OpenAI API, respectively.

Example:
    $ python chatgpt.py

Author: Sunny BHaveen Chandra, modified by SergioMendez
"""
import os
import asyncio
import openai
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.filters.command import CommandStart

class Reference:
    def __init__(self) -> None:
        self.response = ""

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("TOKEN")

# Model used in chatGPT
MODEL_NAME = "gpt-3.5-turbo"

# Create a reference object to store the previous response
reference = Reference()

# Initialize Router
router = Router()

def clear_past():
    reference.response = ""

@router.message(CommandStart())
async def welcome(message: types.Message):
    clear_past()
    await message.reply("Hello! \nI'm a ChatGPT Telegram bot. REMAKEIT FOR SERGIO MENDEZ How may I assist you today?")

@router.message(Command(commands=['clear']))
async def clear(message: types.Message):
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

@router.message(Command(commands=['help']))
async def helper(message: types.Message):
    help_command = """ 
    Hi there, I'm a ChatGPT bot. Here are some commands you can use:
    /start - to start the conversation
    /clear - to clear the past conversation and context
    /help  - to get this help menu
    I hope this helps.
    """
    await message.reply(help_command)

@router.message()
async def chatgpt(message: types.Message):
    print(f"> USER: \n{message.text}")
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": message.text}
        ]
    )
    reference.response = response['choices'][0]['message']['content']
    print(f"> chatGPT: \n{reference.response}")
    await message.reply(reference.response)

async def main():
    # Initialize Bot and Dispatcher
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # Run events dispatching
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Starting bot...")
    asyncio.run(main())
    print("Bot stopped")
