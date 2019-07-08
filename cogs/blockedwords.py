import discord
from discord.ext import commands
import sys
sys.path.append("../")
import random


class BlockedWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        guildautomod = await self.bot.pool.fetch("SELECT * FROM lightswitch WHERE guildid = $1", message.guild.id)
        automodsettings = await self.bot.pool.fetch("SELECT * FROM automodsettings WHERE guildid = $1", message.guild.id)
        if guildautomod == []:
            return

        if automodsettings == []:
            return

        if guildautomod[0]["automoderation"] == False:
            return

        if automodsettings[0]["cursewords"] == False:
            return

        cursewords = await self.bot.pool.fetch("SELECT * FROM cursewords WHERE guildid = $1", message.guild.id)

        if cursewords == []:
            return

        for curseword in cursewords:
            word = curseword["word"]
            if word in message.content:
                if message.content.startswith("/removeword"):
                    return

                await message.delete()
                await message.channel.send(f"{message.author.mention}, you are not allowed to say that word in this server!", delete_after = 10)

def setup(bot):
    bot.add_cog(BlockedWords(bot))