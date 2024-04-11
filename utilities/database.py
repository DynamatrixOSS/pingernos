from mysql import connector as mysql
from utilities.data import get_data


async def mysql_login():
    """
    This function is used to log in to the database.
    :return: The cursor to use for queries.
    """
    database = get_data()['Database']

    return mysql.connect(
        host=database['Host'],
        user=database['User'],
        password=database['Password'],
        database=database['Database'])


async def selector(query: str, variables: list) -> tuple:
    """
    This function is used to select data from the database. It is used for SELECT queries.
    :param query: The query to execute. Use %s for variables. Example: "SELECT * FROM table WHERE column = %s"
    :param variables: The variables to use in the query. If there are no variables, use an empty list.
    :return: The result of the query. If there is no result, it will return False.
    """
    cursor = await mysql_login()
    database = cursor.cursor()
    database.execute(query, variables)
    try:
        result = database.fetchall()[0]
    except IndexError:
        return ()
    database.close()
    cursor.close()
    return result


async def modifier(query: str, variables: list) -> None:
    """
    This function is used to modify data in the database. It is used for INSERT, UPDATE, and DELETE queries.
    :param query: The query to execute. Use %s for variables. Example: "INSERT INTO table (column) VALUES (%s)"
    :param variables: The variables to use in the query. If there are no variables, use an empty list.
    :return: None
     """
    cursor = await mysql_login()
    database = cursor.cursor()
    database.execute(query, variables)
    cursor.commit()
    database.close()
    cursor.close()
