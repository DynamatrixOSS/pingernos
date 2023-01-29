class Utils:
    @staticmethod #This is a static method, you can call it without creating an instance of the class, but does not have access to the class or its attributes (self)
    def removeColorsFromString(text):
        import re
        text = re.sub(r"§[0-9a-r]", "", text)
        return text
    class Colors:
        blue = 0xadd8e6
        red = 0xf04747
        green = 0x90ee90
        orange = 0xfaa61a