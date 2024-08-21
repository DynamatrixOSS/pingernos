from discord import Embed, Color, ButtonStyle, ApplicationContext
from discord.ext import commands
from discord.ui import Button, View
from config.app import Settings
from providers.modifiers.logger import setup_logger

logger = setup_logger()

class Source(View):  # Create a class that subclasses discord.ui.View
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.ctx = None  # Initialize ctx as None

    async def add_buttons(self):
        # Add a URL button to the view
        self.add_item(Button(
            label=await t(self.ctx, 'Source'),
            style=ButtonStyle.link,
            emoji="<github:1271230731691229265>",
            url=self.settings.get_setting('github')
        ))
        self.add_item(Button(
            label=await t(self.ctx, 'Support'),
            style=ButtonStyle.link,
            emoji="<:discord:1271235054697189376>",
            url=self.settings.get_setting('discord')
        ))
        self.add_item(Button(
            label=await t(self.ctx, 'Privacy'),
            style=ButtonStyle.link,
            emoji="<:data:1271237825467121796>",
            url=self.settings.get_setting('privacy')
        ))
        self.add_item(Button(
            label=await t(self.ctx, 'Invite'),
            style=ButtonStyle.link,
            emoji="<:invite:1271238312077561917>",
            url=self.settings.get_setting('invite')
        ))
        return self  # Return self to use this View in ctx.respond()


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def info(self, ctx: ApplicationContext):
        """
        Displays information about the bot.
        :param ctx:
        :return:
        """
        source = Source()
        source.ctx = ctx

        information_embed = Embed()
        information_embed.colour = Color.purple()
        information_embed.set_author(
            name=await t(ctx, 'Dynamatrix OSS by Dynamatrix'),
            icon_url=self.bot.user.avatar.url
        )
        information_embed.set_footer(text=await t(ctx, 'Response time', [round(self.bot.latency * 1000)]))
        information_embed.description = await t(
            ctx,
            'is a bot developed by Dynamatrix OSS',
            [self.bot.user.mention, self.bot.user.display_name]
        )

        await ctx.respond(embed=information_embed, view=await source.add_buttons(), ephemeral=True)


def setup(bot):
    bot.add_cog(BotInfo(bot))
