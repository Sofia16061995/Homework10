import telebot, datetime, time, math, re
from telebot import types

BOT_TOKEN = '5615869595:AAG_E0Hjm9FINSQYVV3OdxYwhT7SkIAE0x8'
BOT_NAME = 'calculator16_bot'
bot= telebot.TeleBot(BOT_TOKEN)

TIMEOUT_CONNECTION = 5

START_MESSAGE = """Что будем творить? Сейчас будет волшебство"""
HELP_MESSAGE = """Давай подскажу солнышко :). Вы отправляете мне необходимое вычисление и получаете его результат.
***Какие операции есть***:
    + -> сложение;
    - -> вычитание;
    \* -> умножение;
    / -> деление;
    \*\* -> возведение в степень.
    
***Какие функции есть***:
    cos(x) -> косинус x;
    sin(x) -> синус x;
    tg(x) -> тангенс x;
    fact(x) -> факториал x;
    sqrt(x) -> квадратный корень х;
    sqr(x) -> х в квадрате.
***Какие логарифмы есть***:
    log2(x) -> логарифм х по основанию 2;
    lg(х) -> десятичный логарифм х;
    ln(x) -> натуральный логарифм x;
    log(b, х) -> логарифм х по основанию b.
***Какие системы счисления есть***:
    0bx -> перевести двоичное число х в десятичное;
    0ox -> перевести восьмеричное число х в десятичное;
    0xx -> перевести шестнадцатеричное число х в десятичное."""

пи = п = p = pi = 3.141592653589793238462643

def fact(float_):
    return math.factorial(float_)

def cos(float_):
    return math.cos(float_)

def sin(float_):
    return math.sin(float_)

def tg(float_):
    return math.tan(float_)
    
def tan(float_):
    return math.tan(float_)


def ln(float_):
    return math.log(float_)

def log(base, float_):
    return math.log(float_, base)

def lg(float_):
    return math.log10(float_)

def log2(float_):
    return math.log2(float_)

def exp(float_):
    return math.exp(float_)


@bot.message_handler(commands=['start', 'help'])
def send_start(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    if message.text.lower() == '/start':
        msg = bot.send_message(message.chat.id, START_MESSAGE, parse_mode='markdown')

    elif message.text.lower() == '/help':
        msg = bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='markdown')
        
    if (msg):
        print('Бот: %s'%msg.text)


@bot.message_handler(func = lambda message: True)
def answer_to_user(message):
    print('%s (%s): %s' %(message.chat.first_name, message.chat.username, message.text))
    msg = None

    user_message = message.text.lower()

    if BOT_NAME:
        regex = re.compile(BOT_NAME.lower())
        print(regex.search(user_message))
        if regex.search(user_message) == None:
            return

        regex = re.compile('%s[^a-z]'%(BOT_NAME.lower()))
        user_message = regex.sub("", user_message)

    user_message = user_message.lstrip()
    user_message = user_message.rstrip()
    
    print(user_message)

    if user_message == 'привет':
        msg = bot.send_message(message.chat.id, '*Привет, %s*'%(message.chat.first_name), parse_mode='markdown')

    elif user_message == 'помощь':
        msg = bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='markdown')

    else:
        try:
            answer = str(eval(user_message.replace(' ', '')))
            msg = bot.send_message(message.chat.id, user_message.replace(' ', '') + ' = ' + answer)
                
        except SyntaxError:
            msg = bot.send_message(message.chat.id, 'Упс...где-то ошибка. Может, неправильно введено выражение?. \nПопробуйте ещё раз.')
        except NameError:
            msg = bot.send_message(message.chat.id, 'Таких переменных не существует. \nПопробуйте ещё раз.')
        except TypeError:
            msg = bot.send_message(message.chat.id, 'Похоже, что в выражении присутствует ошибка . \nПопробуйте ещё раз.')
        except ZeroDivisionError:
            msg = bot.send_message(message.chat.id, 'Ай-Ай! (:. \nПопробуйте ещё раз.')

    if (msg):
        print('Бот: %s'%msg.text)


@bot.inline_handler(func=lambda query: True)
def inline_answer_to_user(inline_query):
    answer = 0
    answer_list = []
    try:
        answer = str(eval(inline_query.query.lower().replace(' ', '')))
        answer_to_send = answer.replace('*', '\*')
        query_to_send = inline_query.query.replace('*', '\*').lower().replace(' ', '')

        answer_list.append(types.InlineQueryResultArticle(
            id = 0,
            title = 'Отправить с выражением',
            description='%s = %s' % (inline_query.query, answer),
            input_message_content = types.InputTextMessageContent(
                message_text = '%s = *%s*' % (query_to_send, answer_to_send),
                parse_mode = 'markdown'),
        ))

        answer_list.append(types.InlineQueryResultArticle(
            id = 1,
            title = 'Отправить без выражения',
            description='%s' % (answer),
            input_message_content = types.InputTextMessageContent(
                message_text = '*%s*' % (answer_to_send),
                parse_mode = 'markdown'),
        ))
            
    except SyntaxError: answer = False
    except NameError: answer = False
    except TypeError: answer = False
    except ZeroDivisionError: answer = False

    if (not answer):    
        answer_list = []
        answer_list.append(types.InlineQueryResultArticle(
            id = 0,
            title = 'Калькулятор',
            description='Чтобы посчитать выражение - введите его.\nЕсли вы хотите просмотреть справку, то перейдите в диалог со мной и напишите \"/help\"',
            input_message_content = types.InputTextMessageContent(message_text = 'Я хотел(а) посчитать выражение, но нажал(а) не туда')
        ))
    
    bot.answer_inline_query(inline_query.id, answer_list)


if (__name__ == '__main__'):
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print ('Ошибка подключения. Попытка подключения через %s сек.'%TIMEOUT_CONNECTION)
            time.sleep(TIMEOUT_CONNECTION)