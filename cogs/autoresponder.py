import discord
from discord.ext import commands
import sys
sys.path.append("../")
import random


class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        autorespondtable = await self.bot.pool.fetch("SELECT * FROM autorespond WHERE guildid = $1", message.guild.id)

        if autorespondtable == []:
            return

        for responses in autorespondtable:
            trigger = responses["respondto"]
            response = responses["respondwith"]
            if trigger in message.content:
                if message.content.startswith("/autorespond"):
                    return

                await message.channel.send(response)
            else:
                return

def setup(bot):
    bot.add_cog(AutoResponder(bot))