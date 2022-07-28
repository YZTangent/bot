from connection import supabaseinteraction as supa
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
from cogs import private_check
from connection.exceptions import UserNotRegisteredError


async def birthday_wishes_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Please configure birthday wish settings in your group."
    )


async def birthday_wishes_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! Please tell me your birthday so I can send you a little surprise :3",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Opt in", callback_data=("bday", True))],
            [InlineKeyboardButton("Opt Out", callback_data=("bday", False))],
            [InlineKeyboardButton("Turn on", callback_data=("bday"))],
            [InlineKeyboardButton("Turn off", callback_data=("bday"))],
        ])
    )


def birthday_wishes():
    return CommandHandler("birthday", private_check(birthday_wishes_private, birthday_wishes_group))