from os import walk
from json import load
class Translation:
    def _get_translation_map() -> dict:
        "You shouldn't have to use this unless your debugging."
        translation_map = {}
        for dirname, _, filenames in walk("./translations/"):
            if dirname == "./translations/": continue
            filename = filenames[0] # There should be only 1
            with open (f"{dirname}/{filename}", "r") as f:
                json_data = load(f)
                translation_map[dirname.removeprefix("./translations/")] = json_data
        return translation_map
    def get_translation(language: str, message_code: str) -> str:
        translation_map = Translation._get_translation_map()
        try:
            return translation_map[language][message_code]
        except KeyError:
            try:
                return translation_map["en-US"][message_code] # Default to US
            except KeyError:
                return "No message available for this given message code"
if __name__ == "__main__":
    #Just some tests
    if Translation.get_translation("en-GB", "test") != "British!":
        print ("Test 1 failed")
        exit(1)
    if Translation.get_translation("thislanguage-doesnotexist", "test") != "Works!":
        print ("Test 2 failed")
        exit(1)
    if Translation.get_translation("en-US", "test") != "Works!":
        print ("Test 3 failed")
        exit(1)
    if Translation.get_translation("en-US", "thisdoesnotexist") != "No message available for this given message code":
        print ("Test 4 failed")
        exit(1)
    print ("All tests passed!")