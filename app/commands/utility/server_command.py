from enum import Enum

from discord import Embed, ApplicationContext
from discord.ext import commands
from providers.modifiers.logger import setup_logger

logger = setup_logger()


class VerificationLevels(Enum):
    NONE = 'No security measures.'
    LOW = 'Verified mail required.'
    MEDIUM = '\n- Verified mail\n- registered for 5+ minutes'
    HIGH = '\n- Verified mail\n- registered for 5+ minutes\n- member for 10+ minutes'
    HIGHEST = 'Verified phone number required.'


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
        features = '\n- `' + '`\n- `'.join(ctx.guild.features) if ctx.guild.features else 'None'
        embed = Embed()
        embed.title = ctx.guild.name
        embed.thumbnail = ctx.guild.icon
        embed.description = f"""
**Owner**: <@{ctx.guild.owner_id}> (ID: `{ctx.guild.owner_id}`)
**Created**: <t:{int(ctx.guild.created_at.timestamp())}:F>
**Guild ID**: `{ctx.guild.id}`

**Members**: {ctx.guild.member_count}
**Security measure(s)**: {VerificationLevels[str(ctx.guild.verification_level).upper()].value}
**Premium tier**: {ctx.guild.premium_tier} with {len(ctx.guild.premium_subscribers)} subscribers

**Features**: {features + '`'}
"""

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(UtilityServer(bot))
