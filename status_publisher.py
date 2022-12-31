from __future__ import annotations

import datetime
import time
import typing as T

import requests
from discord import Color
from discord_webhook import DiscordEmbed, DiscordWebhook

from database.connect import ManagedSession
from database.health import Health, HealthSchema
from utils import log

DEAD = f"\U0001F494"
ALIVE = f"\U0001F49A"

THUMBNAIL_URL = "https://media.discordapp.net/attachments/986155484237156384/1036099095691022356/bigger__1.jpg?width=549&height=549"


class Publisher:
    DEAD_DELTA_TIME = 60.0 * 60.0 * 60.0

    def __init__(self, server_url: str, discord_url: str, quiet: bool = False) -> None:
        self.quiet = quiet
        self.server_url = server_url
        self.webhook: DiscordWebhook = DiscordWebhook(
            discord_url,
            rate_limit_retry=True,
        )
        self.response: requests.Response | None = None

        self.bots: T.Dict[str, T.Tuple[float, Health]] = dict()

    def delete_message(self) -> None:
        log.print_normal(f"Deleting last post")
        try:
            self.webhook.delete()
        except:
            log.print_fail("Failed to delete post")

    def get_bots(self) -> T.List[Health]:
        url = self.server_url + "/health"
        try:
            response = requests.get(
                url, headers={"accept": "application/json, text/plain, */*"}
            ).json()
        except:  # pylint: disable=bare-except
            log.print_fail(f"Failed request to {url}")
            return []

        bots: T.List[Health] = []
        for bot_json in response.get("result", []):
            schema = HealthSchema()
            bots.append(schema.load(bot_json))

        log.print_ok_arrow(f"Found {len(bots)} bot statuses")
        return bots

    def update_status(self) -> None:
        if self.quiet:
            return

        embed = DiscordEmbed(
            title="P2E Auto Bot Status",
            description="Health monitor for all bots in the P2E Auto ecosystem",
            color=Color.teal().value,  # pylint: disable=attr-defined
        )

        now = datetime.datetime.now()

        bots = self.get_bots()

        if not bots:
            log.print_normal(f"No bots available")
            return

        for bot in bots:
            delta = now - bot["last_ping"]
            is_alive = delta.total_seconds() < self.DEAD_DELTA_TIME
            status = ALIVE if is_alive else DEAD
            message = f"{status*len(bots['users'])}"
            log.print_normal(message)
            embed.add_embed_field(name=bot["name"], value=message, inline=False)

        embed.set_thumbnail(url=THUMBNAIL_URL)

        self.webhook.remove_embeds()
        self.webhook.add_embed(embed=embed)

        try:
            if self.response is None:
                self.response = self.webhook.execute()
            else:
                self.webhook.edit()
        except:  # pylint: disable=bare-except
            log.print_fail("Failed to post embed")
            self.response = None

    def run(self) -> None:
        while True:
            self.update_status()
            time.sleep(30.0)
