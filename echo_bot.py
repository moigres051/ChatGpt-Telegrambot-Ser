"""
This is a echo bot.
It echoes any incoming text messages.
"""
'''
import logging
from aiogram import Bot, Dispatcher, Router, types
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_TOKEN = os.getenv("TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot
bot = Bot(token=API_TOKEN)

# Initialize dispatcher and router
dp = Dispatcher()
router = Router()

async def chat_gpt_response(message):
    # Aquí deberías conectar con tu API de ChatGPT y devolver una respuesta.
    return f"Respuesta de ChatGPT a: {message}"

# Manejador para comandos start y help
@router.message(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("¡Hola!\nSoy tu bot de Echo!\nPotenciado por aiogram.")

# Manejador para otros mensajes
@router.message()
async def echo(message: types.Message):
    response = await chat_gpt_response(message.text)
    await message.answer(response)

if __name__ == '__main__':
    dp.include_router(router)
    asyncio.run(dp.polling(bot))

#RUN THECOMMAND  python src/echo_bot.py to start the bot in the terminal
'''

import asyncio
import logging
import sys
import os
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold


# Bot token can be obtained via https://t.me/BotFather
load_dotenv()

TOKEN= os.getenv("TOKEN")

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        #await message.send_copy(chat_id=message.chat.id)

        # Procesar el mensaje entrante y preparar una respuesta
        response = f"Recibí tu mensaje: {message.text}. 
        /¡Aquí está tu respuesta personalizada!"

        # Enviar la respuesta
        await message.answer(response)
        
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
