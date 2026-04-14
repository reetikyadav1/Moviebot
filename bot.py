import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# 🔑 Token (Render env variable se aayega)
BOT_TOKEN = os.getenv("8594561505:AAH4ax25E_FUHLpPTvcNu1-J8wpZGXn9VSE")

CHANNELS = [
    "@MarketEdgeLab",
    "@Multibillionares",
    "@handwritten_notes_11th_12th"
]

# 📱 APK link (Render pe file upload nahi hoti easily)
APK_LINK = "https://your-apk-link.com"

# 🎬 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome to Movie Bot!\n\n👇 Paste your movie name"
    )

# 🎥 Movie input
async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text

    if text.startswith("/"):
        return

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/MarketEdgeLab")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/Multibillionares")],
        [InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/handwritten_notes_11th_12th")],
        [InlineKeyboardButton("✅ Confirm Task", callback_data="check")]
    ]

    await update.message.reply_text(
        "📌 To watch movie, complete all tasks 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🔍 Check join
async def check_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    try:
        for channel in CHANNELS:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                await query.answer("❌ Join all channels first", show_alert=True)
                return

        # ✅ Success
        keyboard = [
            [InlineKeyboardButton("📥 Download App", url=APK_LINK)]
        ]

        await query.message.reply_text(
            "✅ Task completed!\n📱 Download your app 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await query.answer()

    except Exception as e:
        print("Error:", e)
        await query.answer("⚠️ Try again later", show_alert=True)

# 🚀 Run bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, movie))
app.add_handler(CallbackQueryHandler(check_task))

print("Bot is running... 🚀")
app.run_polling()