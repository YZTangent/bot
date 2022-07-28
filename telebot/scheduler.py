from datetime import datetime
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from connection import supabaseinteraction as supa
from connection.exceptions import UserNotRegisteredError, InvalidDatetimeError
from connection.helper import datetime_validation
from cogs import private_check


def create_reminder():
    MESSAGE, INTERVAL, STARTTIME, ENDTIME = range(4)
    reminder_info = {}

    async def create_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Starting point of a reminder creation which asks for a description of the reminder."""
        reminder_info["chat"] = update.message.chat_id
        await update.message.reply_text(
            "Hi! Please tell me the message of your reminder!"
        )

        return MESSAGE

    async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Stores the activity description and asks for a location."""
        reminder_info["message"] = update.message.text
        await update.message.reply_text(
            "Got it! Now, please tell me how often do you want this reminder to repeat? Choose from one of the "
            "standard options below or input the number of hours between each reminder.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Once Only")],
                    [KeyboardButton(text="Once Every Hour")],
                    [KeyboardButton(text="Once Every Day")],
                    [KeyboardButton(text="Once Every Week")],
                ],
                one_time_keyboard=True
            )
        )

        return INTERVAL

    async def interval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        reminder_info["interval"] = update.message.text
        await update.message.reply_text(
            "When does your reminder start? lease let me know either through the WebApp or "
            "in YYYY/MM/DD TTTT +UTC format.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(
                        text="Now",
                    )],
                    [KeyboardButton(
                        text="Choose your time here!",
                        web_app=WebAppInfo(url="https://62df21d4b2873b0479f08480--vermillion-starship-08839f.netlify"
                                               ".app/"),
                    )],
                ],
                one_time_keyboard=True
            )
        )

        return STARTTIME

    async def start_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        # try:
        #     date, time, timezone = update.message.text.split()
        #     year, month, day = date.split("/")
        #     hour = ops[timezone[0]](int(time[0:2]), int(timezone[1])) % 24
        #     minute = int(time[2:])
        #     ts = datetime(int(year), int(month), int(day), hour, minute).isoformat()
        #     reminder_info["starttime"] = update.message.text
        #     reminder_info["finalised"] = True
        # except ValueError:
        #     await update.message.reply_text(
        #         "Invalid Date/Time!"
        #     )
        #     return STARTTIME
        await update.message.reply_text(
            "When does your reminder end? If you wish for the reminder to continue forever, you can skip this step"
            " with /skip!"
        )

        return ENDTIME

    async def endtime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        dur = update.message.text
        if isinstance(dur, int) and dur > 0:
            reminder_info["duration"] = update.message.text
            user_id = update.message.from_user.id
            reminder_info["creatorID"] = await supa.get_user_uuid(TeleID=user_id)
            await supa.send_reminder(reminder_info)
            await update.message.reply_text(
                "Your reminder has been created!"
            )

            return ConversationHandler.END
        else:
            await update.message.reply_text(
                "Please insert a valid number of hours!"
            )

            return ConversationHandler.END

    async def skip_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await supa.send_reminder(reminder_info)
        await update.message.reply_text(
            "Your reminder has been created!"
        )

        return ConversationHandler.END

    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancels and ends the conversation."""
        user = update.message.from_user
        await update.message.reply_text(
            "Aww :( See you again soon!"
        )

        return ConversationHandler.END

    return ConversationHandler(
        entry_points=[CommandHandler("create_reminder", create_reminder)],
        states={
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, message)],
            INTERVAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, interval),
            ],
            STARTTIME: [
                MessageHandler(filters.TEXT, start_time),
            ],
            ENDTIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, endtime),
                CommandHandler("skip", skip_end),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


async def create_event_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Which of the following reminders do you wish to activate? Choose from one of the "
        "standard options below or set a custom time using the WebApp!",
        reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("An Hour Before", callback_data=("remind", True))],
                [InlineKeyboardButton("Two Hours Before", callback_data=("remind", True))],
                [InlineKeyboardButton("A Day Before", callback_data=("remind", True))],
                [InlineKeyboardButton("2 Days Before", callback_data=("remind", True))],
                [InlineKeyboardButton("A Week Before", callback_data=("remind", True))],
                # [InlineKeyboardButton(
                #     "Custom",
                #     callback_data=("remind", True),
                #     web_app=WebAppInfo(url="https://62df21d4b2873b0479f08480--vermillion-starship-08839f.netlify"
                #                                ".app/"),
                # )],
            ]
        )
    )


def event_reminder():
    return CommandHandler("event_reminder", create_event_reminder)


async def callback_timer(update, context):
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name

    async def alert(context):
        # Beep the person who called this alarm:
        await context.bot.send_message(chat_id=context.job.chat_id, text=f'BEEP {context.job.context}!')

    await context.bot.send_message(chat_id=chat_id, text='Setting a timer for 1 minute!')
    # Set the alarm:
    await context.job_queue.run_once(alert, 60, context=name, chat_id=chat_id)
