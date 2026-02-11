import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "8348501409:AAH1o_RGSNqTD1GxL2o2sejI-rboFkfs_6E"
ADMIN_ID = 6158629398


# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    text = f"""
👋 <b>Assalomu alaykum!</b>

🤝 <b>{user.full_name}</b>, sizga hush kelibsiz!

📡 Ushbu bot orqali <b>Safarova_Nasiba_👩‍💻</b> bilan bevosita bog‘lanishingiz mumkin.

💬 Xabar, rasm, video yoki ovozli xabar yuboring — admin ko‘radi va javob beradi.

⏰ <i>Javob odatda 24 soat ichida beriladi.</i>
"""

    await update.message.reply_text(text, parse_mode="HTML")


# ===== FOYDALANUVCHI XABARINI ADMINGA YUBORISH =====
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user

    if user.id == ADMIN_ID:
        return

    text_info = f"""
👤 <b>Foydalanuvchi:</b> {user.full_name}
🆔 <code>{user.id}</code>
━━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✉️ Javob yozish", callback_data=f"reply_{user.id}")]
    ])

    try:
        if message.text:
            await context.bot.send_message(
                ADMIN_ID,
                f"📩 <b>Yangi matn xabar:</b>\n\n{text_info}\n💬 {message.text}",
                parse_mode="HTML",
                reply_markup=keyboard
            )

        elif message.photo:
            await context.bot.send_photo(
                ADMIN_ID,
                message.photo[-1].file_id,
                caption=f"🖼 <b>Rasm yuborildi!</b>\n\n{text_info}",
                parse_mode="HTML",
                reply_markup=keyboard
            )

        elif message.video:
            await context.bot.send_video(
                ADMIN_ID,
                message.video.file_id,
                caption=f"🎬 <b>Video yuborildi!</b>\n\n{text_info}",
                parse_mode="HTML",
                reply_markup=keyboard
            )

        elif message.voice:
            await context.bot.send_voice(
                ADMIN_ID,
                message.voice.file_id,
                caption=f"🎙 <b>Ovozli xabar!</b>\n\n{text_info}",
                parse_mode="HTML",
                reply_markup=keyboard
            )

        elif message.audio:
            await context.bot.send_audio(
                ADMIN_ID,
                message.audio.file_id,
                caption=f"🎧 <b>Audio yuborildi!</b>\n\n{text_info}",
                parse_mode="HTML",
                reply_markup=keyboard
            )

        elif message.sticker:
            await context.bot.send_sticker(ADMIN_ID, message.sticker.file_id)

            await context.bot.send_message(
                ADMIN_ID,
                f"💠 <b>Stiker yuborildi!</b>\n\n{text_info}",
                parse_mode="HTML",
                reply_markup=keyboard
            )

        else:
            await message.reply_text("❗ Ushbu fayl turi qo‘llab-quvvatlanmaydi.")
            return

        await message.reply_text(
            "✅ Xabaringiz Safarova_Nasiba_👩‍💻 yuborildi!\n🕐 Yana savol yozishingiz mumkin."
        )

    except Exception as e:
        print("Xato:", e)


# ===== ADMIN TUGMANI BOSGANI =====
async def reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = int(query.data.split("_")[1])

    context.user_data["target_user"] = user_id

    await query.message.reply_text(
        f"✍️ <b>Javob yozing yoki ovozli xabar yuboring.</b>\n🎯 ID: <code>{user_id}</code>",
        parse_mode="HTML"
    )


# ===== ADMIN JAVOBINI FOYDALANUVCHIGA YUBORISH =====
async def send_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    user_id = context.user_data.get("target_user")

    if not user_id:
        await message.reply_text("⚠️ Avval foydalanuvchini tanlang!")
        return

    try:
        if message.text:
            await context.bot.send_message(
                user_id,
                f"📨 <b>Safarova_Nasiba_👩‍💻 javobi:</b>\n\n{message.text}",
                parse_mode="HTML"
            )

        elif message.voice:
            await context.bot.send_voice(
                user_id,
                message.voice.file_id,
                caption="🎧 Admin javobi (ovozli xabar)"
            )

        elif message.audio:
            await context.bot.send_audio(
                user_id,
                message.audio.file_id,
                caption="🎵 Admin audio javobi"
            )

        elif message.photo:
            await context.bot.send_photo(
                user_id,
                message.photo[-1].file_id,
                caption="🖼 Admin rasm yubordi"
            )

        elif message.video:
            await context.bot.send_video(
                user_id,
                message.video.file_id,
                caption="🎬 Admin video javobi"
            )

        else:
            await message.reply_text("❗ Ushbu turdagi faylni yuborib bo‘lmaydi.")
            return

        await message.reply_text("✅ Javob foydalanuvchiga yuborildi.")

        # 🔥 Javob rejimini yopamiz
        context.user_data.clear()

    except Exception as e:
        await message.reply_text(f"❌ Xato: {e}")


# ===== BARCHA XABARLARNI BOSHQARUVCHI ROUTER =====
async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # 👉 Agar admin javob rejimida bo‘lsa
    if user.id == ADMIN_ID and context.user_data.get("target_user"):
        await send_reply(update, context)
    else:
        await forward_to_admin(update, context)


# ===== MAIN =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(reply_button, pattern="^reply_"))

    # 🔥 ENG MUHIM — bitta universal handler
    app.add_handler(MessageHandler(
        filters.ALL & ~filters.COMMAND,
        message_router
    ))

    print("🤖 Bot ishga tushdi — python-telegram-bot versiya")

    app.run_polling()


if __name__ == "__main__":
    main()
