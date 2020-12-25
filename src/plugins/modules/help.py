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
import typing

import discord
from discord.ext import commands
from discord.ext import menus
from src.plugins.state.pagination import FieldPageSource, RoboPages

from ... import Plugin

log = logging.getLogger(__name__)



class HelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(command_attrs={"hidden": True})

    def get_command_signature(self, command):
        return "{0.clean_prefix}{1.qualified_name} {1.signature}".format(self, command)

    async def send_bot_help(self, mapping):

        list = []
        for x in self.context.bot.cogs:
            if x in ['Jishaku','Guild','Help']:
                continue
            cog = self.context.bot.get_cog(x)
            list.append((cog.qualified_name,f"{cog.description}\n" + ' '.join([f"`{x.name}`" for x in cog.get_commands()])))

        source = FieldPageSource(list,per_page=8)
        source.embed.colour = discord.Color.blurple()
        try:
            await RoboPages(source).start(self.context)
        except menus.MenuError as e:
            await self.context.send(e)


    async def send_command_help(self, command):

        embed = discord.Embed(color=discord.Color.blurple(),description=command.brief)
        embed.set_author(name=f"{command.qualified_name} {' '.join([f'<{command.clean_params[x].name}>' for x in command.clean_params])}")

        await self.context.send(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

def cog_unload(self):
    self.bot.help_command = self.old_help_command


def setup(bot):
    bot.add_cog(Help(bot))
