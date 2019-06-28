import discord
from discord.ext import commands
import sys
sys.path.append("../")
import random
import asyncio


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

    @commands.group(invoke_without_command = True)
    async def autorespond(self, ctx):
        return

    @autorespond.command()
    async def add(self, ctx):
        def check(message):
            if message.channel.id != ctx.channel.id:
                return False
            if message.author.id != ctx.author.id:
                return False

            return True

        await ctx.send("What's the word you would like to trigger the response?")
        try:
            trigger = await self.bot.wait_for("message", check = check, timeout = 30)
        except asyncio.TimeoutError:
            return

        await ctx.send("What would you like to respond with?")
        try:
            response = await self.bot.wait_for("message", check = check, timeout = 30)
        except asyncio.TimeoutError:
            return

        trigger_word = trigger.content
        response_phrase = response.content

        await self.bot.pool.execute("INSERT INTO autorespond VALUES ($1, $2, $3)", ctx.guild.id, f"{trigger_word}", f"{response_phrase}")

        embed = discord.Embed(title = "Done!", color = discord.Color.blurple())
        embed.add_field(name = f"{trigger_word} will be responded to with:", value = response_phrase)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AutoResponder(bot))