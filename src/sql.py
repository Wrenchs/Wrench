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


Logging taken from https://github.com/mouseyapp/bot/blob/cheese/src/logging.py
"""

import logging

import asyncpg

log = logging.getLogger(__name__)


async def init_db(db_config, size):

    try:
        pool = await asyncpg.create_pool(**db_config, max_size=size)

        with open("src/schema.sql") as f:
            await pool.execute(f.read())

        return pool
    except Exception as error:
        log.exception(f"Creating pool failed.", exc_info=error)
