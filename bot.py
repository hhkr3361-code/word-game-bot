import os
import anthropic
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, InlineQueryHandler, ContextTypes
import uuid

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

CATEGORIES = {
    "ولد": "اسم ولد عربي",
    "بنت": "اسم بنت عربي",
    "حيوان": "اسم حيوان بالعربي",
    "جماد": "اسم جماد بالعربي",
    "دولة": "اسم دولة بالعربي",
    "مدينة": "اسم مدينة بالعربي",
}

def get_name(category: str, letter: str) -> str:
    prompt = f"""أنت مساعد لعبة كلمات عربية.
أعطني اسماً عربياً واحداً فقط من فئة "{category}" يبدأ بحرف "{letter}".
شروط:
- اسم عربي حقيقي ومعروف
- يبدأ بالحرف المطلوب تحديداً
- اسم واحد فقط بدون أي شرح أو علامات ترقيم
- لا تكتب إلا الاسم فقط"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً! أنا بوت مساعد لعبة الكلمات 🎮\n\n"
        "الاستخدام في أي محادثة:\n"
        "@اسم_البوت [فئة] [حرف]\n\n"
        "مثال: @اسم_البوت حيوان ب\n\n"
        "الفئات المتاحة:\n"
        "ولد | بنت | حيوان | جماد | دولة | مدينة"
    )

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()

    if not query:
        return

    parts = query.split()
    if len(parts) < 2:
        return

    category_input = parts[0]
    letter = parts[1]

    # match category
    category = None
    for key in CATEGORIES:
        if key in category_input:
            category = CATEGORIES[key]
            break

    if not category or not letter:
        return

    try:
        name = get_name(category, letter)
        results = [
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=f"✅ {name}",
                description=f"{category_input} — حرف {letter}",
                input_message_content=InputTextMessageContent(name),
            )
        ]
        await update.inline_query.answer(results, cache_time=1)
    except Exception as e:
        pass

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(InlineQueryHandler(inline_query))
    app.run_polling()

if __name__ == "__main__":
    main()
