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

import logging

import discord
from discord.ext import commands

from ... import Plugin

log = logging.getLogger(__name__)

class Admin(Plugin):

    @commands.command(name="purge",brief="Remove messages from a channel in your server.")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _purge(self,ctx,amount:int=None):
        
        def is_pinned(m):
            return not m.pinned
        try:
            purged = await ctx.channel.purge(limit=amount + 1, check=is_pinned)
        except Exception as error:
            log.exception(f"There was an error in \"{ctx.command}\" command.",exc_info=error)

        await ctx.send(f"I have purged **{len(purged)}** messages!")