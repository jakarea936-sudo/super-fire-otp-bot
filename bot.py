import logging
import re
from telegram import Update, BotCommand
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler

# ================== কনফিগারেশন ==================
TOKEN = "8862479708:AAG6jNfd_SKeBqA1Jq3BmL9mRlg0iOVQdTI"
YOUR_CHAT_ID = 7455109015

OTP_PATTERN = re.compile(r'\b(\d{4,8})\b')
is_active = True

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                   level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🔥 **Welcome to SUPER FAST OTP Fetcher Bot!**\n\n"
        "আমি গ্রুপ/চ্যাট থেকে OTP অটো ডিটেক্ট করে তোমাকে অ্যালার্ট পাঠাব।\n"
        "কমান্ড:\n"
        "/status - বটের স্ট্যাটাস দেখো\n"
        "/on - বট চালু করো\n"
        "/off - বট বন্ধ করো",
        parse_mode='Markdown'
    )

async def status(update: Update, context: CallbackContext):
    state = "🟢 **চালু আছে**" if is_active else "🔴 **বন্ধ আছে**"
    await update.message.reply_text(f"**বট স্ট্যাটাস:** {state}\nChat ID: {YOUR_CHAT_ID}")

async def turn_on(update: Update, context: CallbackContext):
    global is_active
    is_active = True
    await update.message.reply_text("✅ বট চালু হয়েছে। এখন OTP ডিটেক্ট করবে।")

async def turn_off(update: Update, context: CallbackContext):
    global is_active
    is_active = False
    await update.message.reply_text("⛔ বট বন্ধ হয়েছে।")

async def handle_message(update: Update, context: CallbackContext):
    global is_active
    if not is_active:
        return

    message = update.message
    if not message or not message.text:
        return

    text = message.text
    otps = OTP_PATTERN.findall(text)

    if otps:
        for otp in otps:
            alert = f"""🔥 **FAST OTP DETECTED!** 🔥

**OTP:** `{otp}`
**গ্রুপ:** {message.chat.title or 'Private Chat'}
**ইউজার:** {message.from_user.first_name}
**টাইম:** {message.date}"""

            try:
                await context.bot.send_message(chat_id=YOUR_CHAT_ID, 
                                             text=alert, 
                                             parse_mode='Markdown')
                print(f"✅ OTP পাওয়া গেছে: {otp}")
            except Exception as e:
                print(f"Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("on", turn_on))
    app.add_handler(CommandHandler("off", turn_off))
    
    # OTP Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 SUPER FAST OTP FETCHER BOT চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
