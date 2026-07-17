import logging
import re
import asyncio
import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.constants import ParseMode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 📢 ভেরিফাইড ইউজারদের ডাটাবেজ ট্র্যাক রাখার জন্য সেট
authorized_users = set()

# 🔐 রেলওয়ের Variables থেকে টোকেন এবং চ্যাট আইডি সংগ্রহ (কোড এখন সম্পূর্ণ ফ্রেশ ও নিরাপদ)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
YOUR_CHAT_ID = int(os.environ.get("YOUR_CHAT_ID", "7455109015"))
API_KEY = "MURAD_F455C219DCF80BC50E1E696E"

if not BOT_TOKEN:
    raise ValueError("ERROR: BOT_TOKEN is missing in Railway Variables!")

# টেলিগ্রাম এবং FastAPI ইনিশিয়ালাইজেশন
app_telegram = Application.builder().token(BOT_TOKEN).build()
app_fastapi = FastAPI()

# প্যানেল থেকে আসা ওটিপি ডেটা ফরম্যাট করার মডেল
class OTPPayload(BaseModel):
    otp: str
    service: str = "Unknown"
    phone_number: str = "Unknown"

# মেইন কিবোর্ড মেনু
def get_main_menu_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🎲 GET NUMBER"), KeyboardButton("🔐 2FA CODE")]
    ], resize_keyboard=True, persistent=True)

# আনভেরিফাইড ইউজারদের জন্য চ্যানেল জয়েন কিবোর্ড
def get_join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Join 1", url="https://t.me/EASY_MARKETING1")],
        [InlineKeyboardButton("📢 Join Join 2", url="https://t.me/EASY_METHOD1")],
        [InlineKeyboardButton("✅ Verify", callback_data="verify_user")]
    ])

# সার্ভিস কিবোর্ড মেনু
def get_services_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📘 Facebook", callback_data="service_fb")],
        [InlineKeyboardButton("📸 Instagram", callback_data="service_ig")],
        [InlineKeyboardButton("🔄 Refresh Services", callback_data="refresh_services")],
        [InlineKeyboardButton("🔙 Back Main Menu", callback_data="back_main")]
    ])

# --- টেলিগ্রাম বট লজিক ---

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in authorized_users:
        await update.message.reply_text(
            "✨ Welcome Easy marketing support! ✨\n💰 Balance: 0.0 BDT",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        welcome_text = "🔒 **বট ব্যবহার করার আগে নিচের চ্যানেলগুলোতে জয়েন করুন!**\n\nচ্যানেলে জয়েন করার পর **✅ Verify** বাটনে চাপ দিন।"
        await update.message.reply_text(welcome_text, reply_markup=get_join_keyboard(), parse_mode=ParseMode.MARKDOWN)

async def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if query.data == "verify_user":
        authorized_users.add(user_id)
        await query.message.delete()
        await context.bot.send_message(
            chat_id=user_id,
            text="✨ Welcome Easy marketing support! ✨\n💰 Balance: 0.0 BDT",
            reply_markup=get_main_menu_keyboard()
        )
    elif query.data == "service_fb":
        await query.message.edit_text("আপনি **Facebook** সার্ভিসটি সিলেক্ট করেছেন। ওটিপি-র জন্য অপেক্ষা করুন...", reply_markup=get_services_keyboard())
    elif query.data == "service_ig":
        await query.message.edit_text("আপনি **Instagram** সার্ভিসটি সিলেক্ট করেছেন। ওটিপি-র জন্য অপেক্ষা করুন...", reply_markup=get_services_keyboard())
    elif query.data == "refresh_services":
        await query.message.edit_text("🔄 সার্ভিস লিস্ট রিফ্রেশ করা হয়েছে।\n\n🔍 Select Service:", reply_markup=get_services_keyboard())
    elif query.data == "back_main":
        await query.message.delete()
        await context.bot.send_message(chat_id=user_id, text="🏠 আপনি মেইন মেনুতে ফিরে এসেছেন।", reply_markup=get_main_menu_keyboard())

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    user_id = update.effective_user.id

    if user_id not in authorized_users:
        await update.message.reply_text("🔒 **বট ব্যবহার করার আগে নিচের চ্যানেলগুলোতে জয়েন করুন!**", reply_markup=get_join_keyboard())
        return

    if text == "🎲 GET NUMBER":
        await update.message.reply_text("🔍 Select Service:", reply_markup=get_services_keyboard())
    elif text == "🔐 2FA CODE":
        await update.message.reply_text("🔐 আপনার টু-ফ্যাক্টর (2FA) কোডটি এখানে দিন বা জেনারেট করুন।")

# --- ⚡ ওয়েব হুক এবং ওটিপি এন্ডপয়েন্ট (FastAPI) ---

@app_fastapi.post("/fastx-webhook")
async def receive_telegram_update(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, app_telegram.bot)
        asyncio.create_task(app_telegram.application.process_update(update))
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Webhook Error: {e}")
        return {"status": "error", "details": str(e)}

@app_fastapi.post("/instant-otp")
async def receive_instant_otp(payload: OTPPayload):
    otp = payload.otp
    service = payload.service
    phone = payload.phone_number

    alert = f"""🔥 **FAST OTP DETECTED! (Instant Webhook)** 🔥

**OTP:** `{otp}`
**সার্ভিস:** {service}
**নাম্বার:** `{phone}`
**স্ট্যাটাস:** ⚡ Real-time Delivery"""

    try:
        await app_telegram.bot.send_message(
            chat_id=YOUR_CHAT_ID,
            text=alert,
            parse_mode=ParseMode.MARKDOWN
        )
        return {"status": "success", "message": "OTP sent!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app_fastapi.on_event("startup")
async def startup_event():
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CallbackQueryHandler(handle_callback))
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    await app_telegram.initialize()
    await app_telegram.start()
    logging.info("🚀 বট এবং এপিআই সফলভাবে সংযুক্ত হয়েছে...")

@app_fastapi.on_event("shutdown")
async def shutdown_event():
    await app_telegram.stop()
    await app_telegram.shutdown()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("bot:app_fastapi", host="0.0.0.0", port=port, reload=False)
