from config.app import Settings

from discord import Embed, Color, ButtonStyle, ApplicationContext
from discord.ext import commands
from discord.ui import Button, View

from providers.modifiers.logger import setup_logger

logger = setup_logger()

class Source(View):  # Create a class that subclasses discord.ui.View
    def __init__(self):
        settings = Settings()
        super().__init__()
        # Add a URL button to the view
        self.add_item(Button(
            label="Source",
            style=ButtonStyle.link,
            emoji="<github:1271230731691229265>",
            url=settings.get_setting('github')
        ))
        self.add_item(Button(
            label="Support",
            style=ButtonStyle.link,
            emoji="<:discord:1271235054697189376>",
            url=settings.get_setting('discord')
        ))
        self.add_item(Button(
            label="Privacy",
            style=ButtonStyle.link,
            emoji="<:data:1271237825467121796>",
            url=settings.get_setting('privacy')
        ))
        self.add_item(Button(
            label="Invite",
            style=ButtonStyle.link,
            emoji="<:invite:1271238312077561917>",
            url=settings.get_setting('invite')
        ))


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def info(self, ctx: ApplicationContext):
        """
        Displays information about the bot.
        :param ctx:
        :return:
        """
        information_embed = Embed()
        information_embed.colour = Color.purple()
        information_embed.set_author(
            name='Dynamatrix OSS by Dynamatrix',
            icon_url=self.bot.user.avatar.url
        )
        information_embed.description = f"""
{self.bot.user.mention} is a bot developed by Dynamatrix OSS, an open-source team managed by the Dynamatrix company.

The main goal of {self.bot.user.display_name} is to provide users with a convenient multi-module bot that can integrate a dozen bots into a single one along with easy managing through the web dashboard.

As such, this bot currently offers:

>> Currency
>> Utility
>> Moderation
>> Levelling
>> Verification
"""
        await ctx.respond(embed=information_embed, view=Source(), ephemeral=True)


def setup(bot):
    bot.add_cog(Info(bot))
