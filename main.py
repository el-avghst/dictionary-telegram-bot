import telebot
from config import TOKEN
"""TOKEN - переменная, содержащая токен, полученный при создании бота в BotFather. Хранится в файле config.py."""
from extensions import WrongCommand
from extensions import Word


bot=telebot.TeleBot(TOKEN)
user_spisok = []

@bot.message_handler(commands=["start","help"])
def help(message):
    text="Чтобы получить транскрипцию слова, введите команду боту в следующем формате:\n<слово>, tr\n\nЧтобы получить значение слова, введите команду боту в следующем формате:\n<слово>, def"
    bot.reply_to(message,text)

@bot.message_handler(commands=["history"])
def history(message):
    text = 'Ваша история:\n'
    for i in user_spisok:
        new_str = str(i)[1:-1]
        text +=new_str
        text += '\n'
    text+= 'Чтобы очистить список, введите команду /clear'
    bot.reply_to(message, text)

@bot.message_handler(commands=["clear"])
def clear(message):
    user_spisok.clear()
    text = 'Список очищен'
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text"])
def user_command(message):
    try:
        user_request = message.text.split(",")
        request_tuple = tuple(user_request)
        if request_tuple in user_spisok:
            bot.send_message(message.chat.id, 'Вы уже вводили этот запрос. Чтобы посмотреть введенные ранее запросы, введите команду /history')
        else:
            user_spisok.append(request_tuple)
            if len(user_request) != 2:
                raise WrongCommand("Неверно введена команда")
            if user_request[1] == 'tr' or user_request[1] == ' tr':
                user_word = Word(user_request[0])
                transcription = user_word.get_phonetics()
                bot.send_message(message.chat.id, transcription)
            elif user_request[1] == 'def' or user_request[1] == ' def':
                user_word = Word(user_request[0])
                definition = user_word.get_definition()
                bot.send_message(message.chat.id, definition)
            else:
                raise WrongCommand("Неверно введена команда")
    except WrongCommand:
        bot.reply_to(message, "Неверно введена команда")


bot.polling(non_stop=True)