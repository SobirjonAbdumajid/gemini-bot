# pip install aiogram python-dotenv google-generativeai

import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get tokens from environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEN_AI_API_KEY = os.getenv("GEN_AI_API_KEY")

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Configure Google Generative AI
genai.configure(api_key=GEN_AI_API_KEY)

# Set up the model configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Start an empty chat history
convo = model.start_chat(history=[])

# Define a function to clean Markdown symbols from text
def clean_text(text):
    markdown_symbols = ['**', '__', '*', '_', '`', '~~']
    for symbol in markdown_symbols:
        text = text.replace(symbol, ' ')
    return text

# Command handler for /start and /help
@dp.message(CommandStart())
async def send_welcome(message: Message):
    welcome_text = "Hello! This Bot is made by Sobirjon Abdumajidov. How can I assist you today?"
    await message.answer(welcome_text)

# Handler for all other messages
@dp.message()
async def handle_message(message: types.Message):
    # Simulate typing action
    await bot.send_chat_action(message.chat.id, action="typing")

    # Process the message through the AI model
    convo.send_message(message.text)
    response = convo.last.text

    # Clean the response from Markdown symbols and reply
    clean_response = clean_text(response)
    await message.answer(clean_response)

# Start the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())