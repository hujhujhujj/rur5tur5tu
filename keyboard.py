from telebot import types

def main_keyboard():
	main_keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text="💫 Регистрация", callback_data="register")
	button2 = types.InlineKeyboardButton(text="👤 Профиль", callback_data="profile")
	button3 = types.InlineKeyboardButton(text="📊 Статистика", callback_data="statistics")
	main_keyboard.row(button1, button2)
	main_keyboard.row(button3)
	return main_keyboard

def p2p_deposit_keyboard(bill_id, url):
	deposit_keyboard = types.InlineKeyboardMarkup(row_width=2)
	deposit_keyboard.add(
	    types.InlineKeyboardButton(text='💸 Оплатить 💸', url=url))
	deposit_keyboard.add(
	    types.InlineKeyboardButton(text='🔁 Проверить платёж', callback_data=f'check_p2p_deposit:{bill_id}'),
	    types.InlineKeyboardButton(text='❌ Отменить', callback_data=f'reject_p2p_payment')
	    )
	return deposit_keyboard

def del_msg_keyboard():
	del_msg_keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text="❌ Закрыть", callback_data="delete_message")
	del_msg_keyboard.row(button1)
	return del_msg_keyboard

def worker_menu_keyboard():
	worker_menu_keyboard = types.InlineKeyboardMarkup(row_width=1)
	button1 = types.InlineKeyboardButton(text="🥝 Управление кошельком", callback_data="worker_qiwi_manipulate")
	button2 = types.InlineKeyboardButton(text="📨 Получить данные", callback_data="worker_get_data")
	button3 = types.InlineKeyboardButton(text="🦣 Добавить мамонта", callback_data="worker_add_mamont")
	button4 = types.InlineKeyboardButton(text="📧 Рассылка всем мамонтам", callback_data="worker_all_mamonts_mailing")
	button5 = types.InlineKeyboardButton(text="📚 Мануалы", callback_data="worker_manuals")
	button6 = types.InlineKeyboardButton(text="🔙 Выйти", callback_data="delete_message")

	worker_menu_keyboard.add(button1, button2, button3, button4, button5, button6)
	return worker_menu_keyboard

def back_to_main_keyboard():
	back_to_main_keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_main")
	back_to_main_keyboard.row(button1)
	return back_to_main_keyboard

def back_to_worker_keyboard():
	back_to_worker_keyboard = types.InlineKeyboardMarkup()
	button1 = types.InlineKeyboardButton(text="⏪ Назад", callback_data="worker_back_to_main")
	back_to_worker_keyboard.row(button1)
	return back_to_worker_keyboard

def data_keyboard(user_id):
	from functions import get_mamonts
	mamonts = get_mamonts(user_id)
	data_keyboard = types.InlineKeyboardMarkup(row_width=1)
	i = 1
	for mamont in mamonts:
		if i <= 10:
			data_keyboard.add(types.InlineKeyboardButton(text=f"🦣 {mamont[0]}", callback_data=f"worker_mamont:{mamont[0]}"))
		else:
			i += 1
	data_keyboard.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data="worker_back_to_main"))
	return data_keyboard

def back_to_data_keyboard(mamont_id):
	back_to_data_keyboard = types.InlineKeyboardMarkup(row_width=1)
	button1 = types.InlineKeyboardButton(text="✉️ Отправить сообщение", callback_data=f"worker_send_message:{mamont_id}")
	button2 = types.InlineKeyboardButton(text="⏪ Назад", callback_data="worker_get_data")
	back_to_data_keyboard.add(button1, button2)
	return back_to_data_keyboard

def qiwi_keyboard():
    qiwi_keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="✏️Обновить токен", callback_data="worker_update_token_qiwi")
    button2 = types.InlineKeyboardButton(text="📱Узнать номер", callback_data="worker_get_qiwi_number")
    button3 = types.InlineKeyboardButton(text="💰Узнать баланс", callback_data="worker_get_qiwi_balance")
    button4 = types.InlineKeyboardButton(text="➡️Сделать перевод", callback_data="worker_qiwi_output")
    qiwi_keyboard.row(button1)
    qiwi_keyboard.row(button2, button3)
    qiwi_keyboard.row(button4)
    qiwi_keyboard.add(types.InlineKeyboardButton(text="⏪ Назад", callback_data="worker_back_to_main"))
    return qiwi_keyboard

def admin_menu_keyboard():
	admin_menu_keyboard = types.InlineKeyboardMarkup(row_width=1)
	button1 = types.InlineKeyboardButton(text="🎗 Выдать доступ", callback_data="admin_give_access")
	button2 = types.InlineKeyboardButton(text="🎗 Забрать доступ", callback_data="admin_take_access")
	button3 = types.InlineKeyboardButton(text="🧑‍💻 Рассылка воркерам", callback_data="admin_worker_mailing")

	admin_menu_keyboard.row(button1, button2)
	admin_menu_keyboard.add(button3)
	return admin_menu_keyboard