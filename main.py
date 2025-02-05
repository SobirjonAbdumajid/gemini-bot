# pip install pyTelegramBotAPI
# pip install google-generativeai

import telebot
import google.generativeai as genai
import time

# Configure your bot and AI model here
TELEGRAM_TOKEN = 'TOKEN'
GEN_AI_API_KEY = 'API_KEY'

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)  # parse_mode is None to send plain text
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

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Start an empty chat history
convo = model.start_chat(history=[])

# Define a function to clean Markdown symbols from text
def clean_text(text):
    markdown_symbols = ['**', '__', '*', '_', '`', '~~']
    for symbol in markdown_symbols:
        text = text.replace(symbol, ' ')
    return text

# Define command handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = "Hello! This Bot is made by Sobirjon Abdumajidov. How can I assist you today?"
    bot.reply_to(message, welcome_text)

# Define a handler for all other messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Simulate typing action
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)  # Wait a bit to simulate thinking time

    # Process the message through the AI model
    convo.send_message(message.text)
    response = convo.last.text

    # Clean the response from Markdown symbols and reply
    clean_response = clean_text(response)
    bot.reply_to(message, clean_response)

# Start the bot
if __name__ == '__main__': bot.infinity_polling()
