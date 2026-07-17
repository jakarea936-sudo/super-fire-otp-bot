import logging
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# ================== কনফিগারেশন ==================
TOKEN = "8879167674:AAFIA80mU16FmYelECnKxHvkuf7kknHq25c"

# তোমার প্রাইভেট চ্যাট আইডি এখানে বসাও
YOUR_CHAT_ID = 0  # পরিবর্তন করো

# OTP খুঁজে বের করার প্যাটার্ন
OTP_PATTERN = re.compile(r'\b(\d{4,8})\b')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def handle_message(update: Update, context: CallbackContext):
    message = update.message
    if not message or not message.text:
        return

    text = message.text
    otps = OTP_PATTERN.findall(text)

    if otps:
        for otp in otps:
            alert = f"""🔥 **SUPER FIRE OTP DETECTED!** 🔥

**OTP:** `{otp}`
**গ্রুপ:** {message.chat.title or 'Private Chat'}
**ইউজার:** {message.from_user.first_name}
**টাইম:** {message.date}"""

            try:
                await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=alert, parse_mode='Markdown')
                print(f"✅ OTP পাওয়া গেছে: {otp}")
            except Exception as e:
                print(f"Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 SUPER FIRE OTP BOT চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()