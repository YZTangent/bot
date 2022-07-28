from telegram.constants import ParseMode
from connection import supabaseinteraction as supa
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)
from cogs import private_check, escape_markdown
from connection.exceptions import UserNotRegisteredError


async def list_event_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    try:
        events = await supa.get_teleuser_events(user_id)
        keyboard = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton(i['activity'], callback_data=("events", i, user_id)) for i in events]
        )
        text = "Here are the list of events you are involved in\!"
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard
        )
    except UserNotRegisteredError as e:
        await update.effective_user.send_message(
            "Please register with the bot first with /start!"
        )


async def list_event_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    try:
        events = await supa.get_teleuser_events(user_id)
        # events = await supa.get_telechat_events(chat_id)
        keyboard = InlineKeyboardMarkup.from_column(
            # [InlineKeyboardButton(i['activity'], callback_data=("events", i, chat_id)) for i in events]
            [InlineKeyboardButton(i['activity'], callback_data=("events", i, user_id)) for i in events]
        )
        text = "Here are the list of events this group is involved in\!"
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard
        )
    except UserNotRegisteredError as e:
        await update.effective_user.send_message(
            "Please register with the bot first with /start!"
        )


def list_events():
    return CommandHandler("list_events", private_check(list_event_private, list_event_group))