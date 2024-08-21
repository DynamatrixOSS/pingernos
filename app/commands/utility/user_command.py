import discord
from discord import Embed, ApplicationContext, option, Member
from discord.ext import commands
from providers.modifiers.logger import setup_logger

logger = setup_logger()

class UtilityUser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(integration_types={
        discord.IntegrationType.guild_install,
        discord.IntegrationType.user_install,
    },)
    @option("user", Member, description="The user to display information of", default=None)
    async def user(self, ctx: ApplicationContext, user: Member = None):
        """
        Displays information about a user
        :param user:
        :param ctx:
        :return:
        """
        user = ctx.author if user is None else user

        embed = Embed()
        embed.set_author(name=user.name)
        embed.thumbnail = user.avatar.url
        embed.colour = user.color
        user_in_guild = hasattr(user, 'joined_at')
        embed.description = await t(ctx, 'User information' if user_in_guild else 'User information without join date', [user.id, f'<t:{int(user.created_at.timestamp())}>', f'{ f"<t:{int(user.joined_at.timestamp())}>" if user_in_guild else None}'])

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(UtilityUser(bot))
