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
from unidecode import unidecode

from ... import Plugin

log = logging.getLogger(__name__)


class Mod(Plugin):
    """
    Moderate your server and keep it clean of annoying people
    """

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):

        if reason is None:
            reason = f"[ Kick by {ctx.author} ] No reason provided."

        await ctx.guild.kick(user, reason=reason)
        await ctx.send("\N{OK HAND SIGN}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):

        if reason is None:
            reason = f"[ Ban by {ctx.author} ] No reason provided."

        await ctx.guild.ban(user, reason=reason)
        await ctx.send("\N{OK HAND SIGN}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.Member, *, reason=None):

        if reason is None:
            reason = f"[ Softban by {ctx.author} ] No reason provided."

        await ctx.guild.ban(user, reason=reason)
        await ctx.guild.unban(user, reason=reason)
        await ctx.send("\N{OK HAND SIGN}")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def multiban(
        self, ctx, users: commands.Greedy[discord.Member], *, reason=None
    ):

        if reason is None:
            reason = f"[ Massban by {ctx.author} ] No reason provided."

        total_users = len(users)
        if len(total_users) > 1:
            return await ctx.send(f"You forgot to add users to ban.")

        failed = 0
        for user in users:
            try:
                await ctx.guild.ban(user, reason=reason)
            except discord.HTTPException:
                failed += 1

        await ctx.send(f"Banned {total_users - failed}/{total_users} users.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def asciffy(self, ctx, *, user: discord.Member):

        nick = unidecode(user.nick) if user.nick else unidecode(user.name)[:32]
        await user.edit(nick=nick)

        await ctx.send(f"Their new name is `{nick}`.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def dehoist(self, ctx, *, user: discord.Member):

        nick = " ឵" + user.nick if user.nick else " ឵" + user.name[:32]
        await user.edit(nick=nick)

        await ctx.send(f"Dehoisted {user}.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def cleanup(self, ctx, amount: int, channel: discord.TextChannel = None):
        def is_me(m):
            return m.author.id == ctx.bot.user.id

        channel = channel or ctx.channel

        await channel.purge(limit=amount, check=is_me)

        await ctx.send(
            f"""Cleaned {amount} of my messages from {"here" if channel == ctx.channel else channel.name}"""
        )
