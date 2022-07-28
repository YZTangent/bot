import disnake
from disnake.ext import commands
from dotenv import load_dotenv
# from interactions import SlashCommand
import os
from supabase import create_client, Client
import sys
sys.path.append('..')
from connection import supabaseinteraction

# load credentials
load_dotenv()
# BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

# instantiate supabase client
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
# supabase.table("discordlog").insert({"action":"Startup"}).execute()


# instantiate a bot
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='%',
    intents=intents,
    test_guilds=[979375763348406292]
)

@bot.event
async def on_ready():
    print('Ready.')

@bot.event
async def on_message(message):
    if type(message.channel) == disnake.channel.DMChannel:
        if message.content == "ping":
            await message.reply("pong")

@bot.event
async def on_guild_scheduled_event_subscribe(event, user):
    sbid = await supabaseinteraction.get_user_uuid(DiscID = user.id)
    rsvpinfo = {
        "userID": sbid,
        "eventID": event.description,
        "avail": True
    }
    await supabaseinteraction.set_rsvp(rsvpinfo)

@bot.event
async def on_guild_scheduled_event_unsubscribe(event, user):
    sbid = await supabaseinteraction.get_user_uuid(DiscID = user.id)
    rsvpinfo = {
        "userID": sbid,
        "eventID": event.description,
        "avail": False
    }
    await supabaseinteraction.set_rsvp(rsvpinfo)

bot.load_extension("cogs.Slash")
bot.run(BOT_TOKEN)