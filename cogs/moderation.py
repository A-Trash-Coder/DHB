import discord
from discord.ext import commands
import random
import datetime
import utils.paginator as paginator
import asyncio


class Paginator(paginator.EmbedInterface):
    def __init__(self, ctx, pag):
        self.ctx = ctx
        self.p = pag
        super().__init__(self.ctx.bot, self.p, self.ctx.author)

    async def send_pages(self):
        await self.send_to(self.ctx)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkmark = "<:dhb_tickyes:587468735187779595>"
        self.x = "<:dhb_tickno:592046559131074570>"

    async def uplogamount(self, ctx):
        await self.bot.pool.execute("UPDATE modlog SET logamounts = logamounts + 1 WHERE guildid = $1", ctx.guild.id)

    async def sendlog(self, ctx, commandname: str, user: discord.Member, reason: str):
        guild = await self.bot.pool.fetchrow("SELECT * FROM modlog WHERE guildid = $1", ctx.guild.id)
        if guild != None:
            modlog = self.bot.get_channel(guild["channelid"])
            if modlog == None:
                return

            logamounts = guild["logamounts"]
            embed=discord.Embed(title=f"{commandname} | #{logamounts}", color=discord.Color.blurple())
            embed.add_field(name="User", value=f"{user.mention} ({user.name}#{user.discriminator})", inline=False)
            embed.add_field(name="Moderator", value=f"{ctx.author.mention} ({ctx.author.name}#{ctx.author.discriminator})", inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            msg = await modlog.send(embed=embed)
            await self.storecase(ctx, commandname, user, reason, msg.id)

    async def sendlog_noreason(self, ctx, commandname: str, user: discord.Member):
        guild = await self.bot.pool.fetchrow("SELECT * FROM modlog WHERE guildid = $1", ctx.guild.id)
        if guild != None:
            modlog = self.bot.get_channel(guild["channelid"])
            if modlog == None:
                return

            logamounts = guild["logamounts"]
            embed=discord.Embed(title=f"{commandname} | #{logamounts}", color=discord.Color.blurple())
            embed.add_field(name="User", value=f"{user.mention} ({user.name}#{user.discriminator})", inline=False)
            embed.add_field(name="Moderator", value=f"{ctx.author.mention} ({ctx.author.name}#{ctx.author.discriminator})", inline=False)
            embed.add_field(name="Reason", value="This command does not require a reason.", inline=False)
            msg = await modlog.send(embed=embed)
            await self.storecase_noreason(ctx, commandname, user, msg.id)

    async def storecase(self, ctx, casetype: str, user: discord.Member, reason: str, logmsgid: int):
        guild = await self.bot.pool.fetchrow("SELECT * FROM modlog WHERE guildid = $1", ctx.guild.id)
        if guild == []:
            return

        logamounts = guild["logamounts"]
        await self.bot.pool.execute("INSERT INTO modcases VALUES ($1, $2, $3, $4, $5, $6, $7)", ctx.guild.id, logamounts, casetype, user.id, ctx.author.id, reason, logmsgid)

    async def storecase_noreason(self, ctx, casetype: str, user: discord.Member, logmsgid: int):
        guild = await self.bot.pool.fetchrow("SELECT * FROM modlog WHERE guildid = $1", ctx.guild.id)
        if guild == []:
            return

        logamounts = guild["logamounts"]
        await self.bot.pool.execute("INSERT INTO modcases VALUES ($1, $2, $3, $4, $5, $6, $7)", ctx.guild.id, logamounts, casetype, user.id, ctx.author.id, "This command does not require a reason.", logmsgid)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):
        """Bans the specified member."""
        if reason is None:
            r = "No Reason Provided."
        else:
            r = reason

        if ctx.author.id == user.id:
            embed=discord.Embed(title="Error", description="You cannot ban yourself.", color = discord.Color.blurple())
            await ctx.send(embed=embed)
            return

        try:
            await self.uplogamount(ctx)
            await self.sendlog(ctx, "Ban", user, r)
            await user.ban(reason = reason, delete_message_days=0)

            embed=discord.Embed(title="Done!", description=f"{user.mention} has been banned.", color = discord.Color.blurple())
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed=discord.Embed(title="Error", description=f"This user is an administrator or has roles above me. Due to this, I cannot ban this member.", color = discord.Color.blurple())
            await ctx.send(embed=embed)
            return

        try:
            embed=discord.Embed(title=f"Banned ({ctx.guild.name})", description=r, color = discord.Color.blurple())
            await user.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.command()
    @commands.has_permissions(ban_members = True)
    @commands.bot_has_permissions(ban_members = True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        """Kicks the specified member."""
        if reason is None:
            r = "No Reason Provided."
        else:
            r = reason

        if ctx.author.id == user.id:
            embed=discord.Embed(title="Error", description=f"You cannot kick yourself.", color = discord.Color.blurple())
            await ctx.send(embed=embed)
            return

        try:
            await self.uplogamount(ctx)
            await self.sendlog(ctx, "Kick", user, r)
            await user.kick(reason = reason)

            embed=discord.Embed(title="Done!", description=f"{user.mention} has been kicked.", color = discord.Color.blurple())
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed=discord.Embed(title="Error", description=f"This user is an administrator or has roles above. Due to this, I cannot kick this member.", color = discord.Color.blurple())
            await ctx.send(embed=embed)
            return

        try:
            embed=discord.Embed(title=f"Kicked ({ctx.guild.name})", description=r, color = discord.Color.blurple())
            await user.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.command(aliases = ["warning"])
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, user: discord.Member, *, reason: str = None):
        """Warns the specified member."""
        if reason is None:
            r = "No Reason Provided."
        else:
            r = reason
        if user.id == ctx.author.id:
            embed=discord.Embed(title="Error", description="You cannot warn yourself.", color = discord.Color.blurple())
            await ctx.send(embed=embed)
            return
        if user.bot:
            embed=discord.Embed(title="Error", description="You cannot warn bots.", color = discord.Color.blurple())
            await ctx.send(embed=embed)
            return

        await self.uplogamount(ctx)
        await self.sendlog(ctx, "Warn", user, r)
        await self.bot.pool.execute("INSERT INTO warns VALUES ($1, $2, $3, $4, $5)",
        user.id, ctx.guild.id, ctx.author.id, ctx.author.name,
        reason)

        em = discord.Embed(color = discord.Color.blurple())
        em.add_field(name = "Done!", value = f"{user.mention} has been warned.")
        em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = em)

        em = discord.Embed(title=f"Warned ({ctx.guild.name})", description=reason, color = discord.Color.blurple())
        em.timestamp = datetime.datetime.utcnow()
        try:
            await user.send(embed = em)
        except discord.Forbidden:
            pass

    @commands.command(aliases = ["warnings"])
    async def warns(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author

        warns = await self.bot.pool.fetch("SELECT * FROM warns WHERE userid = $1 AND guildid = $2", user.id, ctx.guild.id)

        if warns == []:
            embed=discord.Embed(title = "Error", color = discord.Color.blurple(), description = "This user has not been warned")
            await ctx.send(embed=embed)
            return

        pag = paginator.EmbedPaginator()

        for warning in warns:
            count = await self.bot.pool.fetchval("SELECT COUNT(*) FROM warns WHERE userid = $1 AND guildid = $2", user.id, ctx.guild.id)
            embed=discord.Embed(title= f"{user} has {count} warning(s)")

            moderator = warning["modname"]
            reason = warning["reason"]

            embed.add_field(name = f"Warned by: {moderator}", value = f"For Reason: {reason}")

            pag.add_page(embed)

        interface = Paginator(ctx, pag)
        await interface.send_pages()

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    @commands.bot_has_permissions(manage_guild = True)
    async def deafen(self, ctx, *, user: discord.Member):
        """Deafens the specified member."""
        if user.voice == None:
            embed = discord.Embed(title = "Cannot Deafen", description = "I can only deafen members who are currently in a voice channel.", color = discord.Color.blurple())
            await ctx.send(embed = embed)
            return

        await user.edit(deafen = True)

        done = discord.Embed(title = "Deafened", description = f"{user} has been deafened!", color = discord.Color.blurple())
        await ctx.send(embed = done)
        await self.uplogamount(ctx)
        await self.sendlog_noreason(ctx, "Deafen", user)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    @commands.bot_has_permissions(manage_guild = True)
    async def undeafen(self, ctx, *, user: discord.Member):
        """Undeafens the specified member."""
        if user.voice == None:
            embed = discord.Embed(title = "Cannot Undeafen", description = "I can only undeafen members who are currently in a voice channel.", color = discord.Color.blurple())
            await ctx.send(embed = embed)
            return

        await user.edit(deafen = False)

        done = discord.Embed(title = "Undeafened", description = f"{user} has been undeafened!", color = discord.Color.blurple())
        await ctx.send(embed = done)
        await self.uplogamount(ctx)
        await self.sendlog_noreason(ctx, "Undeafen", user)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def cases(self, ctx, user: discord.Member = None):
        """Shows the amount of cases for the server."""

        modcases = await self.bot.pool.fetch("SELECT * FROM modcases WHERE guildid = $1", ctx.guild.id)
        
        if modcases == []:
            em = discord.Embed(color = discord.Color.blurple())
            em.add_field(name = "Error", value = "No cases have been found.")
            await ctx.send(embed = em)
            return

        pag = paginator.EmbedPaginator()

        for case in modcases:
            casenumber = case["casenumber"]
            casetype = case["casetype"]
            caseuserid = case["caseuserid"]
            casemodid = case["casemodid"]
            casereason = case["casereason"]
            em = discord.Embed(color = discord.Color.blurple())
            em.title = f"Case #{casenumber} | {casetype}"

            caseuser = await self.bot.fetch_user(caseuserid)
            casemod = await self.bot.fetch_user(casemodid)

            em.add_field(name="User", value=f"{caseuser.mention} ({caseuser.name}#{caseuser.discriminator})", inline=False)
            em.add_field(name="Moderator", value=f"{casemod.mention} ({casemod.name}#{casemod.discriminator})", inline=False)
            em.add_field(name="Reason", value=casereason, inline=False)

            pag.add_page(em)

        interface = Paginator(ctx, pag)
        await interface.send_pages()

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def case(self, ctx, caseid: int):
        """Shows information about the specified case."""
        case = await self.bot.pool.fetchrow("SELECT * FROM modcases WHERE guildid = $1 AND casenumber = $2", ctx.guild.id, caseid)

        if case == None:
            em = discord.Embed(color = discord.Color.blurple())
            em.add_field(name = "Error", value = "No case with that id has been found.")
            await ctx.send(embed = em)
            return

        casenumber = case["casenumber"]
        casetype = case["casetype"]
        caseuserid = case["caseuserid"]
        casemodid = case["casemodid"]
        casereason = case["casereason"]
        embed = discord.Embed(title = f"Case #{casenumber} | {casetype}", color = discord.Color.blurple())

        caseuser = await self.bot.fetch_user(caseuserid)
        casemod = await self.bot.fetch_user(casemodid)

        embed.add_field(name = "User", value = f"{caseuser.mention} ({caseuser.name}#{caseuser.discriminator})", inline = False)
        embed.add_field(name = "Moderator", value = f"{casemod.mention} ({casemod.name}#{casemod.discriminator})", inline = False)
        embed.add_field(name = "Reason", value = casereason, inline = False)
        await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def reason(self, ctx, caseid: int, *, reason: str):
        """Edits the reason for the specified case."""
        gcheck = await self.bot.pool.fetchrow("SELECT * FROM modlog WHERE guildid = $1", ctx.guild.id)
        ccheck = await self.bot.pool.fetchrow("SELECT * FROM modcases WHERE guildid = $1 AND casenumber = $2", ctx.guild.id, caseid)

        if gcheck == None:
            await ctx.send("This guild doesn't have a modlog configured yet.")
            return

        modlogchannel = self.bot.get_channel(gcheck["channelid"])

        if modlogchannel == None:
            await ctx.send("This guild's modlog channel is invalid or has been deleted.")
            return

        if ccheck == None:
            embed = discord.Embed(title = "Error", description = "No case with that id has been found.", color = discord.Color.blurple())
            await ctx.send(embed = embed)
            return

        logmsgid = ccheck["logmsgid"]
        logmsg = await modlogchannel.fetch_message(logmsgid)

        if logmsg == None:
            await ctx.send("The log message for the case was most likely deleted as I cannot find it in the modlog.")
            return

        casenumber = ccheck["casenumber"]
        casetype = ccheck["casetype"]
        caseuserid = ccheck["caseuserid"]
        casemodid = ccheck["casemodid"]
        casereason = ccheck["casereason"]

        caseuser = await self.bot.fetch_user(caseuserid)
        casemod = await self.bot.fetch_user(casemodid)

        await self.bot.pool.execute(f"UPDATE modcases SET casereason = $1 WHERE guildid = $2 AND casenumber = $3", reason, ctx.guild.id, caseid)
        embed = discord.Embed(title = f"{casetype} | #{casenumber}", color = discord.Color.blurple())
        embed.add_field(name = "User", value = f"{caseuser.mention} ({caseuser})", inline=False)
        embed.add_field(name = "Moderator", value = f"{casemod.mention} ({casemod})", inline=False)
        embed.add_field(name = "Reason", value = reason, inline=False)
        await logmsg.edit(embed = embed)
        await ctx.send(f"The reason for **Case #{casenumber}** has been set to **{reason}**")

    @commands.command(aliases = ["nick"])
    @commands.has_permissions(manage_nicknames = True)
    @commands.bot_has_permissions(manage_nicknames = True)
    async def nickname(self, ctx, user: discord.Member, *, nick: str = None):
        """Sets the nickname of the specified member."""
        try:
            if nick != None:
                await user.edit(nick = nick[:32])
            else:
                await user.edit(nick = nick)

            embed = discord.Embed(title = "Set Nickname", description = f"{user}'s nickname has been set to {user.display_name}")
            await ctx.send(embed = embed)
        except discord.Forbidden:
            embed = discord.Embed(title = "Error", description = "I couldn't set the users nickname. This is most likely due to Discord's Hierarchy system.", color = discord.Color.blurple())
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_messages = True)
    async def purge(self, ctx, amount: int):
        """Purges the specified amount of messages."""
        try:
            await ctx.channel.purge(limit = amount + 1)
        except discord.Forbidden:
            em = discord.Embed(color = discord.Color.dark_teal())
            em.add_field(name = "Error", value = "I wasn't able to purge the messages.")
            await ctx.send(embed = em)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    @commands.bot_has_permissions(manage_channels = True)
    async def slowmode(self, ctx, delay: int):
        """Sets the slowmode to the specified number."""
        await ctx.channel.edit(slowmode_delay = delay)
        await ctx.send(f"I have set the slowmode for this channel to **{delay} seconds**.")

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def setmodlog(self, ctx, channel: discord.TextChannel):
        """Sets the modlog for the guild."""
        guild = await self.bot.pool.fetchrow("SELECT * FROM modlog WHERE guildid = $1", ctx.guild.id)
        if guild != None:
            await self.bot.pool.execute("UPDATE modlog SET channelid = $1 WHERE guildid = $2", channel.id, ctx.guild.id)
            await ctx.send(f"I have changed this guild's modlog channel to <#{channel.id}>.")
            return

        await self.bot.pool.execute("INSERT INTO modlog VALUES ($1, $2, $3)", ctx.guild.id, channel.id, 0)
        await ctx.send(f"I have set this guild's modlog channel to <#{channel.id}>.")

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        """Sets the log for the guild."""
        guild = await self.bot.pool.fetchrow("SELECT * FROM loggingsettings WHERE guildid = $1", ctx.guild.id)
        if guild != None:
            await self.bot.pool.execute("UPDATE loggingsettings SET channelid = $1 WHERE guildid = $2", channel.id, ctx.guild.id)
            await ctx.send(f"I have changed this guild's logging channel to <#{channel.id}>.")
            return
        
        await self.bot.pool.execute("INSERT INTO loggingsettings VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)", ctx.guild.id, channel.id, True, True, True, True, True, True, True, True, True, True)
        await ctx.send(f"I have set this guild's logging channel to <#{channel.id}>.")

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def mute(self, ctx, user: discord.Member, *, reason: str):
        """Mutes the specified member."""
        if not discord.utils.find(lambda r: "mute" in r.name.lower(), ctx.message.guild.roles):
                if not discord.utils.find(lambda r: "Muted" == r.name, ctx.message.guild.roles):
                    perms = discord.utils.find(lambda r: "@everyone" == r.name, ctx.message.guild.roles).permissions
                    role = await ctx.guild.create_role(name="Muted", permissions=perms)
                    for channel in ctx.guild.text_channels:
                        await channel.set_permissions(role, overwrite=discord.PermissionOverwrite(send_messages=False, add_reactions=False))
                    for channel in ctx.guild.voice_channels:
                        await channel.set_permissions(role, overwrite=discord.PermissionOverwrite(speak=False))
                role = discord.utils.find(lambda r: "Muted" == r.name, ctx.message.guild.roles)
        else:
                role = discord.utils.find(lambda r: "mute" in r.name.lower(), ctx.message.guild.roles)

        if role not in user.roles:
                roles = user.roles
                roles.append(role)
                mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
                await asyncio.sleep(0.5)
                await user.add_roles(mutedrole, reason=f'''Muted By: {ctx.author} for: {reason} ''')

                embed=discord.Embed(title="Done!", description=f"{user} has been muted.", color = discord.Color.blurple())
                await ctx.send(embed=embed)
                await self.uplogamount(ctx)
                await self.sendlog(ctx, "Mute", user, reason)
        else:
                embed=discord.Embed(title="Already Muted", colour=discord.Colour.blurple(), description=f"{user} is already muted!", timestamp=datetime.datetime.utcnow())
                await ctx.send(embed=embed)
                return

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def unmute(self, ctx, user: discord.Member, *, reason: str):
        """Un-mutes the specified member."""
        role = discord.utils.find(lambda r: r.name == 'Muted', ctx.guild.roles)
        if role in user.roles:
                mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
                await user.remove_roles(mutedrole, reason=f'''Unmuted by {ctx.author}''')

                embed=discord.Embed(title="Done!", description=f"{user.mention} has been un-muted.", color = discord.Color.blurple())
                await ctx.send(embed=embed)
                await self.uplogamount(ctx)
                await self.sendlog(ctx, "Unmute", user, reason)
        else:
                embed=discord.Embed(title="Not Muted", colour=discord.Colour.blurple(), description=f'''{user} was never muted!''', timestamp=datetime.datetime.utcnow())
                await ctx.send(embed=embed)
                return

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def addrole(self, ctx, user: discord.Member, *, rolename: str):
        """Adds a role to the specified member."""
        if not discord.utils.find(lambda r: rolename == r.name, ctx.message.guild.roles):
            await ctx.send("I was not able to find that role in this server.")
            return
        else:
            role = discord.utils.find(lambda r: rolename == r.name, ctx.message.guild.roles)
            if role not in user.roles:
                await user.add_roles(role)
                await ctx.send(f"I have given the role **{rolename}** to **{user}**.")
                return
            else:
                await ctx.send(f"That user already has the **{rolename}** role.")
                return

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    @commands.bot_has_permissions(manage_roles = True)
    async def removerole(self, ctx, user: discord.Member, *, rolename: str):
        """Removes a role from the specified member."""
        if not discord.utils.find(lambda r: rolename == r.name, ctx.message.guild.roles):
            await ctx.send("I was not able to find that role in this server.")
            return
        else:
            role = discord.utils.find(lambda r: rolename == r.name, ctx.message.guild.roles)
            if role in user.roles:
                await user.remove_roles(role)
                await ctx.send(f"I have removed the role **{rolename}** from **{user}**.")
                return
            else:
                await ctx.send(f"That user doesn't have the **{rolename}** role.")
                return


def setup(bot):
    bot.add_cog(Moderation(bot))