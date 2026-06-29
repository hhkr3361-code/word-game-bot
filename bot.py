import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, MessageHandler, InlineQueryHandler, filters, ContextTypes
from uuid import uuid4

TOKEN = "8997876339:AAEvNsnToUWcQIlovWZfnLJ4rLgjm2FrPH4"

DATA = {
    "حيوان": {
        "أ": "أسد", "ب": "ببغاء", "ت": "تمساح", "ث": "ثعلب", "ج": "جمل", "ح": "حصان",
        "خ": "خروف", "د": "دب", "ذ": "ذئب", "ر": "رنة", "ز": "زرافة", "س": "سلحفاة",
        "ش": "شمبانزي", "ص": "صقر", "ض": "ضبع", "ط": "طاووس", "ظ": "ظبي", "ع": "عقرب",
        "غ": "غزال", "ف": "فيل", "ق": "قرد", "ك": "كلب", "ل": "لبؤة", "م": "ماعز",
        "ن": "نمر", "ه": "هدهد", "و": "وعل", "ي": "يمامة"
    },
    "ولد": {
        "أ": "أحمد", "ب": "بدر", "ت": "تركي", "ث": "ثامر", "ج": "جاسم", "ح": "حمد",
        "خ": "خالد", "د": "داود", "ذ": "ذياب", "ر": "راشد", "ز": "زيد", "س": "سالم",
        "ش": "شهاب", "ص": "صالح", "ض": "ضاري", "ط": "طارق", "ظ": "ظافر", "ع": "علي",
        "غ": "غانم", "ف": "فهد", "ق": "قاسم", "ك": "كريم", "ل": "لؤي", "م": "محمد",
        "ن": "ناصر", "ه": "هاني", "و": "وليد", "ي": "ياسر"
    },
    "بنت": {
        "أ": "أميرة", "ب": "بشاير", "ت": "تالا", "ث": "ثريا", "ج": "جواهر", "ح": "حنين",
        "خ": "خلود", "د": "دانة", "ذ": "ذكرى", "ر": "ريم", "ز": "زهرة", "س": "سارة",
        "ش": "شيخة", "ص": "صبا", "ض": "ضحى", "ط": "طيبة", "ظ": "ظافرة", "ع": "عهود",
        "غ": "غلا", "ف": "فاطمة", "ق": "قمر", "ك": "كوثر", "ل": "لمياء", "م": "مريم",
        "ن": "نورة", "ه": "هيا", "و": "وفاء", "ي": "يارا"
    },
    "جماد": {
        "أ": "أريكة", "ب": "باب", "ت": "تلفزيون", "ث": "ثلاجة", "ج": "جدار", "ح": "حقيبة",
        "خ": "خزانة", "د": "درج", "ذ": "ذهب", "ر": "رف", "ز": "زجاجة", "س": "سرير",
        "ش": "شمعة", "ص": "صندوق", "ض": "ضوء", "ط": "طاولة", "ظ": "ظرف", "ع": "عجلة",
        "غ": "غسالة", "ف": "فنجان", "ق": "قلم", "ك": "كرسي", "ل": "لوح", "م": "مفتاح",
        "ن": "نافذة", "ه": "هاتف", "و": "وسادة", "ي": "يد مروحة"
    },
    "دولة": {
        "أ": "الأردن", "ب": "البرازيل", "ت": "تركيا", "ث": "ثايلاند", "ج": "الجزائر", "ح": "الحبشة",
        "خ": "خوزستان", "د": "الدنمارك", "ذ": "ذباب", "ر": "روسيا", "ز": "زيمبابوي", "س": "السعودية",
        "ش": "الشيلي", "ص": "الصين", "ض": "ضمد", "ط": "طاجيكستان", "ظ": "ظفار", "ع": "العراق",
        "غ": "غانا", "ف": "فرنسا", "ق": "قطر", "ك": "الكويت", "ل": "لبنان", "م": "مصر",
        "ن": "نيجيريا", "ه": "هولندا", "و": "اليمن", "ي": "اليابان"
    }
}

ALIASES = {
    "حيوان": "حيوان", "حيوانات": "حيوان",
    "ولد": "ولد", "اولاد": "ولد",
    "بنت": "بنت", "بنات": "بنت",
    "جماد": "جماد", "جمادات": "جماد",
    "دولة": "دولة", "دول": "دولة"
}

logging.basicConfig(level=logging.INFO)

async def inline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    results = []

    if not query:
        return

    parts = query.split()
    if len(parts) < 2:
        return

    category = ALIASES.get(parts[0])
    if not category:
        return

    letter = parts[1][0]
    answer = DATA[category].get(letter)

    if answer:
        results.append(InlineQueryResultArticle(
            id=str(uuid4()),
            title=f"⚡ {answer}",
            description=f"{category} — حرف {letter}",
            input_message_content=InputTextMessageContent(answer)
        ))

    await update.inline_query.answer(results, cache_time=0)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) < 2:
        await update.message.reply_text("اكتب: فئة حرف\nمثال: حيوان ح")
        return

    category = ALIASES.get(parts[0])
    if not category:
        await update.message.reply_text("الفئات: حيوان، ولد، بنت، جماد، دولة")
        return

    letter = parts[1][0]
    answer = DATA[category].get(letter)
    if answer:
        await update.message.reply_text(f"⚡ {answer}")
    else:
        await update.message.reply_text(f"❌ مافي {category} بحرف {letter}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(InlineQueryHandler(inline))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("✅ البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
