# -> Discord
import discord
from discord import Game
from discord.ext import commands
import logging
# -> Configuration
import config
# -> Loop
import sys
import asyncio
import os
# -> Miscellaneous
from jishaku import help_command
import random
# -> Database
import asyncpg

import datetime

# Just incase the host is windows.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

extensions = ["jishaku"]

for f in os.listdir("cogs"):
    if f.endswith(".py") and not f"cogs.{f[:-3]}" in extensions:
        extensions.append("cogs." + f[:-3])

class DHB(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix = "/",
            case_insensitive = True,
            max_messages = 500,
            fetch_offline_members = False,
            reconnect = True
        )
        self.pool = None
        self.owners = [485915627530485760, 293800689266851850]

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = datetime.datetime.utcnow()

            print(f"{self.user} is ready")
            print('Ready For Commands!')
            print(" ")
            options = ('help via /help', 'Discord Hack Week!')
            while True:
                await self.change_presence(activity=discord.Game(name=random.choice(options)))
                await asyncio.sleep(10)

    async def is_owner(self, user):
        return user.id in self.owners

    async def on_connect(self):
        self.help_command = help_command.MinimalEmbedPaginatorHelp()

        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception as error:
                print(f"There was a problem loading the {extension} extension.")
                print(f"\n{error}")

        pool_creds = {
            "user": config.dbuser,
            "password": config.dbuserpasswd,
            "port": 5432,
            "host": config.dbhost,
            "database": "dhb"
        }

        self.pool = await asyncpg.create_pool(**pool_creds)

        with open("schema.sql", "r") as schema:
            await self.pool.execute(schema.read())

    async def start(self):
        await self.login(config.token) # pylint: disable=no-member
        try:
            await self.connect()
        except KeyboardInterrupt:
            await self.stop()

    async def stop(self):
        await super().logout()

    def run(self):
        loop = self.loop
        try:
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            loop.run_until_complete(self.stop())


if __name__ == "__main__":
    DHB().run()
