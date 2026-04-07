from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os
TOKEN = os.getenv("TOKEN")
GROUP_ID = [-1003531096595]

import asyncio

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setlive", setlive))
    app.add_handler(CommandHandler("live", live))
    app.add_handler(CommandHandler("broadcast", broadcast))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())


users = set()
LIVE_LINK = "Belum ada live hari ini"

# START → simpan user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.message.chat_id)
    await update.message.reply_text(
        "Hi sayang 🤍\nKamu sudah join notif live!\nNanti aku kasih tau kalau kita live ya 🔥"
    )

# SET LIVE → update link
async def setlive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global LIVE_LINK
    LIVE_LINK = " ".join(context.args)

    await update.message.reply_text("✅ Link live hari ini sudah diupdate!")

# LIVE → user cek sendiri
async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🔥 LIVE HARI INI 🔥\n\n{LIVE_LINK}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.chat_id)

# BROADCAST → kirim ke semua user
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pisahkan link
    links = LIVE_LINK.split()

    tiktok = links[0] if len(links) > 0 else ""
    facebook = links[1] if len(links) > 1 else ""

    # Message
    msg = (
        "BAGS LIVE ✨\n\n"
        "💸 Shipping Fees\n"
        "• Non-branded items: $7 per parcel\n"
        "• Branded items: $10 per parcel 💼\n\n"
        "⚠️ Preorder system\n"
        "Some items may be unavailable at times.\n\n"
        "🔥 JOIN LIVE RIGHT NOW"
    )

    # Tombol klik
    keyboard = [
        [InlineKeyboardButton("🎥 TikTok Live", url=tiktok)],
        [InlineKeyboardButton("📘 Facebook Live", url=facebook)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # kirim ke user
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user,
                text=msg,
                reply_markup=reply_markup
            )
        except:
            pass

    # kirim ke semua grup
    for group in GROUP_ID:
        try:
            await context.bot.send_message(
                chat_id=group,
                text=msg,
                reply_markup=reply_markup
            )
        except:
            pass

    await update.message.reply_text("✅ Broadcast terkirim ke semua user & grup!")

# RUN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setlive", setlive))
app.add_handler(CommandHandler("live", live))
app.add_handler(CommandHandler("broadcast", broadcast))

app.run_polling()
