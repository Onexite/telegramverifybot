# Telegram Verify/Auth Bot

### About The Project

- This project was created by onexite on January 20, 2024. The project enables you to perform verification/authorization via a Telegram bot.

### İnstallation

- Installation is quite simple, all you need to do is to place the files in the folder and run the following code in the command prompt within that folder:

 ```
pip install -r requirements.txt
```
### How to Install and Run?

- First, go to Telegram and create a bot for yourself via BotFather.
- Afterwards, send any message to the bot you've created.
- Then, to obtain the admin_chat_id data, visit the following address. Also, don't forget to get your token from BotFather!
- https://api.telegram.org/bot{YOUR_TOKEN}/getUpdates
- On this page, you will see the messages sent to your bot. Take the chat_id data from the JSON that appears, it will be something like "123456". Fill in the fields in **cred.py** correctly."
- That's it! Now, run server1.py and server2.py, and your bot will be ready to use!

### Commands

- **/verify : **Sends you a random verification token and redirects you to the site when clicked. After verification, redirects you to the accessible site.
- **/verifyban {chat_id} :** As the name suggests, it bans the usage of the```/verify code for the target {chat_id}.``` **{ONLY ADMINS}**
- **/tokens :** Displays the list of all valid or invalid tokens. **{ONLY ADMINS}**
- **/tokencancel {token_id} :** Used to cancel tokens listed in /tokens. {FORCE} ``` Usage: /tokencancel {token_id} ``` **{ONLY ADMINS}**

### Still Under Development.

```
To quickly report bugs and bugs
Discord: onexite
```

### İmages

![1](https://github.com/Onexite/telegramtokenverify/assets/120252342/5e3bb12c-16da-42d6-be39-d6f6c3d9c140)
![2](https://github.com/Onexite/telegramtokenverify/assets/120252342/f6e2a05c-41f4-4d25-84d0-2eef0e74cdd3)
![3](https://github.com/Onexite/telegramtokenverify/assets/120252342/6ad8c447-79b5-45a9-8b1f-17bfad872505)
![4](https://github.com/Onexite/telegramtokenverify/assets/120252342/b7906960-00a5-4a66-ac6c-2935c625cd7e)
![5](https://github.com/Onexite/telegramtokenverify/assets/120252342/de4501e2-26f2-4aa6-9040-a598ffa94cf3)
![6](https://github.com/Onexite/telegramtokenverify/assets/120252342/ef68bb92-23fe-42d5-88eb-d8fab00b928a)
![7](https://github.com/Onexite/telegramtokenverify/assets/120252342/d31040f4-4238-4050-aeff-ccfdfb58da98)
