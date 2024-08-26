from enum import Enum

from discord import Embed, ApplicationContext
from discord.ext import commands
from providers.modifiers.logger import setup_logger

logger = setup_logger()


async def get_verification_levels(ctx):
    return {
        'NONE': await t('None', ctx),
        'LOW': await t('server_security_low', ctx),
        'MEDIUM': await t('server_security_medium', ctx),
        'HIGH': await t('server_security_high', ctx),
        'HIGHEST': await t('server_security_highest', ctx)
    }


class UtilityServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def server(self, ctx: ApplicationContext):
        """
        Displays information about this server
        :param ctx:
        :return:
        """
        features = '\n- `' + '`\n- `'.join(ctx.guild.features) + '`' if ctx.guild.features else await t('None', ctx)
        verification_levels = await get_verification_levels(ctx)
        embed = Embed()
        embed.title = ctx.guild.name
        embed.thumbnail = ctx.guild.icon.url if ctx.guild.icon else 'https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg'
        embed.image = ctx.guild.banner.url if ctx.guild.banner else ''
        embed.description = await t(
            'server_info',
            ctx,
            [
                ctx.guild.owner_id,
                ctx.guild.owner_id,
                int(ctx.guild.created_at.timestamp()),
                ctx.guild.id,
                ctx.guild.member_count,
                verification_levels[str(ctx.guild.verification_level).upper()],
                ctx.guild.premium_tier,
                len(ctx.guild.premium_subscribers),
                features
            ]
        )

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(UtilityServer(bot))
