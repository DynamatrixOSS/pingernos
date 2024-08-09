from os import walk
from json import load

from discord import ApplicationContext

from database.executioners.database import execute
from providers.modifiers.logger import setup_logger

logger = setup_logger()


class Translation:


    @staticmethod
    def _get_translation_map() -> dict:
        """You shouldn't have to use this unless your debugging."""
        translation_map = {}
        for dirname, _, filenames in walk("./translations/"):
            if dirname == "./translations/":
                continue
            filename = filenames[0] # There should be only 1
            with open (f"{dirname}/{filename}", "r", encoding="UTF-8") as f:
                json_data = load(f)
                translation_map[dirname.removeprefix("./translations/")] = json_data
        return translation_map

    async def t(self, ctx: ApplicationContext, message_code: str, parameters: list = None) -> str:
        translation_map = self._get_translation_map()
        guild_setting = next(iter((await execute('SELECT language FROM guild_settings WHERE guild_id = %s', ctx.guild.id))[0]))
        logger.warning(guild_setting)

        try:
            return (translation_map[guild_setting][message_code]).format(*parameters) if parameters else translation_map[guild_setting][message_code]
        except KeyError:
            try:
                return translation_map["en"][message_code].format(*parameters) if parameters else translation_map["en"][message_code]  # Default to US
            except KeyError:
                return "No message available for this given message code"
