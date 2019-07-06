import discord
from discord.ext import commands, tasks
import sys
sys.path.append("../")
import random
import datetime
import asyncio
import aiohttp
import config
from ddblapi import DivineAPI
import json
import requests


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logchannel = "596797905528946734"
        self.dboats.start() # pylint: disable=no-member
        self.bfd.start() # pylint: disable=no-member
        self.ddb.start() # pylint: disable=no-member

    async def cog_unload(self):
        await self.dboats.cancel() # pylint: disable=no-member
        await self.bfd.cancel() # pylint: disable=no-member
        await self.ddb.cancel() # pylint: disable=no-member

    @tasks.loop(minutes = 30)
    async def dboats(self):
        base = "https://discord.boats/api/v2"

        data = {"server_count": len(self.bot.guilds)}
        headers = {
                "content-type": "APPLICATION/JSON",
                "Authorization": config.dboatstoken
                }
        try:
            requests.post(f"{base}/bot/{self.bot.user.id}", data=json.dumps(data), headers=headers)
            print("Posted Server Count to DBOATS")
        except Exception as erro:
            print(f"\n{error}\n")



    @tasks.loop(minutes = 30)
    async def bfd(self):
        base = "https://botsfordiscord.com/api"

        async with aiohttp.ClientSession() as cs:
            post = await cs.post(f"{base}/bot/{self.bot.user.id}",
            headers = {"Authorization": config.bfdtoken, "Content-Type": "application/json"}, data = {"server_count": len(self.bot.guilds)})
            post = await post.json()

            if "error" in post:
                print(f"Couldn't post server count, {post['error']}")
            else:
                print("Posted guild count to Bots For Discord")


    @tasks.loop(minutes = 30)
    async def ddb(self):
        bot_id = f"{self.bot.user.id}"
        api_key = f"{config.ddbtoken}"

        ddbl = DivineAPI(bot_id=bot_id, api_key=api_key)

        server_count = len(self.bot.guilds)
        post_stats = await ddbl.post_stats(server_count)
        
        if post_stats['error']:
            print(f"An error has occured:\n{post_stats['response']}")
        else:
            print('Successfully posted stats on Divine Discord Bot List !')


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

        if automodsettings[0]["discordinvites"] == False:
            return

        if message.content.startswith("discord.gg/"):
                await message.delete()
                await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in this server!")
        if message.content.startswith("http://discord.gg/"):
                await message.delete()
                await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in this server!")
        if message.content.startswith("https://discord.gg/"):
                await message.delete()
                await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in this server!")
        elif message.content.startswith("discordapp.com/invite"):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in this server!")
        elif message.content.startswith("http://discordapp.com/invite"):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in this server!")
        elif message.content.startswith("https://discordapp.com/invite"):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in this server!")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", message.guild.id)
        if guild == []:
            return

        if guild[0]["message_delete"] == False:
            return

        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return

        embed = discord.Embed(title = "Message Deleted", color = discord.Color.blurple())
        embed.add_field(name = "Message Content", value = message.content, inline = False)
        embed.add_field(name = "Message Author", value = message.author.mention, inline = False)
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", member.guild.id)
        if guild == []:
            return
        
        if guild[0]["member_join"] == False:
            return

        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return

        embed = discord.Embed(title = "Member Joined", description = f"{member.mention} ({member})", color = discord.Color.blurple())
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", member.guild.id)
        if guild == []:
            return
        
        if guild[0]["member_leave"] == False:
            return

        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return

        embed = discord.Embed(title = "Member Left", description = f"{member.mention} ({member})", color = discord.Color.blurple())
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", guild.id)
        if guild == []:
            return
        
        if guild[0]["member_ban"] == False:
            return

        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return

        embed = discord.Embed(title = "Member Banned", description = f"{user.mention} ({user})", color = discord.Color.blurple())
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        guild = await self.bot.pool.fetchrow("SELECT * FROM loggingsettings WHERE guildid = $1", guild.id)
        if guild == []:
            return
        
        if guild[0]["member_unban"] == False:
            return

        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return

        embed = discord.Embed(title = "Member Unbanned", description = f"{user.mention} ({user})", color = discord.Color.blurple())
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", channel.guild.id)
        if guild == []:
            return

        if guild[0]["channel_create"] == False:
            return
        
        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return

        embed = discord.Embed(title = "Channel Created", description = f"{channel.mention} ({channel.name})", color = discord.Color.blurple())
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", channel.guild.id)
        if guild == []:
            return

        if guild[0]["channel_delete"] == False:
            return
        
        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return

        embed = discord.Embed(title = "Channel Deleted", description = f"{channel.name}", color = discord.Color.blurple())
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", role.guild.id)
        if guild == []:
            return

        if guild[0]["role_create"] == False:
            return

        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return
        
        embed = discord.Embed(title = "Role Created", description = role.name, color = discord.Color.blurple())
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", role.guild.id)
        if guild == []:
            return

        if guild[0]["role_delete"] == False:
            return

        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return
        
        embed = discord.Embed(title = "Role Deleted", description = role.name, color = discord.Color.blurple())
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        randommsg = random.choice(messages)
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", randommsg.guild.id)
        if guild == []:
            return
        
        if guild[0]["bulk_message_delete"] == False:
            return

        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return

        embed = discord.Embed(title = "Bulk Message Delete", description = f"**{len(messages)}** messages were deleted in {randommsg.channel.mention}", color = discord.Color.blurple())
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", after.guild.id)
        if guild == []:
            return

        if guild[0]["message_edit"] == False:
            return

        logchannel = self.bot.get_channel(guild[0]["channelid"])

        if logchannel == None:
            return

        embed = discord.Embed(title = "Message Edited", color = discord.Color.blurple())
        embed.add_field(name = "Channel", value = after.channel.mention, inline = False)
        embed.add_field(name = "Content Before", value = before.content, inline = False)
        embed.add_field(name = "Content After", value = after.content, inline = False)
        embed.add_field(name = "Author", value = f"{after.author.mention} ({after.author})", inline = False)
        try:
            await logchannel.send(embed = embed)
        except discord.Forbidden:
            return

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined guild named '{guild.name}' with {guild.member_count} members")

        logchannel = self.bot.get_channel(self.logchannel)
        em = discord.Embed(title = "Joined Guild", color = discord.Color.blurple())
        em.set_thumbnail(url = guild.icon_url)
        em.add_field(name = "Name", value = guild.name)
        em.add_field(name = "ID", value = str(guild.id))
        em.add_field(name = "Owner", value = str(guild.owner))
        em.add_field(name = "Member Count", value = f"{guild.member_count:,d}")
        em.add_field(name = "Verification Level", value = str(guild.verification_level))
        em.add_field(name = "Channel Count", value = f"{len(guild.channels):,d}")
        em.add_field(name = "Creation Time", value = guild.created_at)

        em.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed = em)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"Left guild named '{guild.name}' that had {guild.member_count} members")

        logchannel = self.bot.get_channel(self.logchannel)
        em = discord.Embed(title = "Left Guild", color = discord.Color.purple())
        em.set_thumbnail(url = guild.icon_url)
        em.add_field(name = "Name", value = guild.name)
        em.add_field(name = "ID", value = str(guild.id))
        em.add_field(name = "Owner", value = str(guild.owner))
        em.add_field(name = "Member Count", value = f"{guild.member_count:,d}")
        em.add_field(name = "Verification Level", value = str(guild.verification_level))
        em.add_field(name = "Channel Count", value = f"{len(guild.channels):,d}")
        em.add_field(name = "Creation Time", value = guild.created_at)

        em.timestamp = datetime.datetime.utcnow()
        await logchannel.send(embed = em)


def setup(bot):
    bot.add_cog(Events(bot))