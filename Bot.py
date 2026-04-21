import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Envíame un link de YouTube, TikTok, Instagram o Facebook y te lo descargo 🎥')

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if not url.startswith("http"):
        await update.message.reply_text("Eso no es un link. Mándame una URL válida.")
        return

    msg = await update.message.reply_text("Descargando... ⏳")

    # Opciones para que funcione mejor con Instagram/TikTok
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4/best', # Prioriza mp4, si no, el mejor disponible
        'noplaylist': True, # No descarga playlists completas
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                await context.bot.edit_message_text("Enviando video...", chat_id=update.effective_chat.id, message_id=msg.message_id)
                await update.message.reply_video(video=open(file, 'rb'))
                os.remove(file)
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=msg.message_id)
                return
                
        await context.bot.edit_message_text("No pude encontrar el video descargado 😕", chat_id=update.effective_chat.id, message_id=msg.message_id)

    except Exception as e:
        await context.bot.edit_message_text(f"Error: No se pudo descargar.\nMotivo: {e}", chat_id=update.effective_chat.id, message_id=msg.message_id)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar))

app.run_polling()
