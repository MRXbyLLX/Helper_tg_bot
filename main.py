from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import telebot
from telebot import custom_filters
import sqlite3
import random

token = '5724199271:AAEPzKMBxTdjM3LG-popsyCdpsoZ30WDxWc'

bot = telebot.TeleBot(token)

con = sqlite3.connect('words.db', check_same_thread=False)
cursor = con.cursor()

bot.set_my_commands([
    telebot.types.BotCommand("/start", "start bot"),
    telebot.types.BotCommand("/menu", "helper menu"),
    telebot.types.BotCommand("/stop", "stop words")
])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton(text='👉продолжить👈', callback_data='1')
    markup.add(button_1)
    bot.reply_to(message, 'Привет, этот бот может помочь тебе выучить слова', reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = InlineKeyboardMarkup(row_width=1)
    button_1 = InlineKeyboardButton(text='Создать учебный модуль', callback_data='2')
    button_2 = InlineKeyboardButton(text='Мои модули', callback_data='3')
    markup.add(button_1, button_2)
    bot.reply_to(message, 'Helper menu', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    printed = []
    right1 = []
    wrong1 = []
    right = []
    wrong = []
    n = []
    translate = []
    dict = []
    users_id = message.chat.id
    data1 = cursor.execute('select * from words where id = ?', (users_id,)).fetchall()
    for i in data1:
        t = i[0]
        n.append(t)
    for c in n:
        while n.count(c) > 1:
            n.remove(c)
    for x in n:
        if message.text == x:
            markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            button_1 = KeyboardButton('Редактировать')
            button_2 = KeyboardButton('Изучать')
            button_3 = KeyboardButton('Просмотреть')
            markup.add(button_1, button_2, button_3)
            n = bot.reply_to(message, x + ':', reply_markup=markup)
            bot.register_next_step_handler(n, func5, translate, dict, wrong, right, x, right1, wrong1)


def func24(word1, word, translate, dict, wrong, right, right1, wrong1, x):
    with con:
        cursor.execute('insert into words (num, id, word, translate) values (?,?,?,?)', (x, word1.from_user.id, word, word1.text,))
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = KeyboardButton('Изменить / удалить')
    button_2 = KeyboardButton('Добавить')
    button_3 = KeyboardButton('Удалить модуль')
    button_4 = KeyboardButton('Назад')
    markup.add(button_1, button_2, button_3, button_4)
    n = bot.reply_to(word1, 'Слово успешно добавлено', reply_markup=markup)
    bot.register_next_step_handler(n, func9, translate, dict, wrong, right, x, right1, wrong1)



def func23(message, translate, dict, wrong, right, right1, wrong1, x):
    d = bot.reply_to(message, 'Перевод')
    bot.register_next_step_handler(d, func24, message.text, translate, dict, wrong, right, right1, wrong1, x)


def func22(word1, word, translate, dict, wrong, right, m, right1, wrong1, x, z):
    id = word1.from_user.id
    with con:
        cursor.execute('delete from words where id = ? and word = ? and num = ?;', (id, z, x,))
        cursor.execute('insert into words (num, id, word, translate) values (?,?,?,?)',(x, id, word, word1.text,))
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = KeyboardButton('Редактировать')
    button_2 = KeyboardButton('Удалить')
    button_3 = KeyboardButton('Назад')
    markup.add(button_1, button_2, button_3)
    n = bot.reply_to(word1, 'Слово успешно изменено', reply_markup=markup)
    bot.register_next_step_handler(n, func14, translate, dict, wrong, right, m, right1, wrong1, x, z)

def func21(word, translate, dict, wrong, right, m, right1, wrong1, x, z):
    if word.text == 'Отмена':
        markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_1 = KeyboardButton('Редактировать')
        button_2 = KeyboardButton('Удалить')
        button_3 = KeyboardButton('Назад')
        markup.add(button_1, button_2, button_3)
        n = bot.reply_to(word, m, reply_markup=markup)
        bot.register_next_step_handler(n, func14, translate, dict, wrong, right, m, right1, wrong1, x)
    else:
        d = bot.reply_to(word, 'Перевод')
        bot.register_next_step_handler(d, func22, word.text, translate, dict, wrong, right, m, right1, wrong1, x, z)


def func20(message, translate, dict, wrong, right, x, right1, wrong1):
    if message.text == 'Нет ❤️‍🩹':
        func8(message, translate, dict, wrong, right, right1, wrong1, x)
    elif message.text == 'Да ☠':
        m = len(dict)
        while m != 0:
            with con:
                cursor.execute('delete from words where num = ?;', (x,))
            m -= 1
        markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_1 = KeyboardButton('/menu')
        markup.add(button_1)
        bot.reply_to(message, 'Модуль удалён', reply_markup=markup)

def func19(message, translate, dict, wrong, right, x, right1, wrong1):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = KeyboardButton('Нет ❤️‍🩹')
    button_2 = KeyboardButton('Да ☠')
    markup.add(button_1, button_2)
    n = bot.reply_to(message, 'Точно?', reply_markup=markup)
    bot.register_next_step_handler(n, func20, translate, dict, wrong, right, x, right1, wrong1)

def func18(message, translate, dict, wrong, right, right1, wrong1, x):
    if message.text == 'Нет ❤️‍🩹':
        func8(message, translate, dict, wrong, right, right1, wrong1, x)
    elif message.text == 'Да ☠':
        func19(message, translate, dict, wrong, right, x, right1, wrong1)
    elif message.text == 'Не очень':
        func8(message, translate, dict, wrong, right, right1, wrong1, x)
    elif message.text == 'Хотя...':
        func8(message, translate, dict, wrong, right, right1, wrong1, x)

def func17(message, translate, dict, wrong, right, x, right1, wrong1):
    if message.text == 'Назад':
        func8(message, translate, dict, wrong, right, right1, wrong1, x)

def func16(message, translate, dict, wrong, right, m, right1, wrong1, x):
    if message.text == 'Нет ❤️‍🩹':
        func8(message, translate, dict, wrong, right, right1, wrong1, x)
    elif message.text == 'Да ☠':
        with con:
            cursor.execute('delete from words where word = ?;', (m.split()[0],))
        markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_1 = KeyboardButton('Назад')
        markup.add(button_1)
        n = bot.reply_to(message, 'Слово удалено', reply_markup= markup)
        bot.register_next_step_handler(n, func17, translate, dict, wrong, right, x, right1, wrong1)



def func15(message, translate, dict, wrong, right, m, right1, wrong1, x):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = KeyboardButton('Нет ❤️‍🩹')
    button_2 = KeyboardButton('Да ☠')
    markup.add(button_1, button_2)
    n = bot.reply_to(message, 'Удалить?', reply_markup=markup)
    bot.register_next_step_handler(n, func16, translate, dict, wrong, right, m, right1, wrong1, x)


def func14(message, translate, dict, wrong, right, m, right1, wrong1, x, z):
    if message.text == 'Редактировать':
        n = bot.reply_to(message, 'Введите слово на иностранном языке')
        bot.register_next_step_handler(n, func21, translate, dict, wrong, right, m, right1, wrong1, x, z)

    elif message.text == 'Удалить':
        func15(message, translate, dict, wrong, right, m, right1, wrong1, x)

    elif message.text == 'Назад':
        func9(message, translate, dict, wrong, right, x, right1, wrong1)

def func13(message, translate, dict, wrong, right, m, right1, wrong1, x):
    for i in m:
        if message.text == i:
            markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            button_1 = KeyboardButton('Редактировать')
            button_2 = KeyboardButton('Удалить')
            button_3 = KeyboardButton('Назад')
            markup.add(button_1, button_2, button_3)
            n = bot.reply_to(message, i, reply_markup=markup)
            z = i.split()[0]
            bot.register_next_step_handler(n, func14, translate, dict, wrong, right, i, right1, wrong1, x, z)


def func12(message, translate, dict, wrong, right, right1, wrong1, x):
    l = ''
    for c in dict:
        l += c + ' - ' + translate[dict.index(c)] + '\n'
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = KeyboardButton('Нет ❤️‍🩹')
    button_2 = KeyboardButton('Да ☠')
    button_3 = KeyboardButton('Не очень')
    button_4 = KeyboardButton('Хотя...')
    markup.add(button_1, button_2, button_3, button_4)
    n = bot.reply_to(message, 'Вы точно хотите удалить этот модуль:\n' + l, reply_markup=markup)
    bot.register_next_step_handler(n, func18, translate, dict, wrong, right, right1, wrong1, x)


def func11(message, translate, dict, wrong, right, x, right1, wrong1):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = KeyboardButton('Редактировать')
    button_2 = KeyboardButton('Изучать')
    button_3 = KeyboardButton('Просмотреть')
    markup.add(button_1, button_2, button_3)
    n = bot.reply_to(message, x + ':', reply_markup=markup)
    bot.register_next_step_handler(n, func5, translate, dict, wrong, right, x, right1, wrong1)


def func10(message, translate, dict, wrong, right, right1, wrong1, x):
    m = bot.reply_to(message, 'Введите слово на иностранном языке, для выхода в меню напишите Отмена')
    if message.text == 'Отмена':
        markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_1 = KeyboardButton('Изменить / удалить')
        button_2 = KeyboardButton('Добавить')
        button_3 = KeyboardButton('Удалить модуль')
        button_4 = KeyboardButton('Назад')
        markup.add(button_1, button_2, button_3, button_4)
        n = bot.reply_to(message, x + ':', reply_markup=markup)
        bot.register_next_step_handler(n, func9, translate, dict, wrong, right, x, right1, wrong1)
    else:
        bot.register_next_step_handler(m, func23, translate, dict, wrong, right, right1, wrong1, x)

def func9(message, translate, dict, wrong, right, x, right1, wrong1):
    if message.text == 'Изменить / удалить':
        func6(message, translate, dict, wrong, right, right1, wrong1, x)
    elif message.text == 'Добавить':
        func10(message, translate, dict, wrong, right, right1, wrong1, x)
    elif message.text == 'Удалить модуль':
        func12(message, translate, dict, wrong, right, right1, wrong1, x)
    elif message.text == 'Назад':
        func11(message, translate, dict, wrong, right, x, right1, wrong1)

def func8(message, translate, dict, wrong, right, right1, wrong1, x):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = KeyboardButton('Изменить / удалить')
    button_2 = KeyboardButton('Добавить')
    button_3 = KeyboardButton('Удалить модуль')
    button_4 = KeyboardButton('Назад')
    markup.add(button_1, button_2, button_3, button_4)
    n = bot.reply_to(message, x + ':', reply_markup=markup)
    bot.register_next_step_handler(n, func9, translate, dict, wrong, right, x, right1, wrong1)

def func7(message, translate, dict, wrong, right, x, right1, wrong1):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = KeyboardButton('Редактировать')
    button_2 = KeyboardButton('Изучать')
    button_3 = KeyboardButton('Просмотреть')
    markup.add(button_1, button_2, button_3)
    l = ''
    for c in dict:
        l += c + ' - ' + translate[dict.index(c)] + '\n'
    n = bot.reply_to(message, l, reply_markup= markup)
    bot.register_next_step_handler(n, func5, translate, dict, wrong, right, x, right1, wrong1)

def func6(message, translate, dict, wrong, right, right1, wrong1, x):
    m = []
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for i in dict:
        button_1 = KeyboardButton(i + ' - ' + translate[dict.index(i)])
        markup.add(button_1)
        n = i + ' - ' + translate[dict.index(i)]
        m.append(n)
    b = bot.reply_to(message, 'Слова:', reply_markup=markup)
    bot.register_next_step_handler(b, func13, translate, dict, wrong, right, m, right1, wrong1, x)

def func5(message, translate, dict, wrong, right, x, right1, wrong1):
    if dict == []:
        data2 = cursor.execute('select * from words where num = ?', (x,)).fetchall()
        for b in data2:
            translate.append(b[3])
            dict.append(b[2])
    if message.text == 'Изучать':
        bot.reply_to(message, 'Для выхода нажмите /stop')
        func3(message, translate, dict, wrong, right, right1, wrong1)

    if message.text == 'Редактировать':
        func8(message, translate, dict, wrong, right, right1, wrong1, x)

    if message.text == 'Просмотреть':
        func7(message, translate, dict, wrong, right, x, right1, wrong1)

def func3(message, translate, dict, wrong, right, right1, wrong1):
    right2 = ''
    wrong2 = ''
    m = ''
    n = ''
    if len(translate) == 0:
        markup = InlineKeyboardMarkup(row_width=1)
        button_1 = InlineKeyboardButton(text='Выйти в меню', callback_data='1')
        markup.add(button_1)
        c = len(right1) + len(wrong1)
        h = 100 / c * len(right)
        if h == 100:
            for k in right1:
                if k == right1[len(right1) - 1]:
                    right2 += k
                else:
                    right2 += k + ';\n'
            bot.reply_to(message, 'Всё, ' + str(h).split('.')[0] + '% правильных\n' + right2, reply_markup=markup)
        else:
            for y in wrong1:
                for o in right1:
                    if o == y:
                        right1.remove(y)
            for l in wrong1:
                if l == wrong1[len(wrong1) - 1]:
                    wrong2 += l
                else:
                    wrong2 += l + ';\n'
            for k in right1:
                if k == right1[len(right1) - 1]:
                    right2 += k
                else:
                    right2 += k + ';\n'
            bot.reply_to(message, 'Всё, ' + str(h).split('.')[0] + '% правильных\n' + 'Не праавильные:\n' + wrong2 + '\n' + 'Правильные:\n' + right2, reply_markup=markup)
        return
    else:
        if len(wrong + right) % 7 == 0 and len(wrong + right) != 0:
            for i in wrong:
                if len(wrong) < 2 or i == wrong[len(wrong) - 1]:
                    m += i
                else:
                    m += i + ';\n'
            for t in right:
                if len(right) < 2 or t == right[len(right) - 1]:
                    n += t
                else:
                    n +=t + ';\n'
            bot.reply_to(message, '❌ Не правильных ' + str(len(wrong)) + ' ❌:\n' + m + '\n' + '✅ Правильных ' + str(len(right)) + ' ✅:\n' + n)
            g = random.randrange(len(translate))
            t = bot.reply_to(message, translate[g])
            bot.register_next_step_handler(t, func4, translate, dict, g, wrong, right, right1, wrong1)
        else:
            g = random.randrange(len(translate))
            t = bot.reply_to(message, translate[g])
            bot.register_next_step_handler(t, func4, translate, dict, g, wrong, right, right1, wrong1)


def func4(message, translate, dict, n, wrong, right, right1, wrong1):
    if message.text == '/stop':
        markup = InlineKeyboardMarkup(row_width=1)
        button_1 = InlineKeyboardButton(text='Выйти в меню', callback_data='1')
        markup.add(button_1)
        bot.reply_to(message, 'Всё', reply_markup=markup)
        return
    if message.text == dict[n]:
        bot.reply_to(message, '✅ Правильно ✅')
        right1.append(dict[n])
        right.append(dict[n])
        del translate[n]
        del dict[n]
        func3(message, translate, dict, wrong, right, right1, wrong1)
    else:
        wrong1.append(dict[n])
        wrong.append(dict[n])
        bot.reply_to(message, '❌ Не правильно ❌, ' + dict[n])
        func3(message, translate, dict, wrong, right, right1, wrong1)


@bot.callback_query_handler(func= lambda call: True)
def callback(call):
    n = []
    v = 3
    p = 0
    if call.data == '1':
        markup = InlineKeyboardMarkup(row_width=1)
        button_1 = InlineKeyboardButton(text='Создать модуль', callback_data='2')
        button_2 = InlineKeyboardButton(text='Мои модули', callback_data='3')
        markup.add(button_1, button_2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Helper menu:',reply_markup=markup)

    elif call.data == '2':
        message = bot.reply_to(call.message, 'Как будет называться этот модуль?')
        bot.register_next_step_handler(message, func, p)

    elif call.data == '3':
        users_id = call.message.chat.id
        t = 0
        data1 = cursor.execute('select * from words where id = ?', (users_id,)).fetchall()
        for i in data1:
            t = i[0]
            n.append(t)
        n = set(n)
        if t == 0:
            markup = InlineKeyboardMarkup(row_width=1)
            button_1 = InlineKeyboardButton(text='Назад', callback_data='1')
            markup.add(button_1)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='У вас пока нет ни одного модуля',reply_markup=markup)
        else:
            markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            for m in n:
                v += 1
                x = KeyboardButton(m)
                markup.add(x)
            bot.reply_to(call.message, 'Вот ваши модули', reply_markup=markup)



def func(message, p, modul = ''):
    users_id = message.chat.id
    data1 = cursor.execute('select * from words where id = ?', (users_id,)).fetchall()
    for i in data1:
        t = i[4]
        if int(t) > p:
            p = int(t)
    if message.text == '...':
        markup = InlineKeyboardMarkup(row_width=1)
        button_1 = InlineKeyboardButton(text='выйти в меню', callback_data='1')
        markup.add(button_1)
        bot.reply_to(message, 'Модуль создан', reply_markup=markup)
        return
    if modul == '':
        bot.reply_to(message, 'Теперь введите слово на иностранном языке')
        word = bot.reply_to(message, 'Слово:')
        bot.register_next_step_handler(word, func1, message.text, p)
    else:
        func1(message, modul, p)

def func1(message, modul, p):
    word1 = bot.reply_to(message, 'Перевод:')
    bot.register_next_step_handler(word1, func2, message.text, modul, p)

def func2(word1, word, modul, p):
    n = p + 1
    with con:
        cursor.execute('INSERT INTO words(num,id, word,translate, num1) VALUES(?,?,?,?,?)',(modul, word1.from_user.id, word, word1.text, n,))
    n = bot.reply_to(word1, 'Введите ... для завершения либо следующее слово')
    bot.register_next_step_handler(n, func, modul, p)

bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.add_custom_filter(custom_filters.TextStartsFilter())
bot.add_custom_filter(custom_filters.ChatFilter())
bot.infinity_polling()

