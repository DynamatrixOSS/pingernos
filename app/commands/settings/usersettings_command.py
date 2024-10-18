import os

import discord
from discord import Embed, ApplicationContext, option
from discord.ext import commands

import database.executioners.database as db
from app.controllers.user import User
from providers.modifiers.logger import setup_logger

logger = setup_logger()


class UserSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    usersettings = discord.SlashCommandGroup(name="usersettings", integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    })

    @usersettings.command()
    async def view(self, ctx: ApplicationContext):
        """ Displays information about your user settings """
        embed = Embed()
        user_settings = await User().get_user(ctx.author)
        embed.set_author(name=ctx.author.name)
        embed.thumbnail = ctx.author.avatar.url
        embed.colour = ctx.author.color
        embed.description = '\n'.join(
            [f"**{key.replace('_', ' ').title()}**: {value}" for key, value in user_settings.items()])

        await ctx.respond(embed=embed)

    @usersettings.command()
    @option("setting", description="The setting you want to modify", choices=["language", "name"])
    @option("value", description="The new value of the setting, leave empty to reset it", required=False)
    async def modify(self, ctx: ApplicationContext, setting: str, value: str):
        """ Modify or reset one of your user settings """
        match setting:
            case "language":
                # Read available languages from translations/ folder
                lang_path = 'translations/'
                translations = [name for name in os.listdir(lang_path) if os.path.isdir(os.path.join(lang_path, name))]

                value = value or "en"
                if value not in translations:
                    return await ctx.respond(
                        f"Invalid language! Available options are: {', '.join([f'`{lang}`' for lang in translations])}",
                        ephemeral=True
                    )
                await db.execute("UPDATE user_settings SET language = %s WHERE user_id = %s", (value, ctx.author.id))
                await ctx.respond(f"Your language has been updated to `{value}`!", ephemeral=True)
            case "name":
                value = value or ctx.author.global_name
                if len(value) > 32:
                    return await ctx.respond("Your chosen name is too long! It can only be 32 characters long!",
                                             ephemeral=True)
                await db.execute("UPDATE user_settings SET name = %s WHERE user_id = %s", (value, ctx.author.id))
                await ctx.respond(f"Your name has been updated to `{value}`!", ephemeral=True)


def setup(bot):
    bot.add_cog(UserSettings(bot))
