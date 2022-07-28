import re
from telegram import Update
from telegram.ext import ContextTypes


def escape_markdown(text: str, version: int = 1, entity_type: str = None) -> str:
    """
    Helper function to escape telegram markup symbols.
    """

    escape_chars = r'_*[]()~`>#+-=|{}.!'

    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)


def private_check(private_func, group_func):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat.type == 'private':
            result = await private_func(update, context)

            return result
        else:
            result = await group_func(update, context)

            return result

    return inner
