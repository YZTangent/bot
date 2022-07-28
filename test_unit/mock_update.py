from typing import TYPE_CHECKING, Any, ClassVar, List, Optional
import datetime
from telegram import CallbackQuery
from telegram import ChatJoinRequest
from telegram import ChatMemberUpdated
from telegram import ChosenInlineResult
from telegram import InlineQuery
from telegram import PreCheckoutQuery
from telegram import ShippingQuery
from telegram import Poll, PollAnswer
from telegram import Location


class Chat:
    def __init__(
            self,
            type: str = None
    ):
        self.type = type


class Message:
    def __init__(
            self,
            message_id: int,
            date: datetime.datetime,
            forward_date: datetime.datetime = None,
            reply_to_message: "Message" = None,
            edit_date: datetime.datetime = None,
            text: str = None,
            chat: Chat = None,
            location: Location = None,
            **_kwargs: Any,
    ):
        # Required
        self.message_id = message_id
        # Optionals
        self.date = date
        self.chat = chat
        self.forward_date = forward_date
        self.reply_to_message = reply_to_message
        self.edit_date = edit_date
        self.text = text
        self.location = location

        self._id_attrs = (self.message_id, self.chat)

    @property
    def chat_id(self) -> int:
        """:obj:`int`: Shortcut for :attr:`telegram.Chat.id` for :attr:`chat`."""
        return self.chat.id

    @property
    def id(self) -> int:  # pylint: disable=invalid-name
        """
        :obj:`int`: Shortcut for :attr:`message_id`.
            .. versionadded:: 20.0
        """
        return self.message_id

    def reply_text(self, text):
        return "reply", text


class Effect:

    def send_message(self, text):
        return "private", text


class Update:
    def __init__(
            self,
            update_id: int,
            message: Message = None,
            edited_message: Message = None,
            channel_post: Message = None,
            edited_channel_post: Message = None,
            inline_query: InlineQuery = None,
            chosen_inline_result: ChosenInlineResult = None,
            callback_query: CallbackQuery = None,
            shipping_query: ShippingQuery = None,
            pre_checkout_query: PreCheckoutQuery = None,
            poll: Poll = None,
            poll_answer: PollAnswer = None,
            my_chat_member: ChatMemberUpdated = None,
            chat_member: ChatMemberUpdated = None,
            chat_join_request: ChatJoinRequest = None,
            **_kwargs: Any,
    ):
        # Required
        self.update_id = update_id
        # Optionals
        self.message = message
        self.edited_message = edited_message
        self.inline_query = inline_query
        self.chosen_inline_result = chosen_inline_result
        self.callback_query = callback_query
        self.shipping_query = shipping_query
        self.pre_checkout_query = pre_checkout_query
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
        self.poll = poll
        self.poll_answer = poll_answer
        self.my_chat_member = my_chat_member
        self.chat_member = chat_member
        self.chat_join_request = chat_join_request
        self.effective_user = Effect
