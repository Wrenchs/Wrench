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
from unidecode import unidecode
from src.plugins.state.pagination import FieldPageSource, RoboPages

from ... import Plugin

log = logging.getLogger(__name__)


class Admin(Plugin):
    """
    Management commands to help managing a server.
    """

    @commands.command(
        name="purge", brief="Remove messages from a channel in your server."
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _purge(self, ctx, amount: int = None):
        def is_pinned(m):
            return not m.pinned

        try:
            purged = await ctx.channel.purge(limit=amount + 1, check=is_pinned)
        except Exception as error:
            log.exception(
                f'There was an error in "{ctx.command}" command.', exc_info=error
            )

        await ctx.send(f"I have purged **{len(purged)}** messages!")

    @commands.command(
        name="vckick",
        brief="Clear a voice channel or kick a user from a voice channel.",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def _vckick(
        self,
        ctx,
        to_kick: typing.Union[discord.Member, discord.VoiceChannel],
        *,
        reason: str = None,
    ):

        if type(to_kick) == discord.Member and to_kick.voice.channel:
            try:
                await to_kick.move_to(channel=None, reason=f"[{ctx.author}] {reason}")
            except Exception as error:
                log.exception(
                    f'There was an error in "{ctx.command}" command.', exc_info=error
                )

        elif type(to_kick) == discord.VoiceChannel and to_kick.members:
            try:
                voicekick = ""
                count = 0
                for x in to_kick.members:
                    await x.move_to(channel=None, reason=f"[{ctx.author}] {reason}")
                    if count >= 5:
                        await ctx.send(voicekick)
                        voicekick = ""
                    else:
                        voicekick += f"Voicekicked {x}\n"
                        count += 1
                    await ctx.send(voicekick)
            except Exception as error:
                log.exception(
                    f'There was an error in "{ctx.command}" command.', exc_info=error
                )

    @commands.group(
        name="noroles",
        brief="Manage users with no roles in your server.",
        invoke_without_command=True,
    )
    @commands.has_permissions(manage_roles=True, kick_members=True)
    @commands.bot_has_permissions(manage_roles=True, kick_members=True)
    async def _noroles(self, ctx):

        await ctx.send(
            f"**{ctx.prefix}noroles [prune|purge|remove] <reason>**\n**{ctx.prefix}noroles [show|list]**"
        )

    @_noroles.command(
        name="prune",
        brief="Kick all users without roles in your server.",
        aliases=["purge", "remove"],
    )
    @commands.has_permissions(manage_roles=True, kick_members=True)
    @commands.bot_has_permissions(manage_roles=True, kick_members=True)
    async def _noroles_prune(self, ctx, *, reason: str = None):

        members_to_kick = [
            x for x in ctx.guild.members if x.roles == [ctx.guild.default_role]
        ]
        for x in members_to_kick:
            try:
                await x.kick(reason=f"[{ctx.author}] {reason}")
            except Exception as error:
                logging.exception("Error", exc_info=error)

        await ctx.send(f"Kicked **{len(members_to_kick)}** members with no roles.")

    @_noroles.command(
        name="list",
        brief="List all users in your server with no roles.",
        aliases=["show"],
    )
    @commands.has_permissions(manage_roles=True, kick_members=True)
    @commands.bot_has_permissions(manage_roles=True, kick_members=True)
    async def _noroles_list(self, ctx):

        await ctx.send("Not yet!")

    @commands.command(name="nick", brief="Set a user's name, can be useful sometimes.")
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def _nickname(self, ctx, user: discord.Member, *, nick: str):

        if len(nick) > 32:
            await ctx.send(
                "Not allowed. Make sure the new nickname is under **32** characters!"
            )

        try:
            await user.edit(nick=nick)
        except Exception as error:
            logging.exception("Error", exc_info=error)

        await ctx.send(f"Set {user}'s nickname to `{nick}`")

    @commands.command(
        name="asciify", brief='Change someone\'s super bad name to a "norma" name.'
    )
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def _asciify(
        self, ctx, user: discord.Member,
    ):

        try:
            nick = unidecode(user.nick) if user.nick else unidecode(user.name)[:32]
            await user.edit(nick=nick)
        except Exception as error:
            logging.exception("Error", exc_info=error)

        await ctx.send(f"Asciified {user}'s nickname to `{nick}`")

    @commands.command(
        name="dehoist",
        brief="Dehoist a user it will add a character moving them to the bottom.",
    )
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def _dehoist(self, ctx, user: discord.Member):

        try:
            nick = " ឵" + user.nick if user.nick else " ឵" + user.name[:32]
            await user.edit(nick=nick)
        except Exception as error:
            logging.exception("Error", exc_info=error)

        await ctx.send(f"Dehoisted {user}!")

    @commands.command(
        name="clearr",
        brief="Remove a message's reactions. ALl of them.",
        aliases=["clearreactions", "removereactions", "cleare", "clearemojis"],
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _clearr(self, ctx, message: discord.Message):
        emojis = {}

        try:
            for x in message.reactions:
                emojis[x.emoji] = x.count
            await message.clear_reactions()
        except Exception as error:
            logging.exception("Error", exc_info=error)

        await ctx.send(
            f"Cleared reactions on {message.id}.\n\n{' ,'.join([f'{x}: {emojis[x]}' for x in emojis])}"
        )

    @commands.group(
        name="slowmode",
        brief="Set a channel's slowmode, or remove it completely.",
        invoke_without_command=True,
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def _slowmode(self, ctx, time, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        seconds_per_unit = {"s": 1, "m": 60, "h": 3600}

        def convert_to_seconds(s):
            return int(s[:-1]) * seconds_per_unit[s[-1]]

        if convert_to_seconds(time) > 21600:
            return await ctx.send("Time may not be over **6 hours**")

        try:
            await channel.edit(slowmode_delay=convert_to_seconds(time))
        except Exception as error:
            logging.exception("Error", exc_info=error)

        await ctx.send(f"Set slowmode for {channel.mention} to {time}")

    @_slowmode.command(name="disable", brief="Disable slowmode on a channel")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def _slowmode_disable(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        try:
            await channel.edit(slowmode_delay=None)
        except Exception as error:
            logging.exception("Error", exc_info=error)

        await ctx.send(f"Disabled slowmode in {channel.mention}")