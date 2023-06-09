import json
import time
import traceback
import uuid

import PyPDF2
import docx
import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove

from LANG import *

bot = telebot.TeleBot('6034077201:AAHICg_ZMoB6knQ8atPjdmmt9DgvKE_Obec')

data = {}
pay_data = {"CBE": "- CBE (1000385300291)", "CBE-BIRR": "- CBE-BIRR (0912334223)",
            "Abyssinia": "- Abyssinia Bank (87740986)", "Lion": "- Lion Bank (0031157161553)",
            "Telebirr": "- Telebirr (0912334223)"}


def menu(my_id, data):
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton(text=deliveryy[data[my_id]["lang"]])
    item2 = telebot.types.KeyboardButton(text=printt[data[my_id]["lang"]])
    item5 = telebot.types.KeyboardButton(text=Languagey[data[my_id]["lang"]])
    item4 = telebot.types.KeyboardButton(text=Referrals[data[my_id]["lang"]])
    item6 = telebot.types.KeyboardButton(text=allmart[data[my_id]["lang"]])
    item7 = telebot.types.KeyboardButton(text=help[data[my_id]["lang"]])
    markup.add(item1, item2, item4, item5, item6, item7)
    return markup


@bot.message_handler(commands=['start'])
def start_command(message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    my_id = str(message.from_user.id)
    if my_id in data:
        if len(data[my_id]) > 2:
            if data[my_id]["phone_number"]:
                name = data[my_id]["real_name"]
                bot.send_message(message.chat.id, Welcome_back[data[my_id]["lang"]].format(name),
                                 reply_markup=menu(my_id, data))

            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button = types.KeyboardButton(text=Send_Phone[data[my_id]["lang"]], request_contact=True)

                keyboard.add(button)
                bot.send_message(message.chat.id, Please_Send_Phone[data[my_id]["lang"]], reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Hi! Please enter your name.", reply_markup=ReplyKeyboardRemove())

    elif message.text.startswith('/start '):
        with open('coupon.json', 'r') as fl:
            coupon = json.load(fl)
        coupon_code = message.text.split(' ')[1]
        user_id = coupon[coupon_code]["id"]
        if coupon_code in coupon and my_id not in coupon[coupon_code]["referred"]:
            data[my_id] = {"invited": user_id, "lang": "ENGLISH"}
            coupon[coupon_code]["referred"].append(my_id)
            coupon[coupon_code]["count"] += 1
            with open("coupon.json", "w") as fg:
                json.dump(dict(coupon), fg, indent=4)
        with open("users.json", "w") as fg:
            json.dump(dict(data), fg, indent=4)
        bot.send_message(message.chat.id, enter_your_name["ENGLISH"], reply_markup=ReplyKeyboardRemove())

        return
    else:
        data[my_id] = {"invited": None, "lang": "ENGLISH"}
        with open("users.json", "w") as fg:
            json.dump(dict(data), fg, indent=4)
        bot.send_message(message.chat.id, enter_your_name[data[my_id]["lang"]], reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: message.text in ["Help"])
def Help(message):
    bot.send_message(message.chat.id,
                     "For more info contact our service center \n0912334223 \n@grace_4_real")


@bot.message_handler(func=lambda message: message.text in ["All Mart"])
def All_Mart(message):
    bot.send_message(message.chat.id,
                     "subscribe the channel, Unleash your shopping potential \n The Falcon Group \n https://t.me/the_Falcongroup")


@bot.message_handler(
    func=lambda message: message.text in ["Delivery", "ምብፃሕ", "Qaqqabsiisuu", "ማድረስ"])
def Delivery(message):
    with open('users.json', 'r') as f:
        data = json.load(f)
        my_id = str(message.from_user.id)
        if my_id in data:
            if data[my_id]["phone_number"]:
                bot.send_message(message.chat.id,"Swift Delivery Soaring With Falcon")
                bot.send_message(message.chat.id, deliveray[data[my_id]["lang"]], reply_markup=delivery_choice())
            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button = types.KeyboardButton(text=Send_Phone[data[my_id]["lang"]], request_contact=True)
                keyboard.add(button)
                bot.send_message(message.chat.id, Please_Send_Phone[data[my_id]["lang"]], reply_markup=keyboard)
                return
        else:
            bot.send_message(message.chat.id, register_first[data[my_id]["lang"]])


@bot.message_handler(func=lambda message: message.text in ['Language', "ቋንቋ", "Afaan"])
def Stationary(message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    my_id = str(message.from_user.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn = types.InlineKeyboardButton(
        "ENGLISH",
        callback_data=f"ENGLISH")
    btn2 = types.InlineKeyboardButton(
        "AFFAN_OROMO",
        callback_data=f"AFFAN_OROMO")
    btn3 = types.InlineKeyboardButton(
        "ትግርኛ",
        callback_data=f"Tigrinya")
    btn33 = types.InlineKeyboardButton(
        "AMHARIC",
        callback_data=f"AMHARIC")

    markup.add(btn, btn2, btn3, btn33)
    bot.send_message(message.chat.id, c_lang[data[my_id]["lang"]], reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text in ['Balance and referral', "የእኔ ቀሪ ሂሳብ", "Madaallii koo.", "የእኔ ቀሪ ሂሳብ"])
def Referral(message):
    user_id = str(message.from_user.id)
    with open('users.json', 'r') as f:
        data = json.load(f)
        if user_id in data:
            with open("coupon.json", "r") as file:
                coupon = json.load(file)
            link = data[user_id]["link"]
            count = coupon[data[user_id]["coupon_code"]]["count"]
            coins = coupon[data[user_id]["coupon_code"]]["coins"]
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(
                withdraw[data[user_id]["lang"]], callback_data="-withdraw")
            markup.add(btn)
            bot.send_message(message.chat.id, referral_link[data[user_id]["lang"]].format(link))
            bot.send_message(message.chat.id,
                             invite_have[data[user_id]["lang"]].format(count, coins), reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Help")
def Help(message):
    bot.send_message(message.chat.id, "Help")


@bot.message_handler(
    func=lambda message: message.text in ["Print", "ህትመት", "Maxxansa", "ሕትመት"])
def Pprint(message):
    with open('users.json', 'r') as f:
        data = json.load(f)
        my_id = str(message.from_user.id)
        if my_id in data:
            if data[my_id]["phone_number"]:
                bot.send_message(message.chat.id, "Print With Precision Powered By Falcon!")
                bot.send_message(message.chat.id, send_file[data[my_id]["lang"]])

            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button = types.KeyboardButton(text=send_file[data[my_id]["lang"]], request_contact=True)
                keyboard.add(button)
                bot.send_message(message.chat.id, Please_Send_Phone[data[my_id]["lang"]], reply_markup=keyboard)
                return
        else:
            bot.send_message(message.chat.id, register_first[data[my_id]["lang"]])


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'sticker'])
def handle_document(message):
    my_id = str(message.from_user.id)
    with open('users.json', 'r') as f:
        data = json.load(f)
    try:
        if message.document.file_name.endswith('.docx') or message.document.file_name.endswith(
                '.doc') or message.document.file_name.endswith('.pdf'):
            if my_id in data:
                if data[my_id]["phone_number"]:
                    file_id = message.document.file_id
                    file_info = bot.get_file(file_id)
                    file_path = file_info.file_path
                    file_name = message.document.file_name
                    downloaded_file = bot.download_file(file_path)
                    with open(file_name, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    bot.send_message(message.chat.id, what[data[my_id]["lang"]], reply_markup=print_choice(file_name))

                else:
                    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                    button = types.KeyboardButton(text=Send_Phone[data[my_id]["lang"]], request_contact=True)
                    keyboard.add(button)
                    bot.send_message(message.chat.id, Please_Send_Phone[data[my_id]["lang"]],
                                     reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, register_first[data[my_id]["lang"]])
        else:
            bot.send_message(message.chat.id, sorry_file[data[my_id]["lang"]])
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except:
        bot.send_message(message.chat.id, sorry_file[data[my_id]["lang"]])
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


def print_choice(file_name):
    markup = types.InlineKeyboardMarkup()
    for ans in ["Normal print", "Color print", "Normal print with blaaa", "Color print with blaaa"]:
        btn = types.InlineKeyboardButton(
            ans, callback_data=f"-prints{ans}+{file_name}")
        markup.add(btn)
    return markup


def delivery_choice():
    markup = types.InlineKeyboardMarkup()
    for ans in ["Normal Ertib", "Special Ertib", "Premium Ertib", "Plumpy Nut"]:
        btn = types.InlineKeyboardButton(
            ans, callback_data=f"-Deli{ans}")
        markup.add(btn)
    return markup


print_price_list = {
    "Normal print": 5, "Color print": 15, "Normal print with blaaa": 20, "Color print with blaaa": 25
}

ertib_price_list = {
    "Normal Ertib": 45, "Special Ertib": 50, "Premium Ertib": 55, "Plumpy Nut": 35,
}

payment_gateway = ["    - CBE (100987543)\n", "   - Telebirr (0987654321)\n"]


# create a function to handle user input
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    typ = call.data[2:]

    with open('users.json', 'r') as f:
        data = json.load(f)
        if str(user_id) in data:
            if data[str(user_id)]["phone_number"]:
                if "-prints" in call.data:
                    typ = call.data[7:]
                    file_name = call.data.split("+")[1]
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
                        pay_cash[data[str(user_id)]["lang"]],
                        callback_data=f"-print_cash{num_pages}+{file_name}+{call.data[6:].split('+')[0]}+{price}")
                    btn2 = types.InlineKeyboardButton(
                        pay_falcon[data[str(user_id)]["lang"]],
                        callback_data=f"-print_coin{num_pages}+{file_name}+{call.data[6:].split('+')[0]}+{price}")

                    markup.add(btn, btn2)
                    cap = payment[data[str(user_id)]["lang"]].format(num_pages, price)
                    bot.send_message(call.message.chat.id, cap, reply_markup=markup)
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                elif "-print_cash" in call.data:
                    typ = call.data[11:]
                    num_pages, file_name, ty, price = typ.split("+")

                    mark = types.InlineKeyboardMarkup(row_width=2)
                    btn = types.InlineKeyboardButton(
                        after_paid[data[str(user_id)]["lang"]],
                        callback_data=f"-f_print{num_pages}+{file_name}+{call.data[6:].split('+')[0]}+{price}")
                    mark.add(btn)
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    cap = payment_lang[data[str(user_id)]["lang"]] + "".join(payment_gateway)

                    bot.send_message(user_id, cap, reply_markup=mark)
                elif "-withdraw" in call.data:
                    with open('coupon.json', 'r') as file:
                        coupon = json.load(file)
                    coinss = coupon[data[str(user_id)]["coupon_code"]]["coins"]
                    if coinss >= 1:
                        markup = types.InlineKeyboardMarkup(row_width=3)
                        a = [types.InlineKeyboardButton(
                                ans, callback_data=f"+withdraw{ans}") for ans in range(1, 13)]
                        markup.add(*a[0:3])
                        markup.add(*a[3:6])
                        markup.add(*a[6:9])
                        markup.add(*a[9:12])
                        bot.send_message(user_id, how_much[data[str(user_id)]["lang"]], reply_markup=markup)
                    else:
                        bot.send_message(user_id, not_coins[data[str(user_id)]["lang"]])
                elif "+withdraw" in call.data:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    no = call.data[9:]
                    markup = types.InlineKeyboardMarkup()
                    for k, v in pay_data.items():
                        btn = types.InlineKeyboardButton(
                            k, callback_data=f"$withdrawF{k}+{no}")
                        markup.add(btn)
                    bot.send_message(user_id, payment_lang[data[str(user_id)]["lang"]], reply_markup=markup)

                elif "$withdrawF" in call.data:
                    ty, no = call.data[10:].split("+")
                    cap = f"From         :- {data[str(user_id)]['real_name']}\n" \
                          f"Phone Number :- {data[str(user_id)]['phone_number']}\n" \
                          f"Type         :- {ty}\n" \
                          f"Amount        :- {no}"
                    markup = types.InlineKeyboardMarkup()
                    btn = types.InlineKeyboardButton(
                        "Done", callback_data=f"*withdrawF{str(user_id)}")
                    markup.add(btn)
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                    bot.send_message(chat_id="-1001674209692", text=cap, reply_markup=markup)
                    bot.send_message(user_id, thank_you[data[str(user_id)]["lang"]].format("withdraw"))

                elif "*withdrawF" in call.data:
                    bot.send_message(user_id, payment_Done[data[str(user_id)]["lang"]])
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)



                elif "-print_coin" in call.data:
                    with open('coupon.json', 'r') as file:
                        coupon = json.load(file)
                    typ = call.data[11:]
                    num_pages, file_name, ty, price = typ.split("+")
                    coinss = coupon[data[str(user_id)]["coupon_code"]]["coins"]
                    sub = float(price) / 10
                    if coinss >= sub:
                        with open('coupon.json', 'w') as files:
                            coupon[data[str(user_id)]["coupon_code"]]["coins"] -= sub
                            json.dump(dict(coupon), files, indent=4)
                        num_pages, file_name, ty, price = typ.split("+")
                        cap = f"From         :- {data[str(user_id)]['real_name']}\n" \
                              f"Phone Number :- {data[str(user_id)]['phone_number']}\n" \
                              f"Type         :- {ty}\n" \
                              f"No page      :- {num_pages}\n" \
                              f"Price        :- {price}"

                        with open(file_name, 'rb') as file:
                            bot.send_document(chat_id="-1001674209692", document=file, caption=cap)
                        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                        bot.send_message(user_id, thank_you[data[str(user_id)]["lang"]].format("Printing"))
                    else:
                        markup = types.InlineKeyboardMarkup()
                        btn = types.InlineKeyboardButton(
                            pay_cash[data[str(user_id)]["lang"]],
                            callback_data=f"-print_cash{num_pages}+{file_name}+{call.data[6:].split('+')[0]}+{price}")
                        markup.add(btn)
                        bot.send_message(user_id, not_coins[data[str(user_id)]["lang"]], reply_markup=markup)
                elif "-f_print" in call.data:
                    num_pages, file_name, ty, price = typ.split("+")
                    cap = f"From         :- {data[str(user_id)]['real_name']}\n" \
                          f"Phone Number :- {data[str(user_id)]['phone_number']}\n" \
                          f"Type         :- {ty}\n" \
                          f"No page      :- {num_pages}\n" \
                          f"Price        :- {price}"
                    mark = types.InlineKeyboardMarkup(row_width=2)
                    btn = types.InlineKeyboardButton(
                        "Real", callback_data=f"((Real_{user_id}")
                    btn2 = types.InlineKeyboardButton(
                        "Fake", callback_data=f"((Fake_{user_id}")
                    mark.add(btn, btn2)
                    with open(file_name, 'rb') as file:
                        bot.send_document(chat_id="-1001674209692", document=file, caption=cap, reply_markup=mark)
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(user_id, thank_you[data[str(user_id)]["lang"]].format("Printing"))
                elif call.data in ["ENGLISH", "AMHARIC", "AFFAN_OROMO", "Tigrinya"]:
                    with open('users.json', 'w') as fz:
                        data[str(user_id)]["lang"] = call.data

                        json.dump(dict(data), fz, indent=4)
                    bot.send_message(user_id, success[data[str(user_id)]["lang"]],
                                     reply_markup=menu(str(user_id), data))
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                elif "-Deli" in call.data:
                    query = call.data[5:]
                    markup = types.InlineKeyboardMarkup(row_width=3)
                    a = [types.InlineKeyboardButton(
                        ans, callback_data=f"+Deli{ans}_{query}") for ans in range(1, 13)]
                    markup.add(*a[0:3])
                    markup.add(*a[3:6])
                    markup.add(*a[6:9])
                    markup.add(*a[9:12])
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(user_id, how_much[data[str(user_id)]["lang"]], reply_markup=markup)
                elif "((" in call.data:
                    if "Real" in typ:
                        with open('coupon.json', 'r') as file:
                            coupon = json.load(file)
                        idd = typ.split("_")[-1]
                        if data[str(idd)]['invited']:
                            in_id = data[data[str(idd)]['invited']]
                            in_coupon = in_id['coupon_code']
                            with open('coupon.json', 'w') as files:
                                coupon[in_coupon]["coins"] += 0.2
                                json.dump(dict(coupon), files, indent=4)
                        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                      reply_markup=None)
                        bot.send_message(idd, payment_verified[data[str(user_id)]["lang"]])

                        return
                    bot.send_message(typ.split("_")[-1], payment_not_verified[data[str(user_id)]["lang"]])
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                elif "+Deli" in call.data:
                    no, typpe = call.data[5:].split("_")

                    price = int(no) * ertib_price_list[typpe]
                    markup = types.InlineKeyboardMarkup()
                    btn = types.InlineKeyboardButton(
                        pay_cash[data[str(user_id)]["lang"]], callback_data=f"-Cash{no}+{price}+{typpe}")
                    btn2 = types.InlineKeyboardButton(
                        pay_falcon[data[str(user_id)]["lang"]], callback_data=f"-Falcon{no}+{price}+{typpe}")
                    markup.add(btn, btn2)
                    cap = capp[data[str(user_id)]["lang"]].format(typpe, no, price)
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(call.message.chat.id, cap, reply_markup=markup)
                elif "-Cash" in call.data:
                    typ = call.data[5:]
                    Quantity = int(typ.split("+")[0])
                    ty = call.data.split("+")[-1]
                    price = typ.split("+")[1]
                    markup = types.InlineKeyboardMarkup()
                    btn = types.InlineKeyboardButton(
                        after_paid[data[str(user_id)]["lang"]], callback_data=f"-paid{Quantity}+{price}+{ty}")
                    markup.add(btn)
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    cap = payment_lang[data[str(user_id)]["lang"]] + "".join(payment_gateway)
                    bot.send_message(user_id, cap, reply_markup=markup)
                elif "-paid" in call.data:
                    typ = call.data[5:]
                    Quantity = int(typ.split("+")[0])
                    ty = call.data.split("+")[-1]
                    price = typ.split("+")[1]
                    cap = f"From :- {data[str(user_id)]['real_name']}   " \
                          f"\n Phone Number :- {data[str(user_id)]['phone_number']}  " \
                          f" \n Type         :- {ty}   " \
                          f" \n  Quantity      :- {Quantity}" \
                          f" \n Price        :- {price} "
                    mark = types.InlineKeyboardMarkup(row_width=2)
                    btn = types.InlineKeyboardButton(
                        "Real", callback_data=f"((Real_{user_id}")
                    btn2 = types.InlineKeyboardButton(
                        "Fake", callback_data=f"((Fake_{user_id}")
                    mark.add(btn, btn2)
                    bot.send_message(chat_id="-1001674209692", text=cap, reply_markup=mark)

                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(user_id, thank_you[data[str(user_id)]["lang"]].format("Delivery"))

                elif "-Falcon" in call.data:
                    typ = call.data[7:]
                    with open('coupon.json', 'r') as file:
                        coupon = json.load(file)
                    coinss = coupon[data[str(user_id)]["coupon_code"]]["coins"]
                    Quantity = int(typ.split("+")[0])
                    ty = call.data.split("+")[-1]
                    price = typ.split("+")[1]
                    sub = float(price) / 10
                    if coinss >= sub:
                        with open('coupon.json', 'w') as files:
                            coupon[data[str(user_id)]["coupon_code"]]["coins"] -= sub
                            json.dump(dict(coupon), files, indent=4)
                        cap = f"From :- {data[str(user_id)]['real_name']}   " \
                              f"\n Phone Number :- {data[str(user_id)]['phone_number']}  " \
                              f" \n Type         :- {ty}    " \
                              f" \n  Quantity      :- {Quantity}" \
                              f" \n Price        :- {price} "

                        bot.send_message(chat_id="-1001674209692", text=cap)
                        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                        bot.send_message(user_id, thank_you[data[str(user_id)]["lang"]].format("Delivery"))
                    else:
                        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                        markup = types.InlineKeyboardMarkup()
                        btn = types.InlineKeyboardButton(
                            pay_cash[data[str(user_id)]["lang"]], callback_data=f"-Cash{Quantity}+{price}+{ty}")
                        markup.add(btn)
                        bot.send_message(user_id, not_coins[data[str(user_id)]["lang"]], reply_markup=markup)

            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button = types.KeyboardButton(text=Send_Phone[data[str(user_id)]["lang"]], request_contact=True)
                keyboard.add(button)
                bot.send_message(call.message.chat.id, Please_Send_Phone[data[str(user_id)]["lang"]],
                                 reply_markup=keyboard)

        else:
            bot.send_message(user_id, register_first[data[str(user_id)]["lang"]])


@bot.message_handler(func=lambda message: True)
def name_input(message):
    text = message.text
    user_id = str(message.from_user.id)
    with open('users.json', 'r') as f:
        data = json.load(f)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text=Send_Phone[data[user_id]["lang"]], request_contact=True)
    keyboard.add(button)

    if user_id in data:
        if len(data[user_id]) < 3:
            if "09" in text or "251" in text :
                bot.send_message(message.chat.id,
                                 dont_write[data[user_id]["lang"]],
                                 reply_markup=keyboard)
                return
            if " " not in text or len(text) < 7:
                bot.send_message(message.chat.id, full_name[data[user_id]["lang"]], reply_markup=ReplyKeyboardRemove())
                return
            with open('users.json', 'w') as fz:
                data[str(message.from_user.id)]["real_name"] = text
                data[str(message.from_user.id)]["phone_number"] = None
                json.dump(dict(data), fz, indent=4)
            bot.send_message(message.chat.id, thanks_click[data[user_id]["lang"]].format(text),
                             reply_markup=keyboard)
        elif data[user_id]["phone_number"] is None:
            bot.send_message(message.chat.id, Please_Send_Phone[data[user_id]["lang"]],
                             reply_markup=keyboard)
            return



    else:
        with open('users.json', 'w') as fz:
            data[str(message.from_user.id)]["real_name"] = text
            data[str(message.from_user.id)]["phone_number"] = None
            json.dump(dict(data), fz, indent=4)
        bot.send_message(message.chat.id, thanks_click[data[user_id]["lang"]].format(text),
                         reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def phone_input(message):
    user_id = str(message.from_user.id)
    with open('users.json', 'r') as f:
        data = json.load(f)
        if user_id in data:
            phone_number = message.contact.phone_number
            # user_id = message.from_user.id
            with open('users.json', 'r') as file:
                data = json.load(file)
            uu = str(uuid.uuid4())[:6]
            with open('coupon.json', 'r') as file:
                coupon = json.load(file)
            with open('coupon.json', 'w') as files:
                coupon[uu] = {"id": str(message.from_user.id),
                              "count": 0,
                              "referred": [],
                              "coins": 0
                              }
                json.dump(dict(coupon), files, indent=4)

            with open('users.json', 'w') as files:
                username = message.from_user.username
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name if message.from_user.last_name else ""
                data[user_id]["first_name"] = first_name
                data[user_id]["last_name"] = last_name
                data[user_id]["username"] = username
                data[user_id]["phone_number"] = phone_number
                data[user_id]["coupon_code"] = uu
                data[user_id]["link"] = f"https://t.me/{bot.get_me().username}?start={uu}"

                json.dump(dict(data), files, indent=4)
            bot.send_message(
                message.chat.id, thanks_register[data[user_id]["lang"]], reply_markup=menu(user_id, data))
        else:
            bot.send_message(message.chat.id, register_first[data[user_id]["lang"]])


while True:
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        traceback.print_exc()
        time.sleep(3)
