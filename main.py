from lib import bot as wegbot
import discord

bot = wegbot.WegBot()

OK_EMOJI_CODE = u"\u2705"
NO_EMOJI_CODE = u"\u274C"

_newline = '\n'
role_description = f"""Request a role by name.

Roles that can be requested are:
- {(_newline + '- ').join(bot.eligible_roles)}
"""

@bot.command(usage='<role>', description=role_description)
async def role(ctx, *, role: str):
    """ Request a role by name. """
    print(f"{ctx.author} wants a role called {role}")
    async with ctx.typing():
        role_to_add = None

        for this_role in ctx.guild.roles:
            if this_role.name.lower() == role.lower():
                role_to_add = this_role
        
        if role_to_add is None:
            print(f"Role '{role}' does not exist in this guild.")
            await ctx.message.add_reaction(NO_EMOJI_CODE)
            await ctx.send(f"I don't see a role with the name '{role}', {ctx.author.mention}.")
            return
        
        eligible_roles = [role for role in ctx.guild.roles if role.name.lower() in bot.eligible_roles]
        if not role_to_add.name.lower() in eligible_roles:
            print(f"{ctx.author} requested ineligible role '{role_to_add.name}'")
            await ctx.message.add_reaction(NO_EMOJI_CODE)
            await ctx.send(f"The role `{role_to_add.name}` is not eligible to be requested, {ctx.author.mention}.")
            return
        
        add_reason = f"Role '{role}' requested by {ctx.author}"
        await ctx.author.add_roles(role_to_add, reason=add_reason)

        await ctx.message.add_reaction(OK_EMOJI_CODE)
        await ctx.send(f"Gave the role `{role_to_add.name}` to {ctx.author.mention}")

        print(f"Successfully gave role {role_to_add.name} to {ctx.author}")

@role.error
async def role_error(ctx, err):
    """ ?role broke something... """
    await ctx.message.add_reaction(NO_EMOJI_CODE)

    # 403 Forbidden
    if isinstance(err, discord.errors.Forbidden) or isinstance(err, discord.ext.commands.BotMissingPermissions):
        await ctx.send(f"I don't have permission to do that, {ctx.author.mention}. Go bug Weg about it.")
        return
    
    # unknown error
    await ctx.send("Error! I just broke; that's all I know. Please send Weg.")
    print(err)

if __name__ == "__main__":
    bot.run()
