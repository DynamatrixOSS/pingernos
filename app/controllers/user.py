from database.executioners.database import execute


class User:
    @staticmethod
    async def get_user(user):
        res = (await execute('SELECT * FROM user_settings WHERE user_id = %s', user.id))[0]
        if res:
            language = res['language']
            res['language'] = language.upper() + f' :flag_{language if language != 'en' else 'us'}:'

            filter_fields = ['user_id', 'name']
            for field in filter_fields:
                res.pop(field)
            return res

        return False
