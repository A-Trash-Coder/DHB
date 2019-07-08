import discord
import traceback
from discord.ext import commands
import asyncpg
import asyncio
from contextlib import redirect_stdout
import textwrap
import io
import traceback
import re
import datetime
import inspect
import sys
import os
import platform
import psutil
sys.path.append("../")


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkmark = "<:dhb_tickyes:587468735187779595>"
        self.x = "<:dhb_tickno:592046559131074570>"

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts down the bot."""
        await ctx.message.delete()
        await self.bot.logout()

    @commands.command(name = "eval")
    @commands.guild_only()
    @commands.is_owner()
    async def _eval(self, ctx, *, body):
        """Evaluates python code."""
        env = {
            'ctx': ctx,
            'bot': self.bot,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource
        }

        def cleanup_code(content):
            """Automatically removes code blocks from the code."""
            # remove ```py\n```
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])

            # remove `foo`
            return content.strip('` \n')

        def get_syntax_error(e):
            if e.text is None:
                return f'```py\n{e.__class__.__name__}: {e}\n```'
            return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Simple generator that paginates text.'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text)-1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:

                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('✅')  # tick
        elif err:
            await ctx.message.add_reaction('❌')  # x
        else:
            await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def load(self, ctx, name: str):
        """Attempts to load the specified cog."""
        try:
            self.bot.load_extension("cogs." + name)
        except Exception as e:
            embed=discord.Embed(colour=discord.Color.red(), description=f"Error:  {type(e).__name__} - {e} {self.x}")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(colour=discord.Color.green(), description=f"Successfully loaded {name} {self.checkmark}")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def update(self, ctx):
        """Pulls from Github and reloads the updated cogs."""
        await ctx.channel.trigger_typing()
        pro = await asyncio.create_subprocess_exec(
            "git", "pull",
            stdout = asyncio.subprocess.PIPE,
            stderr = asyncio.subprocess.PIPE
        )

        try:
            com = await asyncio.wait_for(pro.communicate(), timeout = 10)
            com = com[0].decode() + "\n" + com[1].decode()
        except asyncio.TimeoutError:
            embed=discord.Embed(title="Error", description=f"Took too long to respond.", color=discord.Color.blurple())
            return

        reg = r"(.*?)\.py"
        found = re.findall(reg, com)

        if found:
            updated = []
            final_string = ""

            for x in found:
                extension = re.sub(r"\s+", "", x)
                extension = extension.replace("/", ".")

                try:
                    self.bot.reload_extension(extension)
                except ModuleNotFoundError:
                    continue
                except Exception as error:
                    if inspect.getfile(self.bot.__class__).replace(".py", "") in extension:
                        continue
                    else:
                        embed=discord.Embed(title="Error", description=f"```\n{error}\n```", color=discord.Color.blurple())
                        await ctx.send(embed=embed, delete_after = 5)
                        continue

                updated.append(extension)

            for b in updated:
                final_string += f"`{b}` "

            if updated == []:
                embed=discord.Embed(title=f"No cogs were updated {self.x}.", color=discord.Color.blurple())
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title=f"Updated Cogs: {final_string} {self.checkmark}", color=discord.Color.blurple())
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f"No cogs were updated {self.x}.", color=discord.Color.blurple())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Owner(bot))