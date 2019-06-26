import discord
from discord.ext import commands
import asyncio
import datetime


class Administrative(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command = True)
    @commands.has_permissions(manage_guild = True)
    async def automod(self, ctx):
        """Main automod command."""
        embed = discord.Embed(title = "Automod Settings", description = "**Usage:**\n\n/automod on\n/automod off\n/automod inviteblocker\n/automod cursewords", color = discord.Color.blurple())
        await ctx.send(embed = embed)

    @automod.command()
    @commands.has_permissions(manage_guild = True)
    @commands.guild_only()
    async def on(self, ctx):
        """Turns automod on."""
        guild = await self.bot.pool.fetch("SELECT * FROM lightswitch WHERE guildid = $1", ctx.guild.id)

        if guild == []:
            await self.bot.pool.execute("INSERT INTO lightswitch VALUES ($1, $2)", ctx.guild.id, True)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="I have turned on automod for this guild.")
            await ctx.send(embed=embed)
            return
        else:
            if guild[0]["automoderation"] == True:
                embed=discord.Embed(title="Error", color=discord.Color.blurple(), description="Automod is already on for this guild.")
                await ctx.send(embed=embed)                
                return
            else:
                await self.bot.pool.execute("UPDATE lightswitch SET automoderation = $1 WHERE guildid = $2", True, ctx.guild.id)
                embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="I have turned on automod for this guild.")
                await ctx.send(embed=embed)

    @automod.command()
    @commands.has_permissions(manage_guild = True)
    @commands.guild_only()
    async def off(self, ctx):
        """Turns automod off."""
        guild = await self.bot.pool.fetch("SELECT * FROM lightswitch WHERE guildid = $1", ctx.guild.id)

        if guild == []:
            await self.bot.pool.execute("INSERT INTO lightswitch VALUES ($1, $2)", ctx.guild.id, False)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="I have turned off automod for this guild.")
            await ctx.send(embed=embed)
            return
        else:
            if guild[0]["automoderation"] == False:
                embed=discord.Embed(title="Error", color=discord.Color.blurple(), description="Automod is already off for this guild.")
                await ctx.send(embed=embed)
                return
            else:
                await self.bot.pool.execute("UPDATE lightswitch SET automoderation = $1 WHERE guildid = $2", False, ctx.guild.id)
                embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="I have turned off automod for this guild.")
                await ctx.send(embed=embed)

    @automod.command()
    @commands.has_permissions(manage_guild = True)
    async def inviteblocker(self, ctx):
        """Toggles the invite blocker feature for the server."""
        guild = await self.bot.pool.fetchrow("SELECT * FROM automodsettings WHERE guildid = $1", ctx.guild.id)
        if guild == None:
            await self.bot.pool.execute("INSERT INTO automodsettings VALUES ($1, $2, $3)", ctx.guild.id, False, False)

        status = await self.bot.pool.fetch("SELECT * FROM automodsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["discordinvites"] == True or status[0]["discordinvites"] == []:
            await self.bot.pool.execute("UPDATE automodsettings SET discordinvites = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Invite Blocker has been turned off for this guild.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE automodsettings SET discordinvites = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Invite Blocker has been turned on for this guild.")
            await ctx.send(embed=embed)

    @automod.command()
    @commands.has_permissions(manage_guild = True)
    async def cursewords(self, ctx):
        """Toggles the blocked word feature for the server."""
        guild = await self.bot.pool.fetchrow("SELECT * FROM automodsettings WHERE guildid = $1", ctx.guild.id)
        if guild == None:
            await self.bot.pool.execute("INSERT INTO automodsettings VALUES ($1, $2, $3)", ctx.guild.id, False, False)

        status = await self.bot.pool.fetch("SELECT * FROM automodsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["cursewords"] == True or status[0]["cursewords"] == []:
            await self.bot.pool.execute("UPDATE automodsettings SET cursewords = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Curse words have been turned off for this guild.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE automodsettings SET cursewords = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Curse words have been turned on for this guild.")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def addword(self, ctx, word: str):
        """Adds a word to list of blocked words"""
        wcheck = await self.bot.pool.fetch("SELECT * FROM cursewords WHERE guildid = $1 AND word = $2", ctx.guild.id, word)

        if wcheck != []:
            await ctx.send("That word is already blocked in this server!")
            return
        else:
            await self.bot.pool.execute("INSERT INTO cursewords VALUES ($1, $2)", ctx.guild.id, word)
            await ctx.send("That word is now blocked in this server.\n(The Blocked Word feature is not on automatically. To turn it on or off use `/automod cursewords`)")
            return

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def removeword(self, ctx, word: str):
        """Removes a word from the list of blocked words."""
        wcheck = await self.bot.pool.fetch("SELECT * FROM cursewords WHERE guildid = $1 AND word = $2", ctx.guild.id, word)

        if wcheck == []:
            await ctx.send("That word is not blocked in this server!")
            return
        else:
            await self.bot.pool.execute("DELETE FROM cursewords WHERE guildid = $1 AND word = $2", ctx.guild.id, word)
            await ctx.send("That word is now un-blocked in this server.\n(The Blocked Word feature is not on automatically. To turn it on or off use `/automod cursewords`)")
            return

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def words(self, ctx):
        """Lists all the blocked words in that server."""
        wcheck = await self.bot.pool.fetch("SELECT * FROM cursewords WHERE guildid = $1", ctx.guild.id)
        if wcheck == []:
            await ctx.send("There are no blocked words in this server.")
            return

        wordsstring = []

        for words in wcheck:
            word = words["word"]
            wordsstring.append(word)

        embed = discord.Embed(title = f"Blocked Words for {ctx.guild.name}", description = "\n".join(wordsstring), color = discord.Color.blurple())
        await ctx.send(embed = embed)

    @commands.group(invoke_without_command = True)
    @commands.has_permissions(manage_guild = True)
    async def log(self, ctx):
        """Main log control command."""
        embed=discord.Embed(title="Logging Settings", color=discord.Color.blurple(), description="To toggle each setting, please use the commands below:")
        embed.add_field(name= ( "​" ), value = "message delete: ``/log messagedelete`` \nmember join: ``/log memberjoin`` \nmember leave: ``/log memberleave`` \nmember ban: ``/log memberban``  \nmember unban: ``/log memberunban`` \nchannel create: ``/log channelcreate`` \nchannel delete: ``/log channeldelete`` \nrole create: ``/log channelcreate`` \nrole delete: ``/log roledelete`` \nbulk message delete: ``/log bulkmessagedelete`` \nmessage edit: ``/log messageedit``")
        await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def messagedelete(self, ctx):
        """Toggles the message_delete event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["message_delete"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET message_delete = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for deleting message.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET message_delete = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for deleting message.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def memberjoin(self, ctx):
        """Toggles the member_join event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["member_join"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET member_join = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for members joining.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET member_join = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for members joining.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def memberleave(self, ctx):
        """Toggles the member_leave event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["member_leave"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET member_leave = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for members leaving.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET member_leave = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for members leaving.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def memberban(self, ctx):
        """Toggles the member_ban event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["member_ban"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET member_ban = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for members being banned.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET member_ban = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for members being banned.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def memberunban(self, ctx):
        """Toggles the member_unban event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["member_unban"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET member_unban = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for members being un-banned.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET member_unban = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for members being un-banned.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def channelcreate(self, ctx):
        """Toggles the channel_create event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["channel_create"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET channel_create = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for channels being created.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET channel_create = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for channels being created.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def channeldelete(self, ctx):
        """Toggles the channel_delete event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["channel_delete"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET channel_delete = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for channels being deleted.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET channel_delete = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for channels being deleted.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def rolecreate(self, ctx):
        """Toggles the role_create event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["role_create"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET role_create = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for roles being created.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET role_create = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for roles being created.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def roledelete(self, ctx):
        """Toggles the role_delete event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["role_delete"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET role_delete = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for roles being deleted.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET role_delete = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for roles being deleted.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def bulkmessagedelete(self, ctx):
        """Toggles the bulk_message_delete event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["bulk_message_delete"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET bulk_message_delete = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for bulk messages being deleted.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET bulk_message_delete = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for bulk messages being deleted.")
            await ctx.send(embed=embed)

    @log.command()
    @commands.has_permissions(manage_guild = True)
    async def messageedit(self, ctx):
        """Toggles the message_edit event."""
        status = await self.bot.pool.fetch("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)

        if status[0]["message_edit"] == True:
            await self.bot.pool.execute("UPDATE loggingsettings SET message_edit = $1 WHERE guildid = $2", False, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned off for messages being edited.")
            await ctx.send(embed=embed)
            return
        else:
            await self.bot.pool.execute("UPDATE loggingsettings SET message_edit = $1 WHERE guildid = $2", True, ctx.guild.id)
            embed=discord.Embed(title="Done!", color=discord.Color.blurple(), description="Logging has been turned on for messages being edited.")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Administrative(bot))