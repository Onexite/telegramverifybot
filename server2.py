# --------------------------------
# |                              |
# |      copyright onexite       |
# |     Developed by onexite     |
# |      Discord : onexite       |
# |                              |
# --------------------------------

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime, timedelta, timezone
import os
from cred import get_admin_chat_id, get_token,get_mysqli_host,get_mysqli_name,get_mysqli_pass,get_mysqli_dbname,get_mysqli_host2
import time

# Zaman dilimini ayarla (örneğin Türkiye saati)
os.environ['TZ'] = 'Europe/Istanbul'

turkey_timezone = timezone(timedelta(hours=3))
turkey_time = datetime.now(turkey_timezone)
current_time = datetime.now(turkey_timezone)

print("Türkiye Saati:", turkey_time)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{get_mysqli_name()}:{get_mysqli_pass()}@{get_mysqli_host2()}/{get_mysqli_dbname()}"
db = SQLAlchemy(app)

class AuthorizedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(400), unique=True, nullable=False)
    chat_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(turkey_timezone))   
    expiry = db.Column(db.DateTime, nullable=True)
    
@app.before_request
def set_timezone():
    if not hasattr(request, 'turkey_time'):
        request.turkey_time = datetime.now(turkey_timezone)

def is_token_valid(authorized_token):
    expiration_time = authorized_token.expiry
    if expiration_time is None or expiration_time < datetime.now(turkey_timezone).replace(tzinfo=None):
        return False
    else:
        return True

    
def update_token_expiry(authorized_token):
    new_expiry = datetime.now(turkey_timezone) + timedelta(minutes=5)
    authorized_token.expiry = new_expiry
    db.session.commit()

@app.route('/verification', methods=['GET'])
def verification_page():
    token = request.args.get('token', '')
    chat_id1 = request.args.get('chat_id', "")
    
    authorized_token = AuthorizedToken.query.filter_by(token=token).first()

    if authorized_token and authorized_token.chat_id == int(chat_id1) and is_token_valid(authorized_token):
        user_agent = request.headers.get('User-Agent')
        ip_address = request.remote_addr

        bot_token = get_token()
        chat_id = chat_id1
        admin_chat_id = get_admin_chat_id()
        current_time = datetime.now(turkey_timezone)
        expiration_time = authorized_token.timestamp + timedelta(minutes=5)

        message = f"✅ Token Erişimi \n\nTarayıcı Bilgileri:\n\nUser-Agent: {user_agent}\n\nIP Adresi: {ip_address}\n\nSaat: {current_time.strftime('%H:%M:%S')}"
        message1 = f"✅ Oturum Süreniz | {expiration_time.strftime('%H:%M')} süresine kadar"
        adminmessage = f"❗️ ✅ [ADMIN] Token kullanımı! \n\nTarayıcı Bilgileri:\n\nUser-Agent: {user_agent}\n\nIP Adresi: {ip_address} \nChat ID : {chat_id1} \n\nSaat: {current_time.strftime('%H:%M:%S')} \n\nİlgili token : {token} "
        send_telegram_message(bot_token, chat_id, message)
        send_telegram_message(bot_token, chat_id, message1)
        send_telegram_message(bot_token, admin_chat_id, adminmessage)
        return render_template('verification.html', token=token, chat_id=chat_id1)
    
    user_agent = request.headers.get('User-Agent')
    ip_address = request.remote_addr
    bot_token = get_token()
    admin_chat_id = get_admin_chat_id()
    current_time = datetime.now(turkey_timezone)
    
    if authorized_token:
        expiration_time = authorized_token.timestamp + timedelta(minutes=5)
        adminmessage1 = f"❗️ ❌ [ADMIN] Token kullanımı! (GEÇERSİZ) \n\nTarayıcı Bilgileri:\n\nUser-Agent: {user_agent}\n\nIP Adresi: {ip_address} \nChat ID : {chat_id1} \n\nSaat: {current_time.strftime('%H:%M:%S')}\n\nİlgili token :\n{token} "
    else:
        adminmessage1 = f"❗️ ❌ [ADMIN] Token kullanımı! (GEÇERSİZ) \n\nTarayıcı Bilgileri:\n\nUser-Agent: {user_agent}\n\nIP Adresi: {ip_address} \nChat ID : {chat_id1} \n\nSaat: {current_time.strftime('%H:%M:%S')}\n\nToken bulunamadı."
    
    send_telegram_message(bot_token, admin_chat_id, adminmessage1)
    return render_template('veriification.html', token=token)

@app.route('/authorize/<token>', methods=['POST'])
def authorize(token):
    chat_id = request.args.get('chat_id', "")
    
    existing_token = AuthorizedToken.query.filter_by(token=token).first()

    if not existing_token or not is_token_valid(existing_token):
        new_token = AuthorizedToken(token=token, chat_id=chat_id)
        db.session.add(new_token)
        db.session.commit()
        update_token_expiry(new_token)
        return "Token başarıyla doğrulandı!"
    else:
        return "Token zaten doğrulanmış veya geçerliliği devam ediyor!"

def send_telegram_message(bot_token, chat_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(host='0.0.0.0', port=80, debug=True)

# --------------------------------
# |                              |
# |      copyright onexite       |
# |     Developed by onexite     |
# |      Discord : onexite       |
# |                              |
# --------------------------------
