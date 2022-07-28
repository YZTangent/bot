import asyncio
from operator import truediv
import disnake
from disnake.ext import commands
from typing import List
from datetime import datetime, timezone, timedelta
import sys
sys.path.append('..')
from connection import supabaseinteraction
import pytz
import uuid
# from interactions import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    local_tz = pytz.timezone('Asia/Singapore')
    utc_tz = pytz.utc

    def utc_to_local(utc_dt):
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(Slash.local_tz)
        return Slash.local_tz.localize(local_dt)

    def local_to_utc(local_dt):
        utc_dt = local_dt.replace(tzinfo=Slash.local_tz).astimezone(pytz.utc)
        return Slash.utc_tz.localize(utc_dt)

    def dt_to_iso(dt):
        return dt.strftime("%d/%m/%Y, %H%M")

    # autocompleteOptions = ["a", "b", "c", "d", "e"]

    async def autocomplete_options(inter, string: str) -> List[str]:
        return [x for x in ["a", "b", "c", "d", "e"] if string.lower() in x.lower()]

    async def autocomplete_events(inter, string: str) -> List[str]:
        foo = map(
            lambda x: x.name,
            await inter.guild.fetch_scheduled_events()
        )
        return [x for x in foo if string.lower() in x.lower()]

    async def autocomplete_edit(inter, string: str) -> List[str]:
        edit = ["location", "time", "rename", "duration"]
        return [x for x in edit if string.lower() in x.lower()]

    @commands.slash_command(description="Test command")
    async def test(inter):
        embed = disnake.Embed(title="Working")
        await inter.response.send_message(embeds=[embed])

    @commands.slash_command(description="Return your UID")
    async def myid(inter):
        await inter.response.send_message(str(inter.author.id))

    @commands.slash_command(description="Create an Event, specify date as DDMMYY, time in HHMM, and duration in hours")
    async def createevent(inter, activity: str, date: str, time: str, duration: int = 1):
        if(len(date) != 6 or len(time) != 4):
            await inter.response.send_message("Invalid Date/Time!")
            return
        day = int(date[0:2])
        month = int(date[2:4])
        year = int(date[4:]) + 2000
        hour = int(time[0:2])
        minute = int(time[2:])
        # ^^ this is local time, but
        # discord will take this as utc 0 and add 8 in discord interface, supabase takes this as utc 0
    # try:
        scheduled = datetime(year, month, day, hour, minute) - timedelta(hours=8)
        new_uuid = uuid.uuid1()
        ts = scheduled.isoformat() 
        event = {
            "id": str(new_uuid),
            "activity": activity,
            "starttime": ts,
            "duration": duration,
            "discgrp": inter.channel_id
        }
        await supabaseinteraction.send_event(event)
        metadata = disnake.GuildScheduledEventMetadata()
        metadata.location = "Somewhere"
        await inter.guild.create_scheduled_event(
            name = activity,
            description = str(new_uuid),
            entity_type = disnake.GuildScheduledEventEntityType(3),
            entity_metadata = metadata,
            scheduled_start_time = scheduled,
            scheduled_end_time = scheduled + timedelta(hours=1)
        )
        await inter.response.send_message("Event created successfully! Use /editevent to make changes if needed.")
        # except ValueError:
        #     await inter.response.send_message("Invalid Date/Time!")
        # except:
        #     await inter.response.send_message("Something went wrong...")


    @commands.slash_command(description="Edit an event")
    async def editevent(
        inter,
        action: str = commands.Param(autocomplete=autocomplete_edit),
        activty: str = commands.Param(autocomplete=autocomplete_events),
        to: str = None
    ):
        await inter.response.send_message("WIP")

    @commands.slash_command(description="List all events")
    async def listevent(inter):
        # Slash.utc_to_local(x.scheduled_start_time).strftime("%d/%m/%Y, %H%M")
        x = map(
            lambda x: x.name + " at \"" + x.entity_metadata.location + "\" on " + x.scheduled_start_time.strftime("%d/%m/%Y, %H%M") + "hrs. ",
            await inter.guild.fetch_scheduled_events()
        )
        await inter.response.send_message('\n'.join(x))


    # @commands.slash_command(description="Return your UID")
    # async def autocomplete(
    #     inter,
    #     text: str = commands.Param(autocomplete=autocomplete_options)
    # ):
    #     await inter.response.send_message(text)
    
def setup(bot):
    bot.add_cog(Slash(bot))