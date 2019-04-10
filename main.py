from lib import bot as wegbot, errors as wegbot_errors
import discord

bot = wegbot.WegBot()

OK_EMOJI_CODE = u"\u2705"
NO_EMOJI_CODE = u"\u274C"
_newline = '\n'

addrole_description = f"""Roles that can be requested are:
- {(_newline + '- ').join(bot.eligible_roles)}
"""

@bot.command(usage='<role>', description=addrole_description)
async def addrole(ctx, *, role: str):
    """ Request a role by name, or request ALL. """

    # must be in eligible text channel
    if not ctx.message.channel.id in bot.eligible_channels:
        return
    
    logger = bot.logger

    logger.info(f"{ctx.author} in guild '{ctx.guild}' wants a role called {role}")
    async with ctx.typing():
        if role.lower() == 'all':
            await bot.give_all_roles(ctx)
            await ctx.send(f"Gave all roles to {ctx.author.mention}. Probably.")
        else:
            await bot.give_role(ctx, role)
            role_to_add = bot.find_role_by_name(ctx, role)
            await ctx.send(f"Gave the role `{role_to_add.name}` to {ctx.author.mention}")
            logger.info(f"Successfully gave role {role_to_add.name} to {ctx.author}")
        
        await ctx.message.add_reaction(OK_EMOJI_CODE)


@addrole.error
async def addrole_error(ctx, err):
    """ ?addrole broke something... """
    await ctx.message.add_reaction(NO_EMOJI_CODE)

    # role does not exist
    if isinstance(err, wegbot_errors.RoleNotFoundError):
        bot.logger.info(f"Role '{err.role_name}' does not exist")
        await ctx.send(f"There's no role here called '{err.role_name}', {ctx.author.mention}.")
        return
    
    # role is ineligible
    if isinstance(err, wegbot_errors.IneligibleRoleError):
        bot.logger.warn(f"{ctx.author.mention} requested ineligible role '{err.role.name}' in {ctx.guild}")
        await ctx.send(f"`{err.role.name}` can't be requested, {ctx.author.mention}.")
        return

    # permission errors
    permission_errors = [discord.errors.Forbidden, discord.ext.commands.BotMissingPermissions, discord.ext.commands.MissingPermissions]
    for perm_error in permission_errors:
        if isinstance(err, perm_error):
            bot.logger.warn(f"Permission error attempting to give a role to {ctx.author} in guild '{ctx.guild}'")
            await ctx.send(f"I don't have permission to do that, {ctx.author.mention}. Go bug Weg about it.")
            return
    
    # unknown error
    await ctx.send("Error! I just broke; that's all I know. Please send Weg.")
    bot.logger.error(err)

removerole_description = f"""Roles that can be requested are:
- {(_newline + '- ').join(bot.eligible_roles)}
"""

@bot.command(usage='<role>', description=removerole_description)
async def removerole(ctx, *, role: str):
    """ Remove a role by name. """

    # must be in eligible text channel
    if not ctx.message.channel.id in bot.eligible_channels:
        return
    
    logger = bot.logger

    logger.info(f"{ctx.author} in guild '{ctx.guild}' wants to remove a role called {role}")
    async with ctx.typing():
        if role.lower() == 'all':
            await ctx.message.add_reaction(NO_EMOJI_CODE)
            await ctx.send(f"Can't request to have all roles removed, {ctx.author.mention}.")
            return
        await bot.remove_role(ctx, role.lower())
        await ctx.message.add_reaction(OK_EMOJI_CODE)
        role_to_add = bot.find_role_by_name(ctx, role)
        await ctx.send(f"Removed the role `{role_to_add.name}` from {ctx.author.mention}")

@removerole.error
async def removerole_error(ctx, err):
    await ctx.message.add_reaction(NO_EMOJI_CODE)
    await ctx.send(f"You can't remove that role, {ctx.author.mention}.")
    logger.info("can't remove that role")

if __name__ == "__main__":
    bot.run()
