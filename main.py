import time
import telebot

bot = telebot.TeleBot('<BOT_TOKEN>')

def logging(func):
    def _wrapper(message):
        print(f'{ time.strftime("%Y-%m-%d %H:%M:%S") } :' \
            + f'    <{ message.chat.id } / @{ message.chat.username } / "{ message.chat.title }">:' \
            + f'    <{ message.from_user.id } / @{ message.from_user.username } / "{ message.from_user.first_name }">:' \
            + f'        { message.text }')
        func(message)
    return _wrapper

def admins_only(func):
    def _wrapper(message):
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator']:
            func(message)
        else:
            bot.reply_to(message, 'You are neither a creator nor an administrator')
    return _wrapper


@bot.message_handler(commands=['off'])
@logging
@admins_only
def msg_off(message):
    permissions = bot.get_chat(message.chat.id).permissions
    permissions.can_send_messages = False
    bot.set_chat_permissions(message.chat.id, permissions, use_independent_chat_permissions=True)
    bot.send_message(message.chat.id, 'Messages are switched off')

@bot.message_handler(commands=['on'])
@logging
@admins_only
def msg_on(message):
    permissions = bot.get_chat(message.chat.id).permissions
    permissions.can_send_messages = True
    bot.set_chat_permissions(message.chat.id, permissions, use_independent_chat_permissions=True)
    bot.send_message(message.chat.id, 'Messages are switched on')


bot.infinity_polling()
