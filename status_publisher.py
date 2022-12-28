import time

import discord_notify


class Publisher:
    def __init__(self, discord: discord_notify.Notifier, quiet: bool = False) -> None:
        self.num_bots = 0
        self.discord = discord
        self.quiet = quiet

    def send_message(self, message: str) -> None:
        if self.quiet:
            return
        self.discord.send(message)

    def run(self) -> None:
        while True:
            print("ping")
            time.sleep(30.0)
