from telegram.constants import ParseMode
from uuid import uuid4
from connection import supabaseinteraction as supa
from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
)
from telegram.ext import (
    InlineQueryHandler,
    ContextTypes,
)
from connection.exceptions import UserNotRegisteredError
from rsvp import build_rsvp_message


async def load_inline_rsvp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query
    user_id = update.inline_query.from_user.id

    print("new query")

    try:
        events = await supa.get_teleuser_events(user_id)
        results = []

        for i in events:
            if i['activity'].startswith(query):
                text, keyboard = await build_rsvp_message(i)
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid4()),
                        title=i['activity'],
                        description=i['description'],
                        input_message_content=InputTextMessageContent(
                            message_text=text,
                            parse_mode=ParseMode.MARKDOWN_V2
                        ),
                        reply_markup=keyboard
                    )
                )
        await update.inline_query.answer(results)
    except UserNotRegisteredError as e:
        await update.effective_user.send_message(
            "Please register with the bot first with /start!"
        )


def inline_rsvp():
    return InlineQueryHandler(load_inline_rsvp)