"""
Copyright 2020 ibx34

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pathlib

import aiohttp
import discord
from discord.ext import commands

from .config import config
from .sql import init_db


config = config()


def get_extensions():

    if config.get("plugins"):
        return config["plugins"]

    found = ["jishaku"]
    base = pathlib.Path("./src/plugins")

    for path in base.glob("*/__init__.py"):
        found.append(str(path.parent).replace("\\", "."))

    return found


def mentions():

    return discord.AllowedMentions(everyone=False, roles=False, users=False)


def intents():

    needed = [
        "messages",
        "guilds",
        "members",
        "guild_messages",
        "reactions",
        "dm_messages",
        "dm_reactions",
        "voice_states",
        "presences",
    ]

    intents = discord.Intents.none()

    for name in needed:
        setattr(intents, name, True)

    return intents


async def get_pre(wrenchboat, message):

    try:
        return commands.when_mentioned_or(*config["prefixes"])(wrenchboat, message)
    except:
        pass


def start_session(wrenchboat):

    return aiohttp.ClientSession(loop=wrenchboat.loop)


class Wrenchboat(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_pre,
            case_insensitive=True,
            description="an easy to use bot for managing servers of any size.\n:warning: Errors are meant to be like that and im not being lazy :)",
            reconnect=True,
            status=discord.Status.online,
            activity=discord.Game("with my wrench"),
            intents=intents(),
            allowed_mentions=mentions(),
            shard_id=0,
            shard_count=1,
        )

        self.pool = None
        self.session = None
        self.redis = None
        self.config = config

    async def start(self):
        self.session = start_session(self)
        self.pool = await init_db(db_config=config['db_config'],size=150)

        for name in get_extensions():
            self.load_extension(name)

        await super().start(config["token"])

    async def process_commands(self, message):

        ctx = await self.get_context(message, cls=commands.Context)
        if ctx.command is None:
            return

        await self.invoke(ctx)


if __name__ == "__main__":
    Wrenchboat().run()
