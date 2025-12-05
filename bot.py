import os
import uuid
import shutil
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context):
    await update.message.reply_text("سلام داداش! بات ریک و مورتی فارسی آماده‌ست\nیه موضوع بفرست، برات ویدیوی خفن می‌سازم\n\nمثال: ریک و مورتی تو عید نوروز")

async def handle(update: Update, context):
    topic = update.message.text
    msg = await update.message.reply_text("در حال ساخت ویدیو… حدود ۸-۱۰ دقیقه صبر کن")
    folder = f"temp/{uuid.uuid4().hex[:8]}"
    os.makedirs(folder, exist_ok=True)
    try:
        os.system(f"python make_video.py \"{topic}\" {folder}")
        if os.path.exists(f"{folder}/final.mp4"):
            await update.message.reply_video(open(f"{folder}/final.mp4", "rb"), caption=topic)
            await msg.delete()
        else:
            await msg.edit_text("یه مشکلی شد، دوباره امتحان کن")
    except:
        await msg.edit_text("خطا داد")
    finally:
        shutil.rmtree(folder, ignore_errors=True)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
