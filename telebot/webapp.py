from connection import supabaseinteraction as supa
from connection.exceptions import UserNotRegisteredError, InvalidDatetimeError
from connection.helper import past_future_check, datetime_validation
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, WebAppInfo
from telegram.ext import (
    MessageHandler,
    ContextTypes,
    filters
)
import json


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    data = json.loads(update.effective_message.web_app_data.data)
    print(data)
    # if data["handler"] ==


def web_data():
    return MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data)