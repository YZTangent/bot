import asyncio
from operator import truediv
import disnake
from disnake.ext import commands, tasks
from typing import List
from datetime import datetime, timezone, timedelta
import sys
sys.path.append('..')
from connection import supabaseinteraction
import pytz
import uuid

class Sched(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0



    # Slash command
    @commands.slash_command(description="Test command")
    async def remind(
        inter,
        message: str = "",
        freq: int = 10
    ):
        class Confirm(disnake.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None
                self.author = inter.author

            # When the confirm button is pressed, set the inner value to `True` and
            # stop the View from listening to more input.
            # We also send the user an ephemeral message that we're confirming their choice.
            @disnake.ui.button(label="Stop", style=disnake.ButtonStyle.red)
            async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
                if interaction.author == self.author:
                    await interaction.response.send_message("Stopping reminders", ephemeral=True)
                    self.value = True
                    self.stop()
                else:
                    await interaction.response.send_message("You are not the reminder author", ephemeral=True)


            # This one is similar to the confirmation button except sets the inner value to `False`
            @disnake.ui.button(label="Cancel", style=disnake.ButtonStyle.grey)
            async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
                await interaction.response.send_message("Cancelling", ephemeral=True)
                self.value = False
                self.stop()

        # the returned task object
        # need to object.start() for it to run
        @tasks.loop(minutes=freq)
        async def theTask():
            targetChannel = inter.channel
            author = inter.author
            response = await inter.followup.send("{}\nThis reminder will be sent every {} minute(s)".format(message, freq))

        # how to get a reaction on the message to cancel the task?
        # need to keep the task somewhere
        
        # put theTask somewhere
        # storage.append(theTask)

        theTask.start() 
        view = Confirm()
        await inter.send('Reminder set: {}'.format(message), view=view)
        await view.wait()
        if view.value is None:
            print("Timed out...")
        elif view.value:
            theTask.stop()
            # print("Stopping...")
        else:
            print("Cancelled...")




def setup(bot):
    bot.add_cog(Sched(bot))

