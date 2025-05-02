import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '7671969883:AAElIjOGnNeYgNapLrivHImJFlPCNuYmMFQ'
FaucetPay_wallet = 'EQD14kgmngE0fNYVs7_9dw78V3rPhNt7_Ee-7X3ykDORQvMp'
Telegram_Channel = 'https://t.me/qqwweerrttqqyyyy'
bot = telebot.TeleBot(TOKEN)

users = {}
questions = [
    {"q": f"ما هو السؤال رقم {i}؟", "options": [f"خيار أ{i}", f"خيار ب{i}", f"خيار ج{i}"], "answer": f"خيار ب{i}"}
    for i in range(1, 51)
]

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("ابدأ الاختبار"), KeyboardButton("رصيدي"))
    markup.add(KeyboardButton("مساعدة"), KeyboardButton("حول البوت"))
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"points": 0, "referrals": 0, "subscribed": False}
    bot.send_message(message.chat.id, "مرحبًا بك في بوت اختبار المعرفة!\nاختر أحد الأزرار للبدء.", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "ابدأ الاختبار")
def ask_question(message):
    user_id = message.from_user.id
    index = users[user_id].get("last_q", 0)

    # تحقق من الاشتراك في القناة
    if user_id not in users or not users[user_id].get("subscribed", False):
        bot.send_message(message.chat.id, "يرجى الاشتراك في القناة أولاً للاحتفاظ بإمكانية بدء الاختبار.",
                         reply_markup=ReplyKeyboardMarkup([["https://t.me/qqwweerrttqqyyyy"]]))
        return

    if index >= len(questions):
        bot.send_message(message.chat.id, "لقد أنهيت جميع الأسئلة! شكراً لمشاركتك.")
        return

    q = questions[index]
    options = "\n".join(q["options"])
    bot.send_message(message.chat.id, f"السؤال {index + 1}:\n{q['q']}\nالخيارات:\n{options}")
    users[user_id]["current_q"] = index
    users[user_id]["last_q"] = index + 1

@bot.message_handler(func=lambda m: m.text in sum([[q["answer"]] + q["options"] for q in questions], []))
def handle_answer(message):
    user_id = message.from_user.id
    q_index = users[user_id].get("current_q", 0)
    correct = questions[q_index]["answer"]
    
    if message.text == correct:
        users[user_id]["points"] += 10
        bot.send_message(message.chat.id, "إجابة صحيحة! +10 نقاط")
    else:
        bot.send_message(message.chat.id, f"إجابة خاطئة. الإجابة الصحيحة كانت: {correct}")
    
    ask_question(message)

@bot.message_handler(func=lambda m: m.text == "رصيدي")
def balance(message):
    user_id = message.from_user.id
    points = users.get(user_id, {}).get("points", 0)
    bot.send_message(message.chat.id, f"رصيدك الحالي: {points} نقطة")

@bot.message_handler(func=lambda m: m.text == "مساعدة")
def help_command(message):
    bot.send_message(message.chat.id, "استخدم الأزرار لبدء الاختبار، ومشاهدة رصيدك، والحصول على معلومات.")

@bot.message_handler(func=lambda m: m.text == "حول البوت")
def about_command(message):
    bot.send_message(message.chat.id, "هذا البوت مصمم لتقديم اختبارات معلوماتية ممتعة باللغة العربية.")

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "عذرًا، لم أفهم هذا الأمر. استخدم الأزرار المتاحة.", reply_markup=main_menu())

# تحقق من الاشتراك في القناة
@bot.message_handler(func=lambda message: True)
def check_subscription(message):
    user_id = message.from_user.id
    try:
        # التحقق من الاشتراك في القناة
        member = bot.get_chat_member('@qqwweerrttqqyyyy', user_id)
        if member.status == 'member' or member.status == 'administrator':
            users[user_id]["subscribed"] = True
        else:
            users[user_id]["subscribed"] = False
    except Exception as e:
        print(f"Error in subscription check: {e}")

bot.polling()
