from save_and_load import Users
import telebot
from telebot import types

List = Users("DataBase")
print(List.users)
def push_back_List(message):
    global List
    if not message.chat.id in List.users:
        List.add(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    elif List.users[message.chat.id] != [message.from_user.first_name, message.from_user.last_name, message.from_user.username] :
            List.users[message.chat.id] = [message.from_user.first_name, message.from_user.last_name, message.from_user.username]
            List.save()

bot = telebot.TeleBot('1159344872:AAHPZvYQrm8vNILYunGT-qhefwkoUzHQmyI')

def return_String (message):
    String = ''
    if message.from_user.first_name != None and message.from_user.first_name != '..,':
        String += message.from_user.first_name + " "
    if message.from_user.last_name != None :
        String += message.from_user.last_name + " "
    if  message.from_user.username != None :
        String += message.from_user.username + " "
    return String

@bot.message_handler(commands=['start'])
def start(message):
    global List
    push_back_List(message)
    bot.send_message(message.chat.id, "Привет, ублюдок")
    String = return_String(message) + ' use "/start"'
    if message.chat.id != 422752846 :
        bot.send_message(422752846, String)
    print(String + "\nBot:\n-Привет, ублюдок\n")

@bot.message_handler(commands=['take_control'])
def take_control(message):
    if message.chat.id != 422752846 :
        bot.send_message(422752846, "Это комманда только для админа, ты не админ!")
        return
    global List
    keyboard = types.InlineKeyboardMarkup()
    for key in List.users.keys():
        string = ''
        for i in List.users[key]:
            string += str(i) + ' '
        callback_button = types.InlineKeyboardButton(text=string, callback_data="test")
        keyboard.add(callback_button)
    bot.send_message(message.chat.id, "Выбери ключ:", reply_markup=keyboard)

@bot.message_handler(commands=['list_clear'])
def take_control(message):
    if message.chat.id != 422752846 :
        bot.send_message(422752846, "Это комманда только для админа, ты не админ!")
        return
    List.users.clear()

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    global List
    push_back_List(message)
    if message.text == 'да' or message.text == 'Да' or message.text =='Да?' or message.text =='Да!':
        bot.send_message(message.chat.id, 'Нет!')
    else:
        bot.send_message(message.chat.id, message.text)
        String = return_String(message) + ":\n-" + message.text + "\n"
        print(String)
        print("Bot:\n-" + message.text + '\n')
        if message.chat.id != 422752846 :
            bot.send_message(422752846, String)

if __name__ == '__main__':
     bot.polling(none_stop=True)
