import discord
from discord import Embed, ApplicationContext, option, Member
from discord.ext import commands

from app.controllers.user import User
from providers.modifiers.logger import setup_logger

logger = setup_logger()

class userSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },)
    @option("user", Member, description="The user to display information of", default=None)
    async def user_settings(self, ctx: ApplicationContext):
        """
        Displays information about a user
        :param user:
        :param ctx:
        :return:
        """

        embed = Embed()
        user_settings = await User().get_user(ctx.author)
        embed.set_author(name=ctx.author.name)
        embed.thumbnail = ctx.author.avatar.url
        embed.colour = ctx.author.color
        embed.description = '\n'.join([f"**{key.replace('_', ' ').title()}**: {value}" for key, value in user_settings.items()])

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(userSettings(bot))
