import logging
import re
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler
from telegram.constants import ParseMode

# ⚠️ এগুলো সবসময় গোপন রাখবেন। 
TOKEN = "8862479708:AAG6jNfd_SKeBqA1Jq3BmL9mRlg0iOVQdTI"
YOUR_CHAT_ID = 7455109015

# ৪ থেকে ৮ ডিজিটের সংখ্যা খোঁজার জন্য রেগুলার এক্সপ্রেশন
OTP_PATTERN = re.compile(r'\b(\d{4,8})\b')
authorized_users = set()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: CallbackContext):
    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("🔗 Join Group 1"), KeyboardButton("🔗 Join Group 2")],
        [KeyboardButton("✅ Verify")],
        [KeyboardButton("📱 GET NUMBER"), KeyboardButton("📊 My Status")],
        [KeyboardButton("👨‍💼 Contact Admin")]
    ], resize_keyboard=True, persistent=True)

    await update.message.reply_text(
        "🔥 **SUPER FIRE OTP BOT** চালু হয়েছে। নিচের বাটনগুলো ব্যবহার করুন।", 
        reply_markup=keyboard, 
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    
    # বোতাম বা কিবোর্ডের কমান্ডগুলোর তালিকা
    menu_buttons = ["🔗 Join Group 1", "🔗 Join Group 2", "✅ Verify", "📱 GET NUMBER", "📊 My Status", "👨‍💼 Contact Admin"]

    # ১. বাটন ক্লিকের রেসপন্স হ্যান্ডলিং
    if text == "✅ Verify":
        authorized_users.add(user_id)
        await update.message.reply_text("✅ ভেরিফাই সফল! এখন OTP অ্যালার্ট পাবেন।")
        return  # কাজ শেষ, তাই এখানেই ফাংশন থামিয়ে দিচ্ছি

    elif text == "📊 My Status":
        state = "✅ ভেরিফাইড" if user_id in authorized_users else "❌ Verify করুন"
        await update.message.reply_text(f"📊 স্ট্যাটাস: {state}")
        return

    elif text == "📱 GET NUMBER":
        await update.message.reply_text("📱 সার্ভিস নির্বাচন করুন (Facebook, Instagram ইত্যাদি)।")
        return

    elif text == "👨‍💼 Contact Admin":
        await update.message.reply_text("👨‍💼 অ্যাডমিনের সাথে যোগাযোগ করুন।")
        return
        
    elif text in ["🔗 Join Group 1", "🔗 Join Group 2"]:
        await update.message.reply_text("🔗 গ্রুপে জয়েন করার লিংক পেতে অ্যাডমিনের সাথে যোগাযোগ করুন।")
        return

    # ২. ওটিপি ডিটেকশন লজিক (শুধুমাত্র সাধারণ টেক্সট মেসেজের জন্য)
    # মেসেজটি যদি উপরের কোনো বাটন না হয়, তবেই ওটিপি চেক করবে
    if text not in menu_buttons:
        if user_id not in authorized_users:
            # ইউজার ভেরিফাইড না থাকলে ওটিপি অ্যালার্ট পাঠাবে না
            return
            
        otps = OTP_PATTERN.findall(text)
        if otps:
            for otp in otps:
                alert = f"🔥 **FAST OTP DETECTED!** 🔥\n\n" \
                        f"**OTP:** `{otp}`\n" \
                        f"**গ্রুপ:** {update.message.chat.title or 'Private'}\n" \
                        f"**ইউজার:** {update.effective_user.first_name}\n" \
                        f"**টাইম:** {update.message.date.strftime('%Y-%m-%d %H:%M:%S')}"
                
                await context.bot.send_message(YOUR_CHAT_ID, alert, parse_mode=ParseMode.MARKDOWN)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # filters.TEXT & ~filters.COMMAND নিশ্চিত করে যে কোনো বটের কমান্ড (/start) এখানে আসবে না
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 SUPER FIRE OTP BOT চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
