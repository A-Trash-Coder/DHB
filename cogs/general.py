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
        embed.add_field(name = "Links", value = "[Docs](https://dhb-documentation.readthedocs.io/en/latest/index.html) | [Support](https://discord.gg/KEkwrwd) | [Invite](https://discordapp.com/api/oauth2/authorize?client_id=592811241756688405&permissions=2080762998&scope=bot)")
        await ctx.send(embed = embed)

    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        embed = discord.Embed(title = f"Info for {ctx.guild.name}", color = discord.Color.blurple())
        embed.add_field(name = "Owner", value = ctx.guild.owner)
        embed.add_field(name = "ID", value = ctx.guild.id)
        embed.add_field(name = "Region", value = ctx.guild.region)
        embed.add_field(name = "Categories", value = len(ctx.guild.categories))
        embed.add_field(name = "Text Channels", value = len(ctx.guild.text_channels))
        embed.add_field(name = "Voice Channels", value = len(ctx.guild.voice_channels))
        embed.add_field(name = "Members", value = ctx.guild.member_count)
        embed.add_field(name = "Roles", value = len(ctx.guild.roles))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed = embed)

    @commands.command()
    @commands.guild_only()
    async def docs(self, ctx):
        embed = discord.Embed(title = "Documentation", description = "[Click here to visit our documentation!](https://dhb-documentation.readthedocs.io/en/latest/index.html)", color = discord.Color.blurple())
        await ctx.send(embed = embed)

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        embed=discord.Embed(title = f"{user.name}'s Information", color = discord.Color.blurple())
        embed.add_field(name = "Name:", value = user.mention)
        embed.add_field(name = "Name Hash:", value = user.name)
        embed.add_field(name = "Nickname:", value = user.nick)
        embed.add_field(name = "Account Created:", value = user.created_at.strftime("%m-%d-%Y"))
        embed.add_field(name = "Joined Server At:", value = user.joined_at.strftime("%m-%d-%Y"))
        embed.add_field(name = "ID:", value = user.id)
        embed.add_field(name = "Status", value = user.status)
        embed.add_field(name = "Activity:", value = user.activity)
        embed.add_field(name = "Highest Role", value = user.top_role)
        embed.add_field(name = ( "​" ), value = ( "​" ))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))