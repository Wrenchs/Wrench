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
import unicodedata

import discord
import arrow
from discord.ext import commands
from typing import Union

from ... import Plugin, constants

log = logging.getLogger(__name__)


class Meta(Plugin):
    """
    Commands to get information on various things.
    """

    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        """
        Shows you information about a number of characters.
        Only up to 25 characters at a time.
        """

        def to_string(c):
            digit = f"{ord(c):x}"
            name = unicodedata.name(c, "Name not found.")
            return f"`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>"

        msg = "\n".join(map(to_string, characters))
        if len(msg) > 2000:
            return await ctx.send("Output too long to display.")
        await ctx.send(msg)

    @commands.command()
    async def info(self, ctx, *, user: discord.Member = None):
        """
        Get information on a server's member
        """

        user = user or ctx.author
        roles = [
            role.name.replace("@", "@\u200b") for role in getattr(user, "roles", [])
        ]

        embed = discord.Embed(color=user.color)
        embed.set_author(name=user)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(
            name="Joined",
            value=f"{user.joined_at} ({arrow.get(user.joined_at).humanize()})",
            inline=False,
        )
        embed.add_field(
            name="Joined",
            value=f"{user.created_at} ({arrow.get(user.created_at).humanize()})",
            inline=False,
        )
        embed.add_field(
            name="Roles",
            value=", ".join(roles) if len(roles) < 10 else f"{len(roles)} roles",
            inline=False,
        )
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        """
        Get information on your current server
        """

        roles = [
            role.name.replace("@", "@\u200b")
            for role in getattr(ctx.guild, "roles", [])
        ]

        embed = discord.Embed(color=ctx.author.color)
        embed.set_author(name=ctx.guild)
        embed.add_field(
            name="Channels",
            value=f"<:channel:792056134931709952> {len(ctx.guild.text_channels)}\n<:voice:792056122642137090> {len(ctx.guild.voice_channels)}",
            inline=False,
        )
        embed.add_field(
            name="Members",
            value=f"Total: {ctx.guild.member_count}\nBots: {len([x for x in ctx.guild.members if x.bot])}",
            inline=False,
        )
        embed.add_field(
            name="Roles",
            value=", ".join(roles) if len(roles) < 10 else f"{len(roles)} roles",
            inline=False,
        )
        embed.add_field(
            name="Emojis",
            value=f"Regular: {len([x for x in ctx.guild.emojis if not x.animated])}/{ctx.guild.emoji_limit}\nAnimated: {len([x for x in ctx.guild.emojis if x.animated])}/{ctx.guild.emoji_limit}\nTotal: {len(ctx.guild.emojis)}/{ctx.guild.emoji_limit * 2}",
            inline=False,
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member):
        """
        Shows a users avatar in a larger picture
        """

        user = user or ctx.author
        embed = discord.Embed()
        embed.color = user.color
        embed.set_image(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def join(self, ctx, bot:int=791839785857712169):

        permissions = discord.Permissions()
        invite = discord.utils.oauth_url(bot,permissions=permissions)
        await ctx.send(f"<{invite}>")

    @commands.command()
    async def source(self,ctx):

        await ctx.send(constants.GITHUB_REPO)