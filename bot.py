import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

# ==================== تنظیمات اصلی ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔥 توکن ربات از متغیر محیطی Railway
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8223115597:AAHI8LQIaY9Tw_Vuc1sIqljESuv3In0dlYo")

# 🔥 آیدی شما
ADMIN_ID = 6362322187
ADMIN_USERNAME = "@stevenmacmin"

# 🔥 آیدی کانال‌های شما (مقادیر پیش‌فرض)
TRAANFILM_CHANNEL_ID = int(os.environ.get("TRAANFILM_CHANNEL_ID", -1003652247811))
TRAANHUB_CHANNEL_ID = int(os.environ.get("TRAANHUB_CHANNEL_ID", -1003486802784))
STORAGE_CHANNEL_ID = int(os.environ.get("STORAGE_CHANNEL_ID", -1003592864027))

# ==================== ساختار فیلم‌ها ====================
FILMS = {
    "test": {
        "title": "🎬 فیلم تست ربات",
        "description": "این یک فیلم تست است",
        "file_id": None,
        "caption": "کیفیت: 720p | صدا: فارسی | مدت: 5 دقیقه"
    }
}

# ==================== توابع اصلی ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start"""
    user = update.effective_user
    
    logger.info(f"کاربر start از {user.id} ({user.first_name})")
    
    # اگر لینک فیلم زده
    if context.args and context.args[0] in FILMS:
        film_key = context.args[0]
        film = FILMS[film_key]
        
        # بررسی عضویت در کانال‌ها
        from telegram import Bot
        bot = Bot(token=BOT_TOKEN)
        missing_channels = []
        
        # بررسی عضویت در traanfilm
        try:
            member = await bot.get_chat_member(TRAANFILM_CHANNEL_ID, user.id)
            if member.status in ['left', 'kicked']:
                missing_channels.append("@traanfilm")
        except Exception as e:
            logger.error(f"خطا در بررسی traanfilm: {e}")
            missing_channels.append("@traanfilm")
        
        # بررسی عضویت در traanhub
        try:
            member = await bot.get_chat_member(TRAANHUB_CHANNEL_ID, user.id)
            if member.status in ['left', 'kicked']:
                missing_channels.append("@traanhub")
        except Exception as e:
            logger.error(f"خطا در بررسی traanhub: {e}")
            missing_channels.append("@traanhub")
        
        if missing_channels:
            await update.message.reply_text(
                f"⚠ لطفا اول در کانال‌ها عضو شوید:\n" + "\n".join(missing_channels)
            )
            return
        
        # ارسال فیلم اگر تنظیم شده
        if film["file_id"]:
            await update.message.reply_text(
                f"✅ فیلم تست:\n{film['title']}\n\nدر حال ارسال..."
            )
            
            try:
                await update.message.reply_video(
                    video=film["file_id"],
                    caption=film["caption"]
                )
            except Exception as e:
                await update.message.reply_text(
                    f"❌ خطا در ارسال فیلم: {str(e)}\n\n"
                    f"لطفا دوباره تنظیم کنید: /setfilm {film_key} FILE_ID"
                )
        else:
            await update.message.reply_text(
                f"❌ این فیلم هنوز تنظیم نشده\n"
                f"لطفا به ادمین اطلاع دهید: {ADMIN_USERNAME}"
            )
        return
    
    # پیام خوش‌آمدگویی
    welcome = f"""
🤖 **ربات ترن فیلم فعال شد!**

سلام {user.first_name} 👋

✅ **وضعیت میزبانی:** Railway
✅ **ربات آنلاین:** بله
✅ **توکن ربات:** صحیح

🎯 **مراحل بعدی:**
1. با /setfilm فیلم‌ها را تنظیم کنید
2. لینک بسازید: https://t.me/TraanFilmBot?start=test

🔧 **دستورات تست:**
/test - بررسی وضعیت
/setup - راهنمای تنظیم
/help - راهنمای کامل

👑 **ادمین:** {ADMIN_USERNAME}
🆔 **آیدی شما:** `{user.id}`
"""
    
    await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تست ربات"""
    try:
        from telegram import Bot
        import telegram
        
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        
        await update.message.reply_text(
            f"✅ **تست موفق!**\n\n"
            f"🤖 ربات: @{me.username}\n"
            f"📛 نام: {me.first_name}\n"
            f"🆔 آیدی: {me.id}\n"
            f"📦 کتابخانه: {telegram.__version__}\n"
            f"🚀 میزبان: Railway\n"
            f"✅ **وضعیت:** آنلاین\n\n"
            f"🎬 حالا می‌توانید ربات کامل را راه‌اندازی کنید."
        )
    except Exception as e:
        await update.message.reply_text(f"❌ خطا در تست: {str(e)}")

async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """راهنمای تنظیمات"""
    guide = """
🔧 **مراحل کامل راه‌اندازی ربات در Railway:**

🎯 **مرحله ۱: ساخت کانال‌ها در تلگرام**
1. @traanfilm - کانال فیلم‌ها (عمومی)
2. @traanhub - کانال اصلی (عمومی)
3. @TraanFilmStorage - ذخیره فیلم‌ها (خصوصی)

🎯 **مرحله ۲: دریافت آیدی عددی**
1. به @userinfobot بروید -> آیدی خودتان
2. ربات را به کانال‌ها ادمین کنید
3. از @getidsbot یا @my_id_bot آیدی کانال بگیرید

🎯 **مرحله ۳: تنظیم Railway Variables**
1. در Railway به بخش Variables بروید
2. این متغیرها را اضافه کنید:
   - BOT_TOKEN: توکن ربات شما
   - TRAANFILM_CHANNEL_ID: آیدی عددی کانال @traanfilm
   - TRAANHUB_CHANNEL_ID: آیدی عددی کانال @traanhub
   - STORAGE_CHANNEL_ID: آیدی عددی کانال @TraanFilmStorage

🎯 **مرحله ۴: اضافه کردن فیلم**
1. فیلم را در @TraanFilmStorage آپلود کنید
2. روی آن ریپلای کرده و /getid بزنید
3. با /setfilm فیلم را تنظیم کنید

🔗 **لینک تست فعلی:**
`https://t.me/TraanFilmBot?start=test`
"""
    
    await update.message.reply_text(guide, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """راهنمای کامل"""
    help_text = """
🆘 **راهنمای ربات ترن فیلم**

📋 **دستورات کاربری:**
/start - شروع کار
/test - تست ربات
/setup - راهنمای تنظیم
/help - این راهنما

⚙️ **دستورات ادمین (فقط شما):**
/setfilm - تنظیم فیلم جدید
/getid - دریافت File ID
/status - وضعیت ربات

🎬 **نحوه کار ربات:**
1. کاربر در کانال روی لینک کلیک می‌کند
2. ربات عضویت را بررسی می‌کند
3. فیلم ارسال می‌شود
4. تبلیغات نمایش داده می‌شود

📞 **پشتیبانی:** @stevenmacmin
"""
    
    await update.message.reply_text(help_text)

async def setfilm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تنظیم فیلم - فقط ادمین"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ دسترسی ندارید!")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "📝 فرمت: `/setfilm کد_فیلم FILE_ID`\n\n"
            "🎬 مثال:\n"
            "`/setfilm test AgACAgIAAxkBAAI8B0xAAgABQvfkMxiHFwACLwQAAgJHAAIuCwAC8h7F7wE`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    film_key = context.args[0]
    file_id = context.args[1]
    
    if film_key in FILMS:
        FILMS[film_key]["file_id"] = file_id
        await update.message.reply_text(
            f"✅ فیلم تنظیم شد!\n\n"
            f"🎬 {FILMS[film_key]['title']}\n"
            f"🔗 لینک: https://t.me/TraanFilmBot?start={film_key}"
        )
    else:
        # اضافه کردن فیلم جدید
        FILMS[film_key] = {
            "title": f"🎬 فیلم {film_key}",
            "description": "توضیحات",
            "file_id": file_id,
            "caption": f"فیلم {film_key} - ارسال شده توسط ربات"
        }
        await update.message.reply_text(
            f"✅ فیلم جدید اضافه شد!\n\n"
            f"🎬 کد: {film_key}\n"
            f"🔗 لینک: https://t.me/TraanFilmBot?start={film_key}"
        )

async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت File ID - فقط ادمین"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ دسترسی ندارید!")
        return
    
    if update.message.reply_to_message:
        msg = update.message.reply_to_message
        
        if msg.video:
            file_id = msg.video.file_id
            await update.message.reply_text(
                f"🎥 File ID (ویدیو):\n`{file_id}`\n\n"
                f"برای تنظیم: `/setfilm test {file_id}`",
                parse_mode=ParseMode.MARKDOWN
            )
        elif msg.document:
            file_id = msg.document.file_id
            await update.message.reply_text(
                f"📄 File ID (فایل):\n`{file_id}`\n\n"
                f"برای تنظیم: `/setfilm test {file_id}`",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "📌 لطفا روی یک ویدیو یا فایل ریپلای کنید."
            )
    else:
        await update.message.reply_text(
            "📌 روی یک ویدیو ریپلای کنید و /getid بزنید."
        )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """وضعیت ربات"""
    from telegram import Bot
    
    try:
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        
        films_ready = sum(1 for f in FILMS.values() if f["file_id"])
        
        status_text = f"""
📊 **وضعیت ربات:**

🤖 **مشخصات:**
• نام: {me.first_name}
• یوزرنیم: @{me.username}
• آیدی: {me.id}

👑 **ادمین:**
• {ADMIN_USERNAME}
• آیدی: {ADMIN_ID}

🎬 **فیلم‌ها:**
• کل: {len(FILMS)}
• آماده: {films_ready}
• تنظیم نشده: {len(FILMS) - films_ready}

🔧 **کانال‌ها:**
• @traanfilm: {'✅' if TRAANFILM_CHANNEL_ID else '❌'}
• @traanhub: {'✅' if TRAANHUB_CHANNEL_ID else '❌'}
• @TraanFilmStorage: {'✅' if STORAGE_CHANNEL_ID else '❌'}

🚀 **میزبان: Railway**
✅ **وضعیت:** آنلاین
"""
        
        await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {str(e)}")

# ==================== تابع اصلی ====================
def main():
    """شروع ربات"""
    print("=" * 50)
    print("🤖 راه‌اندازی ربات ترن فیلم (نسخه Railway)")
    print(f"👑 ادمین: {ADMIN_USERNAME}")
    print("🚀 میزبان: Railway")
    print("=" * 50)
    
    try:
        # ساخت اپلیکیشن
        app = Application.builder().token(BOT_TOKEN).build()
        
        # اضافه کردن دستورات
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("test", test))
        app.add_handler(CommandHandler("setup", setup))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("setfilm", setfilm))
        app.add_handler(CommandHandler("getid", getid))
        app.add_handler(CommandHandler("status", status))
        
        print("✅ ربات ساخته شد!")
        print("✅ Railway آماده اجرا")
        print("⏳ در حال اتصال به تلگرام...")
        
        # شروع
        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        print("\n🔧 **راه‌حل Railway:**")
        print("1. در Railway Variables را چک کنید")
        print("2. BOT_TOKEN را تنظیم کنید")
        print("3. Railway را Redeploy کنید")

if __name__ == '__main__':
    main()
