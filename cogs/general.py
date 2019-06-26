import discord
from discord.ext import commands
import asyncio
import datetime


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        """Shows the bot's latency."""
        botlatency = round(self.bot.latency * 1000, 3)
        embed = discord.Embed(title = "Pong!", description = f":ping_pong: `{botlatency}ms`", color = discord.Color.blurple())
        await ctx.send(embed = embed)

    @commands.command()
    @commands.guild_only()
    async def about(self, ctx):
        """Shows info about the bot."""
        embed = discord.Embed(title = f"About {self.bot.user.name}", color = discord.Color.blurple())
        embed.set_thumbnail(url = self.bot.user.avatar_url)
        embed.add_field(name = "Developers", value = "Kowlin#4417 & A Trash Coder#0981", inline = False)
        embed.add_field(name = "Library", value = "discord.py rewrite", inline = False)
        embed.add_field(name = "Source Code", value = "[Click here](https://github.com/kowlintechnologies/DHB)", inline = False)
        embed.add_field(name = "Links", value = "[Docs](https://dhb-documentation.readthedocs.io/en/latest/index.html) | [Support](https://discord.gg/KEkwrwd) | [Invite](https://discord.gg/KEkwrwd)")
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(General(bot))