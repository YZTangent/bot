from connection import supabaseinteraction as supa
from connection.exceptions import UserNotRegisteredError, InvalidDatetimeError
from connection.helper import past_future_check, datetime_validation
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)
from telebot.cogs import private_check


async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    name = update.message.from_user.full_name
    try:
        await supa.get_user_uuid(TeleID=user_id)
        await update.message.reply_text("Hi {}! Welcome back to your trusty personal assistant and scheduler, "
                                        "Ka.Y.E!"
                                        "\n Use /createevent to create a new event, or check out the bot menu to "
                                        "explore "
                                        "all my functionalities!".format(name))
    except UserNotRegisteredError:
        await update.message.reply_text(
            "Hi! Welcome to your trusty personal assistant and scheduler, Ka.Y.E!"
            "Please press the button below Sign In or Sign Up via the WebApp to access all my functionalities!",
            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton(
                    text="Sign In or Sign Up Here!",
                    web_app=WebAppInfo(url="https://62df0c3dbfabcd0066040df7--fastidious-vacherin-ea59a9.netlify.app/"),
                ),
                one_time_keyboard=True
            ),
        )


async def start_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    name = update.message.from_user.full_name
    try:
        await supa.get_user_uuid(TeleID=user_id)
        await update.message.reply_text("Hi {}! Welcome to your trusty personal assistant and scheduler, Ka.Y.E!"
                                        "\n Head over to my DMs and use /createevent to create a new event, "
                                        "or check out the bot menu to explore "
                                        "all my functionalities!".format(name))
    except UserNotRegisteredError as e:
        await update.effective_user.send_message(
            "Hi! Welcome to your trusty personal assistant and scheduler, Ka.Y.E!"
            "Please press the button below Sign In or Sign Up via the WebApp to access all my functionalities!",
            reply_markup=ReplyKeyboardMarkup.from_button(
                KeyboardButton(
                    text="Sign In or Sign Up Here!",
                    web_app=WebAppInfo(url="https://62df0c3dbfabcd0066040df7--fastidious-vacherin-ea59a9.netlify.app/"),
                ),
                one_time_keyboard=True
            ),
        )


def start():
    return CommandHandler("start", private_check(start_private, start_group))


async def get_id_handler(update, context):
    await update.message.reply_text(update.message.from_user.id)


def get_id():
    return CommandHandler("get_id", get_id_handler)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text(
        "Welcome back to your trusty personal assistant and scheduler, Ka.Y.E!"
        "Use /createevent in a DM with me to create an event, and send out your rsvp with /send_rsvp in your group!"
        "Feel free to explore my menu to see all of my functionalities and their description :)"
    )


def help():
    return CommandHandler("help", help_command)


async def handle_invalid_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Informs the user that the button is no longer available."""
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        "Sorry, I could not process this button click 😕"
    )


async def set_birthday_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    try:
        bday = context.args[0].replace("/", "-")
        year, month, day = bday.split("-")
        if past_future_check(datetime_validation(int(year), int(month), int(day))) != "past":
            await update.message.reply_text(
                "Invalid Date!"
            )
            return
        id = await supa.get_user_uuid(TeleID=user_id)
        await update.message.reply_text(
            "Your birthday has been updated!"
        )
        await supa.update_birthday({
            'id': id,
            'bday': bday
        })
    except IndexError:
        await update.message.reply_text(
            "Please provide a date!"
        )
    except InvalidDatetimeError:
        await update.message.reply_text(
            "Invalid Date!"
        )
    except UserNotRegisteredError:
        await update.effective_user.send_message(
            "Please register with the bot first with /start!"
        )


def set_birthday():
    return CommandHandler("set_birthday", set_birthday_command)