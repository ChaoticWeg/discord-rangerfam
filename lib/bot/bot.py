from discord.ext import commands
from lib import config

import discord

bot_info = config.bot()
bot_token = config.token()

class WegBot(commands.Bot):

    def __init__(self):
        super().__init__(**bot_info)
        self._eligible_roles = config.read_eligible_roles()

    async def on_ready(self):
        print(f"Ready: {self.user} (ID: {self.user.id})")
    
    def run(self):
        super().run(bot_token, reconnect=True)

    @property
    def eligible_roles(self):
        return self._eligible_roles

    @eligible_roles.setter
    def eligible_roles(self, value):
        self._eligible_roles = value
        config.write_eligible_roles(self._eligible_roles)
    
    def add_eligible_role(self, name):
        prev_roles = [role for role in self._eligible_roles]
        prev_roles.append(name)
        self.eligible_roles = prev_roles
    
    def remove_eligible_role(self, name):
        prev_roles = [role for role in self._eligible_roles if not role.lower() == name.lower()]
        self.eligible_roles = prev_roles
