import discord
from discord.ext import commands
from humanize import naturaldelta
import sys
sys.path.append("../")


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandOnCooldown):
            try:
                self.bot.get_command(ctx.command.name).reset_cooldown(ctx)
            except AttributeError:
                pass

        errors = {
            commands.MissingPermissions: {"msg": "You do not have the correct permissions to run this command.", "ty": "Missing Permissions"},
            commands.NSFWChannelRequired: {"msg": "This command cannot be run in Non-NSFW channels.", "ty": "NSFW Command"},
            commands.BotMissingPermissions: {"msg": "I do not have the correct permissions.", "ty": "Bot Missing Permissions"},
            discord.HTTPException: {"msg": "There was an error contacting Discord.", "ty": "HTTP Exception"},
            commands.CommandInvokeError: {"msg": "An Exception occurred while  running the command.\n[ERROR]", "ty": "Command Error"},
            commands.NotOwner: {"msg": "You aren't the owner of this bot.", "ty": "Low Permissions"},
            commands.BadArgument: {"msg": "A `Bad Argument` Exception occurred.", "ty": "Bad Argument"}
        }

        ex = (commands.MissingRequiredArgument, commands.CommandOnCooldown, commands.CommandNotFound)

        if not isinstance(error, ex):

            ets = errors.get(error.__class__)
            if ets == None:
                ets = {}
                ets["msg"] = "An unexpected error has occurred.\n[ERROR]"
                ets["ty"] = "Unexpected Error"
                                    
            em = discord.Embed(title = ets['ty'], description = ets["msg"].replace("[ERROR]", f"```\n{error}\n```"), color = discord.Color.blurple())
            
            try:
                await ctx.send(embed = em)
            except discord.Forbidden:
                try:
                    await ctx.author.send(embed = em)
                except:
                    pass

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(color = discord.Color.blurple())
            em.add_field(name = "Missing Argument", value = f"""Missing a parameter, `{str(error.param).partition(':')[0]}`.""")
            await ctx.send(embed = em)

        elif isinstance(error, commands.CommandOnCooldown):
            time = naturaldelta(error.retry_after)

            em = discord.Embed(color = discord.Color.blurple())
            em.add_field(name = "Cooldown Active", value = f"Please wait {time} to use `{ctx.command.name}` again.")
            await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))