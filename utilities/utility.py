import re
import discord


def check_ip(server: str) -> str:
    if not server.endswith('.aternos.me'):
        server += '.aternos.me'
    regEx = re.compile(r"\w+\.aternos\.me")
    matcher = re.findall(regEx, server)
    if not matcher:
        return False
    else:
        return matcher[0]
