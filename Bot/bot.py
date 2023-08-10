from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters
from Miscellaneous.Scraper import pastebin, text_scraper, throwbin
import os

# Import other helper functions
from Checks.Altbalaji import altbalaji_helper
from Checks.hoichoi import hoichoi_helper
from Checks.voot import Voot_helper
from Checks.zee5 import zee_helper
from message import Sendmessage, logger

# Get your bot token from environment variables
bot_token = os.environ.get('TG_BOT_TOKEN')

startmessage = [
    [
        InlineKeyboardButton(
            "Telegraph 📝",
            url='https://telegra.ph/Instructions-to-Use-This-Bot-04-07'
        ),
        InlineKeyboardButton(
            "DEV 👷🏻",
            url='https://t.me/B0RNTOLE4RN'
        )
    ]
]

# ... (rest of your code remains unchanged)

def start(update, context):
    info = update.effective_user
    print(info)
    chat_id = info.id
    userid = info.username
    text = f'Welcome @{userid}, To Account Check Bot, to know more use /help or read the telegraph below. This bot is provided for educational use only, any misuse then you should be responsible'
    Sendmessage(chat_id, text, reply_markup=InlineKeyboardMarkup(startmessage))


def help_command(update, context):
    chat_id = update.message.chat_id
    text = "<b>Available Sites:\n!alt~space~combo* - to check Altbalaji accounts\n!hoi~space~combo* - to check Hoichoi accounts\n!voo~space~combo* - to check Voot accounts\n!zee~space~combo* - to check Zee5 accounts\n\nMiscellaneous:-\n!pst~space~title|text - to paste text on Throwbin.io and get paste link</b>(If you don't want to give title then skip it just send the text)\n\n*combo here means Email:password combination,':' is important."
    Sendmessage(chat_id, text, reply_markup=InlineKeyboardMarkup(startmessage), parse_mode='HTML')


def duty(update, context):
    chat_id = update.message.chat_id
    text = update.message.text.split(' ', 1)
    if text[0] == '!alt':
        if '\n' in text[1]:
            simple = combos_spilt(text[1])
            for i in simple:
                altbalaji_helper(chat_id, i)
            Sendmessage(chat_id, 'Completed')
        else:
            altbalaji_helper(chat_id, text[1])
    # ... similar blocks for other commands
    else:
        logger.info('Unknown Command')


def scraper_command(update, context):
    msg = update.message.text
    status_msg = update.message
    chat_id = status_msg.chat_id
    try:
        if 'pastebin' in msg:
            link = msg.split(' ')[1]
            pastebin(chat_id, link)
        else:
            scrape_text = status_msg.reply_to_message.text
            text_scraper(chat_id, scrape_text)
    except:
        Sendmessage(chat_id, 'Only Supports pastebin, please check if you send paste bin link')


def main():
    updater = Updater(bot_token)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, duty))

    dp.add_handler(CommandHandler("scrape", scraper_command))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    logger.info("Bot Started!!!")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
