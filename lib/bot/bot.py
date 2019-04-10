from discord.ext import commands
from lib import config, logging, errors

import discord

bot_info = config.bot()
bot_token = config.token()

class WegBot(commands.Bot):

    def __init__(self):
        super().__init__(**bot_info)
        self._eligible_roles = config.read_eligible_roles()
        self._eligible_channels = config.read_eligible_channels()
        self._logger = logging.get_logger()

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=f'?help'))
        self.logger.info(f"Ready: {self.user} (ID: {self.user.id})")
    
    def run(self):
        super().run(bot_token, reconnect=True)
    
    @property
    def logger(self):
        return self._logger
    
    @property
    def eligible_channels(self):
        return self._eligible_channels

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

    def find_role_by_name(self, ctx, name):
        results = [role for role in ctx.guild.roles if role.name.lower() == name.lower()]
        return None if len(results) < 1 else results[0]
    
    def get_echo(self, filename):
        return config.read_echo(filename)

    async def give_role(self, ctx, name):
        self.logger.debug(f"Trying to give role '{name}' to {ctx.author} in {ctx.guild}")
        role = self.find_role_by_name(ctx, name)
        if role is None:
            raise errors.RoleNotFoundError(name)
        if not role.name.lower() in self.eligible_roles:
            raise errors.IneligibleRoleError(role)
        add_reason = f"Role '{role.name}' requested by {ctx.author}"
        await ctx.author.add_roles(role, reason=add_reason)

    async def give_all_roles(self, ctx):
        roles = [self.find_role_by_name(ctx, name) for name in self.eligible_roles]
        for role in roles:
            if role is None:
                raise errors.RoleNotFoundError("unknown")
        add_reason = f"All roles requested by {ctx.author}"
        await ctx.author.add_roles(*roles, reason=add_reason)

    async def remove_role(self, ctx, name):
        role = self.find_role_by_name(ctx, name)
        if role is None:
            raise errors.RoleNotFoundError(name)
        if not role.name.lower() in self.eligible_roles:
            raise errors.IneligibleRoleError(role)
        rem_reason = f"Role '{role.name}' requested to be removed by {ctx.author}"
        await ctx.author.remove_roles(role, reason=rem_reason)
