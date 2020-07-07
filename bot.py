import telebot, requests, random
from telebot import types
from bs4 import BeautifulSoup
from save_and_load import Users
from Token import token


bot = telebot.TeleBot(token)
iter = 0
List = Users("DataBase")
print(List.users)

def monney(URL):
    Dolar_rub = URL
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    full_page = requests.get(Dolar_rub, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span", {"class": "converter-100__info-currency-bold"})
    string = ''
    for i in convert[0].text:
        if i == ' ':
            break
        string += i
    return string

def cut(data, begin, end):
    list = {}
    step = begin
    for key in List.users.keys():
        if step == end:
            break
        list[key] = data[key]
        step += 1
    return list

def next(list):
    keyboard = types.InlineKeyboardMarkup()
    for key in list.keys():
        string = ''
        for i in list[key]:
            string += str(i) + ' '
        callback_button = types.InlineKeyboardButton(text=string, callback_data=key)
        keyboard.add(callback_button)
    return keyboard

def push_back_List(message):
    global List
    if not message.chat.id in List.users:
        List.add(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    elif List.users[message.chat.id] != [message.from_user.first_name, message.from_user.last_name, message.from_user.username] :
            List.users[message.chat.id] = [message.from_user.first_name, message.from_user.last_name, message.from_user.username]
            List.save()

def return_String (message):
    String = ''
    if message.from_user.first_name != None :
        String += message.from_user.first_name + " "
    if message.from_user.last_name != None :
        String += message.from_user.last_name + " "
    if message.from_user.username != None :
        String += message.from_user.username + " "
    return String

@bot.message_handler(commands=['start'])
def start(message):
    global List
    push_back_List(message)
    bot.send_message(message.chat.id, "Приветики")
    String = return_String(message) + ' use "/start"'
    if message.chat.id != 422752846 :
        bot.send_message(422752846, String)
    print(String + "\nBot:\n-Приветики\n")

@bot.message_handler(commands=['take_control'])
def take_control(message):
    if message.chat.id != 422752846 :
        bot.send_message(422752846, "Это комманда только для админа, ты не админ!")
        return
    global iter
    keyboard = types.InlineKeyboardMarkup()
    list = cut(List.users, iter, iter + 3)
    next_list_button = types.InlineKeyboardButton(text="Next", callback_data="next")
    keyboard.add(next(list), next_list_button)
    if next_list_button.callback_data == "next":
        iter += 3
        list = cut(List.users, iter, iter + 3)
        keyboard = next(list)
        keyboard.add(next_list_button)
    bot.send_message(message.chat.id, "Выбери ключ:", reply_markup=keyboard)

@bot.message_handler(commands=['currencies'])
def currencies(message):
    keyboard = types.InlineKeyboardMarkup()
    curr_bel = types.InlineKeyboardButton(text= monney('https://myfin.by/converter/usd-byn/1') + " бел. руб.", callback_data="много")
    curr_eur = types.InlineKeyboardButton(text= monney('https://myfin.by/converter/usd-eur/1') + " евро", callback_data="много")
    curr_rub = types.InlineKeyboardButton(text= monney('https://myfin.by/converter/usd-rub/1') + " рус.руб.", callback_data="много")
    keyboard.add(curr_eur, curr_rub)
    keyboard.add(curr_bel)
    bot.send_message(message.chat.id, "Один доллар равен:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global List
    if call.data == "много":
        answer = ["Кааапец, дa???", "уффф", "........", "дааа, куда катится этот мир...", "все из-за Гейца!!!", "фу, воняет!", "@#$%^& рот!!!"]
        bot.send_message(call.message.chat.id, random.choice(answer))
    if call.data in List.users:
        print(List.users[call.data])
    if call.data == "Next":
        global iter
        iter += 3
        list = cut(List.users, iter, iter + 3)
        keyboard = next(list)
        keyboard.add(types.InlineKeyboardButton(text="Next", callback_data="next"))

@bot.message_handler(commands=['list_clear'])
def list_clear(message):
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
