# --------------------------------
# |                              |
# |      copyright onexite       |
# |     Developed by onexite     |
# |      Discord : onexite       |
# |                              |
# --------------------------------

import random
import string
import requests
from telegram.ext import Updater, CommandHandler
import mysql.connector
from datetime import datetime, timedelta, timezone
from tabulate import tabulate
import time
from cred import get_admin_chat_id, get_token,get_mysqli_host,get_mysqli_name,get_mysqli_pass,get_mysqli_dbname,get_serverip,get_mysqli_host2


TOKEN = get_token()

def generate_random_token(length=132):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def send_token_to_server2(token, chat_id):
    server2_url = f"http://{get_serverip()}/authorize/{token}?chat_id={chat_id}"
    response = requests.post(server2_url)
    return response.text

def verifyban(update, context):
    chat_id = update.message.chat_id
    args = context.args
    if not args:
        if str(chat_id) == get_admin_chat_id():
            update.message.reply_text("Lütfen engellemek istediğiniz kullanıcının chat ID'sini belirtin. Örneğin: /verifyban 1234567")
        return
    banned_user_id = args[0]

    context.user_data['banned_users'] = context.user_data.get('banned_users', [])
    context.user_data['banned_users'].append(banned_user_id)

    update.message.reply_text(f"Chat ID {banned_user_id} artık /verify komutunu kullanamayacak.")

def verify(update, context):
    current_time = time.time()
    last_verification_time = context.user_data.get('last_verification_time', 0)

    if current_time - last_verification_time < 60:
        update.message.reply_text("Bir dakika içinde tekrar /verify komutunu kullanamazsınız!")
        return
    chat_id = update.message.chat_id

    banned_users = context.user_data.get('banned_users', [])
    if str(chat_id) in banned_users:
        update.message.reply_text("Bu kullanıcı /verify komutunu kullanamaz.")
        return

    token = generate_random_token()
    website_link = f"http://{get_serverip()}/verification?token={token}&chat_id={chat_id}"
    send_token_to_server2(token, chat_id)
    update.message.reply_text(f"Doğrulama Talebi Oluşturuldu, Linke Tıklayınız: {website_link}")

    context.user_data['last_verification_time'] = current_time




def is_token_valid(expiry):
    current_time = datetime.now()
    return expiry > current_time

def tokenadmin(update, context):
    chat_id = update.message.chat_id
    if str(chat_id) == get_admin_chat_id():
        conn = mysql.connector.connect(
            host=get_mysqli_host(),
            user=get_mysqli_name(),
            password=get_mysqli_pass(),
            database=get_mysqli_dbname()
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, token, expiry FROM authorized_token")
        tokens = cursor.fetchall()
        conn.close()

        if tokens:
            token_list = []
            for token in tokens:
                token_id, token_str, expiry = token
                validity = "Geçerli ✅" if is_token_valid(expiry) else "Süresi Dolmuş ❌"
                token_info = f"ID: {token_id}, Token: {token_str}, Geçerlilik Tarihi: {expiry}, Durum: {validity}"
                token_list.append(token_info)

            token_text = "\n".join(token_list)
            update.message.reply_text("Tokenler:\n" + token_text)
        else:
            update.message.reply_text("Veritabanında hiç token bulunamadı.")
    else:
        update.message.reply_text("Bu işlemi gerçekleştirmek için yetkiniz bulunmamaktadır.")
        

def send_telegram_message(TOKEN, chat_id, message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=data)

def cancel_token(update, context):
    # Komutun argümanlarını ayıkla
    chat_id = update.message.chat_id
    admin_chat_id = get_admin_chat_id()
    adminmessage1 = "❌ [ADMİN] Yetkisiz Erişim "
    
    if str(chat_id) != get_admin_chat_id():
        update.message.reply_text("Bu işlemi gerçekleştirmek için yetkiniz bulunmamaktadır.")
        send_telegram_message(TOKEN, admin_chat_id, adminmessage1)
        return

    args = context.args
    if not args:
        update.message.reply_text("Lütfen silmek istediğiniz tokenin ID'sini belirtin. Örneğin: /tokencancel 1")
        return

    token_id = args[0]

    conn = mysql.connector.connect(
        host=get_mysqli_host(),
        user=get_mysqli_name(),
        password=get_mysqli_pass(),
        database=get_mysqli_dbname()
    )
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM authorized_token WHERE id = %s", (token_id,))
        conn.commit()
        update.message.reply_text(f"Token ID {token_id} başarıyla silindi.")
    except mysql.connector.Error as err:
        update.message.reply_text(f"Token ID {token_id} silinirken bir hata oluştu: {err}")
    finally:
        cursor.close()
        conn.close()

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("verify", verify))
    dp.add_handler(CommandHandler("tokens", tokenadmin))
    dp.add_handler(CommandHandler("tokencancel", cancel_token))
    dp.add_handler(CommandHandler("verifyban", verifyban))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

# --------------------------------
# |                              |
# |      copyright onexite       |
# |     Developed by onexite     |
# |      Discord : onexite       |
# |                              |
# --------------------------------
