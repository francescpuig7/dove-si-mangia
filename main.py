from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import *
from telegram.ext import *
import os
from get_json import get_messages, get_random_restaurant, update_json_new_restaurant, get_list_restaurants

TOKEN = os.getenv('DOVESIMANGIA_TOKEN')
updater = Updater(TOKEN, use_context=True)

category_text_romana = "Cucina Romana"
category_text_pizza = "Pizza"
category_text_greco = "Greco"
category_text_sushi = "Sushi"
category_text_etnico = "Etnico"
category_text_messicano = "Messicano"


def start(update: Update, context: CallbackContext):
    msg = get_messages('messages', 'start')
    update.message.reply_text(msg)


def get_restaurant(update: Update, context: CallbackContext):
    print("New get random restaurant {} - {}".format(update, context))
    buttons = [
        [KeyboardButton(category_text_pizza)], [KeyboardButton(category_text_romana)],
        [KeyboardButton(category_text_sushi)], [KeyboardButton(category_text_greco)],
        [KeyboardButton(category_text_messicano)], [KeyboardButton(category_text_etnico)]
    ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Scieglie!",
                             reply_markup=ReplyKeyboardMarkup(buttons))


def get_all_restaurants(update: Update, context: CallbackContext):
    rests = get_list_restaurants()
    for k, v in rests.items():
        update.message.reply_text(v)


def set_new_restaurant(update: Update, context: CallbackContext):
    try:
        ctx = update['message']
        new_link = ctx['text'].replace('/nuovo ', '')
        user = ctx['chat']['first_name']
        print("User: {username} - Insert new link {link}".format(username=user, link=new_link))
        resp = update_json_new_restaurant(new_restaurant=new_link, username=user)
        update.message.reply_text(resp)
    except Exception as err:
        print(err)
        update.message.reply_text('Ops! Qualcosa non è andata bene')


def message_handler(update: Update, context: CallbackContext):
    if update.message.text == category_text_pizza:
        update.message.reply_text(get_random_restaurant("pizza"))
    if update.message.text == category_text_romana:
        update.message.reply_text(get_random_restaurant("romana"))
    if update.message.text == category_text_sushi:
        update.message.reply_text(get_random_restaurant("sushi"))
    update.message.reply_text("Ops! Mi dispiace, {0} non è un comando valido".format(update.message.text))


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Ops! Mi dispiace non capisco cosa intendi: '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('random', get_restaurant))
updater.dispatcher.add_handler(CommandHandler('lista', get_all_restaurants))
updater.dispatcher.add_handler(CommandHandler('nuovo', set_new_restaurant))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown_text))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
