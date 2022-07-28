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


async def build_rsvp_message(event_info):
    coming = await supa.get_rsvp_by_event(event_info['id'], True)
    not_coming = await supa.get_rsvp_by_event(event_info['id'], False)

    header = "*Will you be coming for* {}*?*" \
             "\n {}" \
             "\n {}" \
             "\n*Location:* {}" \
             "\n" \
        .format(escape_markdown(event_info['activity']),
                "\n" + escape_markdown(event_info['description']) if event_info['description'] else "",
                "\n" + "*Date:* " + event_info['starttime'][0:10].replace("-", "\/") + "\n" + "\n*Time:* "
                + event_info['starttime'][11:].replace("-", " UTC\-").replace("+", " UTC\+")
                    if event_info['starttime'] else "\n*Time:* TBC",
                escape_markdown(event_info['location']) if event_info['location'] else "TBC")

    coming = "\n*Coming:* " \
             "\n{}" \
             "\n*Not Coming:* " \
             "\n{}" \
        .format("\n".join([i["username"] for i in coming]) + "\n" if coming else "",
                "\n".join([i["username"] for i in not_coming]))

    text = header + coming
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes, I'm coming!", callback_data=("rsvp", True, event_info))],
        [InlineKeyboardButton("No, I can't make it :(", callback_data=("rsvp", False, event_info))],
        [InlineKeyboardButton("Refresh", callback_data=("reload", event_info))]
    ])
    return text, keyboard


async def send_rsvp_private(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! Please send your RSVP to a group."
    )


async def send_rsvp_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    try:
        events = await supa.get_teleuser_events(user_id)
        keyboard = InlineKeyboardMarkup.from_column(
            [InlineKeyboardButton(i['activity'], callback_data=("events", i, user_id)) for i in events]
        )
        text = "Please select your event\!"
        await update.message.reply_text(
            text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard
        )
    except UserNotRegisteredError as e:
        await update.effective_user.send_message(
            "Please register with the bot first with /start!"
        )


async def load_rsvp_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    _, event_info, user_id = query.data
    if query.from_user.id == user_id:
        await query.answer()

        text, keyboard = await build_rsvp_message(event_info)
        await query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
    else:
        await query.answer()
        await update.effective_user.send_message(
            "Only the user who is sending the RSVP can choose the event!"
        )

    context.drop_callback_data(query)


async def handle_rsvp_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    _, available, event_info = query.data
    user_id = await supa.get_user_uuid(TeleID=query.from_user.id)
    rsvp_info = {
        "userID": user_id,
        "eventID": event_info['id'],
        "avail": available,
        "eventname": event_info["activity"]
    }
    await query.answer()
    await supa.set_rsvp(rsvp_info)
    text, keyboard = await build_rsvp_message(event_info)
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboard,
    )


async def reload_rsvp_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    _, event_info = query.data
    await query.answer()
    text, keyboard = await build_rsvp_message(event_info)
    await query.edit_message_text(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboard,
    )


def choose_rsvp():
    return CommandHandler("send_rsvp", private_check(send_rsvp_private, send_rsvp_group))


def send_rsvp():
    return CallbackQueryHandler(load_rsvp_message, lambda callback: callback[0] == "events")


def handle_rsvp():
    return CallbackQueryHandler(handle_rsvp_message, lambda callback: callback[0] == "rsvp")


def reload_rsvp():
    return CallbackQueryHandler(reload_rsvp_message, lambda callback: callback[0] == "reload")
