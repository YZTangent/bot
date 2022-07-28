import pytest
from telebot.create_event import create_event
from telebot.rsvp import send_rsvp, choose_rsvp, handle_rsvp, reload_rsvp
from telebot.list_event import list_events
from telebot.inline_rsvp import inline_rsvp
from telebot.scheduler import create_reminder, event_reminder
from telebot.birthday import birthday_wishes
from telebot.basic import start, help, get_id, set_birthday, web_data
from telebot.cogs import escape_markdown, private_check


@pytest.mark.parametrize("test_input,expected", [
    (":(*&$%*&", ":\(\*&$%\*&"),
    ("#&$&@+'_", "\#&$&@\+'\_"),
    ("€÷®π®¶£~", "€÷®π®¶£\~"),
])
def test_escape_markdown(test_input, expected):
    assert escape_markdown(test_input) == expected