TOKEN = '7671969883:AAElIjOGnNeYgNapLrivHImJFlPCNuYmMFQ'
FaucetPay_wallet = 'EQD14kgmngE0fNYVs7_9dw78V3rPhNt7_Ee-7X3ykDORQvMp'
Telegram_Channel = 'https://t.me/qqwweerrttqqyyyy'

# معرف حسابك
admin_user_id = 5475256932  # هذا هو معرفك

# دالة للتحقق إذا كان المستخدم هو المسؤول
def is_admin(user_id):
    return user_id == admin_user_id

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        bot.send_message(message.chat.id, "مرحبًا بك، أنت المسؤول!")
    else:
        bot.send_message(message.chat.id, "مرحبًا بك في البوت!")

# أي أوامر أو عمليات أخرى يجب أن تكون محصورة فقط للمسؤول
@bot.message_handler(commands=["custom_command"])
def custom_command(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "تم تنفيذ الأمر بنجاح!")
    else:
        bot.send_message(message.chat.id, "أنت غير مخول لتنفيذ هذا الأمر.")
