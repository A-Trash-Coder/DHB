import discord
from discord.ext import commands
import sys
sys.path.append("../")
import random


class Events(commands.Cog):
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
                if message.content.startswith("/addword") or message.content.startswith("/removeword"):
                    return

                await message.delete()
                await message.channel.send(f"{message.author.mention}, you are not allowed to say that word in this server!")

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
        elif message.content.startswith("discordapp.com/invite"):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you are not allowed to send invites in this server!")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", message.guild.id)
        if guild == []:
            return

        if guild[0]["message_delete"] == False:
            return

        logchannel = self.bot.get_channel(guild["channelid"])

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

        logchannel = self.bot.get_channel(guild["channelid"])

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

        logchannel = self.bot.get_channel(guild["channelid"])

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

        logchannel = self.bot.get_channel(guild["channelid"])

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

        logchannel = self.bot.get_channel(guild["channelid"])

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
        
        logchannel = self.bot.get_channel(guild["channelid"])

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
        
        logchannel = self.bot.get_channel(guild["channelid"])

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

        logchannel = self.bot.get_channel(guild["channelid"])

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

        logchannel = self.bot.get_channel(guild["channelid"])

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

        logchannel = self.bot.get_channel(guild["channelid"])

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

        logchannel = self.bot.get_channel(guild["channelid"])

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


def setup(bot):
    bot.add_cog(Events(bot))