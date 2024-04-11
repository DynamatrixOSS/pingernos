import re


def check_ip(server: str) -> str | bool:
    if not server.endswith('.aternos.me'):
        server += '.aternos.me'
    regex = re.compile(r"\w+\.aternos\.me")
    matcher = re.findall(regex, server)
    if not matcher:
        return False
    return matcher[0]
