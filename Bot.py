from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PRIVATE_GROUP_LINK = os.environ.get("GROUP_LINK")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=os.environ.get("QR_IMAGE_URL"),
        caption=(
            "🎯 *Monthly Prize Group*\n\n"
            "💰 Neeche QR se payment karo\n"
            "📸 Payment ka screenshot yahan bhejo\n\n"
            "✅ Verification ke baad group link milega!"
        ),
        parse_mode="Markdown"
    )

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    name = user.full_name
    username = f"@{user.username}" if user.username else "No username"
    uid = user.id

    await context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 New Screenshot!\n👤 {name}\n🔗 {username}\n🆔 {uid}\n\nApprove karne ke liye:\n/approve {uid}"
    )
    await update.message.reply_text("✅ Screenshot mil gaya! Thodi der mein link bheja jayega.")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    try:
        user_id = int(context.args[0])
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🎉 *Payment Verified!*\n\nGroup join karo:\n{PRIVATE_GROUP_LINK}",
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ Link bhej diya!")
    except:
        await update.message.reply_text("❌ Error! Format: /approve 123456789")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("approve", approve))
app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
app.run_polling()
