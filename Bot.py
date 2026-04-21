import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Mándame un link de YouTube y te lo descargo 🎥')

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # Solo procesa si parece un link
    if not url.startswith("http"):
        await update.message.reply_text("Eso no es un link. Mándame una URL de YouTube.")
        return

    await update.message.reply_text("Descargando... ⏳")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4' # Para que no pese tanto
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir():
            if file.startswith("video"):
                await update.message.reply_video(video=open(file, 'rb'))
                os.remove(file)
                
    except Exception as e:
        await update.message.reply_text(f"Error al descargar: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, descargar))

app.run_polling()
