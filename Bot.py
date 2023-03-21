import json
import time

import PyPDF2
import docx
import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot('6034077201:AAHICg_ZMoB6knQ8atPjdmmt9DgvKE_Obec')

data = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    # Check if user is already registered
    with open('users.json', 'r') as f:
        data = json.load(f)
        if str(message.chat.id) in data:
            name = data[str(message.chat.id)]["real_name"]
            bot.send_message(message.chat.id, f"Welcome back, {name}! ",
                             reply_markup=menu())
        else:
            bot.send_message(message.chat.id, "Hi! Please enter your name.", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: message.text == "Delivery")
def Delivery(message):
    with open('users.json', 'r') as f:
        data = json.load(f)
        if str(message.chat.id) in data:
            if data[str(message.chat.id)]["phone_number"]:
                bot.send_message(message.chat.id, "Ertib from Tulu dimtu", reply_markup=delivery_choice())
            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button = types.KeyboardButton(text="Send Phone Number", request_contact=True)
                keyboard.add(button)
                bot.send_message(message.chat.id, f"Please click 'Send Phone Number' button", reply_markup=keyboard)
                return
        else:
            bot.send_message(message.chat.id, "Please register first /start.")


@bot.message_handler(func=lambda message: message.text == "Stationary")
def Stationary(message):
    bot.send_message(message.chat.id, "Stationary ......")


@bot.message_handler(func=lambda message: message.text == "Help")
def Help(message):
    bot.send_message(message.chat.id, "Help")


@bot.message_handler(func=lambda message: message.text == "Print")
def Pprint(message):
    with open('users.json', 'r') as f:
        data = json.load(f)
        if str(message.chat.id) in data:
            if data[str(message.chat.id)]["phone_number"]:
                bot.send_message(message.chat.id, "Please send your file in doc or pdf format")

            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button = types.KeyboardButton(text="Send Phone Number", request_contact=True)
                keyboard.add(button)
                bot.send_message(message.chat.id, f"Please click 'Send Phone Number' button", reply_markup=keyboard)
                return
        else:
            bot.send_message(message.chat.id, "Please register first /start.")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    # user_id = message.from_user.id
    # filter only PDF and DOCX files
    with open('users.json', 'r') as f:
        data = json.load(f)
        if str(message.chat.id) in data:
            if data[str(message.chat.id)]["phone_number"]:
                if message.document.mime_type == 'application/pdf' or message.document.file_name.endswith(
                        '.docx') or message.document.file_name.endswith('.doc'):
                    # save the file to disk
                    file_id = message.document.file_id
                    file_info = bot.get_file(file_id)
                    file_path = file_info.file_path
                    file_name = message.document.file_name
                    print(file_name, 999)
                    downloaded_file = bot.download_file(file_path)
                    with open(file_name, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    bot.send_message(message.chat.id, "What do you want", reply_markup=print_choice(file_name))
                else:
                    bot.send_message(message.chat.id, "Sorry, We only accept PDF or DOC and DOCX files.")
                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button = types.KeyboardButton(text="Send Phone Number", request_contact=True)
                keyboard.add(button)
                bot.send_message(message.chat.id, f"Please click 'Send Phone Number' button",
                                 reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Please register first /start.")


def print_choice(file_name):
    markup = types.InlineKeyboardMarkup()
    for ans in ["Normal print", "Color print", "Normal print with blaaa", "Color print with blaaa"]:
        btn = types.InlineKeyboardButton(
            ans, callback_data=f"**{ans}+{file_name}")
        markup.add(btn)
    return markup


def delivery_choice():
    markup = types.InlineKeyboardMarkup()
    for ans in ["Normal", "Normal Plus", "Special"]:
        btn = types.InlineKeyboardButton(
            ans, callback_data=f"=={ans}")
        markup.add(btn)
    return markup


print_price_list = {
    "Normal print": 5, "Color print": 15, "Normal print with blaaa": 20, "Color print with blaaa": 25
}

ertib_price_list = {
    "Normal": 45, "Normal Plus": 50, "Special": 55
}


# create a function to handle user input
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    typ = call.data[2:]
    with open('users.json', 'r') as f:
        data = json.load(f)
        if str(user_id) in data:
            if data[str(user_id)]["phone_number"]:
                if "**" in call.data:
                    file_name = call.data.split("+")[1]
                    # print(file_name, 99)
                    ext = file_name.split(".")[-1]
                    if ext == "pdf":
                        with open(file_name, 'rb') as file:
                            pdf_reader = PyPDF2.PdfFileReader(file)
                            num_pages = pdf_reader.getNumPages()
                    else:
                        doc = docx.Document(file_name)
                        num_pages = len(doc.sections)
                    price = num_pages * print_price_list[typ.split('+')[0]]
                    markup = types.InlineKeyboardMarkup()
                    btn = types.InlineKeyboardButton(
                        "Click this button after you paid",
                        callback_data=f"--{num_pages}+{file_name}+{typ.split('+')[0]}")
                    markup.add(btn)
                    cap = f"Total Pages :- {num_pages}\n" \
                          f"Price :- {price}\n" \
                          f"Payment Methods\n" \
                          f"    - CBE (100987543)\n" \
                          f"    - Telebirr (0987654321)"
                    bot.send_message(call.message.chat.id, cap, reply_markup=markup)
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                elif "--" in call.data:
                    file_name = call.data.split("+")[1]

                    with open(file_name, 'rb') as file:
                        num_pages = int(typ.split("+")[0])
                        ty = typ.split("+")[-1]
                        cap = f"From         :- {data[str(user_id)]['real_name']}\n" \
                              f"Phone Number :- {data[str(user_id)]['phone_number']}\n" \
                              f"Type         :- {ty}|nNo page      :- {num_pages}\n" \
                              f"Price        :- {num_pages * print_price_list[ty]}"
                        bot.send_document(chat_id="-1001674209692", document=file, caption=cap)
                        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                        bot.send_message(user_id, "Thank you for working with us.\n"
                                                  "Within 5 Min we will call you if you paid.\n"
                                                  "if don't get any response from us contact us 0912345678 ")
                elif "==" in call.data:
                    query = call.data[2:]
                    markup = types.InlineKeyboardMarkup(row_width=3)
                    a = [types.InlineKeyboardButton(
                        ans, callback_data=f"||{ans}_{query}") for ans in range(1, 13)]
                    markup.add(*a[0:3])
                    markup.add(*a[3:6])
                    markup.add(*a[6:9])
                    markup.add(*a[9:12])
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(user_id, "How much do you want", reply_markup=markup)
                elif "||" in call.data:
                    no, typpe = call.data[2:].split("_")
                    price = int(no) * ertib_price_list[typpe]
                    markup = types.InlineKeyboardMarkup()
                    btn = types.InlineKeyboardButton(
                        "Click this button after you paid", callback_data=f"!!{no}+{price}+{typpe}")
                    markup.add(btn)
                    cap = f"Item     :- {typpe} Ertib\n" \
                          f"Quantity :- {no}\n" \
                          f"Price    :- {price}\n" \
                          f"Payment Methods  \n" \
                          f"   - CBE (100987543) \n" \
                          f"   - Telebirr (0987654321) "

                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                    bot.send_message(call.message.chat.id, cap, reply_markup=markup)
                elif "!!" in call.data:
                    Quantity = int(typ.split("+")[0])
                    ty = call.data.split("+")[-1]
                    price = typ.split("+")[1]
                    cap = f"From :- {data[str(user_id)]['real_name']} " \
                          f"\n Phone Number :- {data[str(user_id)]['phone_number']} " \
                          f"\n Type         :- {ty} Ertib " \
                          f"\n  Quantity      :- {Quantity}" \
                          f"\n Price        :- {price}"
                    bot.send_message(chat_id="-1001674209692", text=cap)
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(user_id, "Thank you for working with us.\n"
                                              "Within 5 Min we will call you if you paid.\n"
                                              "if don't get any response from us contact us 0912345678 ")
            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button = types.KeyboardButton(text="Send Phone Number", request_contact=True)
                keyboard.add(button)
                bot.send_message(call.message.chat.id, f"Please click 'Send Phone Number' button",
                                 reply_markup=keyboard)

        else:
            bot.send_message(user_id, "Please register first /start.")


@bot.message_handler(func=lambda message: True)
def name_input(message):
    text = message.text
    with open('users.json', 'r') as f:
        data = json.load(f)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text="Send Phone Number", request_contact=True)
    keyboard.add(button)
    if "09" in text or "+251" in text:
        bot.send_message(message.chat.id,
                         f"Please, Don't write your phone number just click 'Send Phone Number' button",
                         reply_markup=keyboard)
    elif str(message.chat.id) in data:
        if data[str(message.chat.id)]["phone_number"] is None:
            bot.send_message(message.chat.id,
                             f"Please, Don't write your phone number just click 'Send Phone Number' button",
                             reply_markup=keyboard)
    elif str(message.chat.id) not in data:
        if " " not in text or len(text) < 7:
            bot.send_message(message.chat.id, "Please, enter your full name.", reply_markup=ReplyKeyboardRemove())
            return
        print(message.chat.id, data)
        with open('users.json', 'w') as fz:
            data[message.chat.id] = {"real_name": text, "phone_number": None}
            json.dump(dict(data), fz, indent=4)
        bot.send_message(message.chat.id, f"Thanks {text}! Please provide your phone number.", reply_markup=keyboard)

    # else:
    #     bot.send_message(message.chat.id, f"Thanks {t ext}! Please provide your phone number.", reply_markup=keyboard)


def menu():
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton(text='Delivery')
    item2 = telebot.types.KeyboardButton(text='Print')
    item5 = telebot.types.KeyboardButton(text='Stationary')
    item4 = telebot.types.KeyboardButton(text='Help')
    markup.add(item1, item2, item4, item5, )
    return markup


@bot.message_handler(content_types=['contact'])
def phone_input(message):
    user_id = message.chat.id
    with open('users.json', 'r') as f:
        data = json.load(f)
        if str(user_id) in data:
            phone_number = message.contact.phone_number
            user_id = message.from_user.id

            with open('users.json', 'r') as f:
                data = json.load(f)

            with open('users.json', 'w') as f:
                username = message.from_user.username
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name if message.from_user.last_name else ""
                data[str(message.chat.id)]["first_name"] = first_name
                data[str(message.chat.id)]["last_name"] = last_name
                data[str(message.chat.id)]["username"] = username
                data[str(message.chat.id)]["phone_number"] = phone_number
                json.dump(dict(data), f, indent=4)
            bot.send_message(
                user_id, "Thanks for registering,\n Choose an option:", reply_markup=menu())
        else:
            bot.send_message(user_id, "Please register first /start.")


while True:
    try:
        bot.polling(non_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(3)
