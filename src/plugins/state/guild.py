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

from ... import Plugin

log = logging.getLogger(__name__)


class Guild(Plugin):
    @Plugin.listener("on_guild_join")
    async def on_guild_join(self, guild):

        log.info(f"Gained a guild. [{guild} ({guild.id})]")

    @Plugin.listener("on_guild_remove")
    async def on_guild_remove(self, guild):

        log.info(f"Lost a guild. [{guild} ({guild.id})]")
