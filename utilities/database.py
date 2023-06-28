from utilities.data import get_data
from mysql import connector as mysql


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


async def selector(query: str, variables: list):
    """
    This function is used to select data from the database. It is used for SELECT queries.
    :param query: The query to execute. Use %s for variables. Example: "SELECT * FROM table WHERE column = %s"
    :param variables: The variables to use in the query. If there are no variables, use an empty list.
    :return: The result of the query. If there is no result, it will return False.
    """
    cursor = await mysql_login()
    db = cursor.cursor()
    db.execute(query, variables)
    try:
        result = db.fetchall()[0]
    except IndexError:
        return False
    db.close()
    cursor.close()
    return result


async def modifyData(query: str, variables: list) -> None:
    """
    This function is used to modify data in the database. It is used for INSERT, UPDATE, and DELETE queries.
    :param query: The query to execute. Use %s for variables. Example: "INSERT INTO table (column) VALUES (%s)"
    :param variables: The variables to use in the query. If there are no variables, use an empty list.
    :return: None
     """
    cursor = await mysql_login()
    db = cursor.cursor()
    db.execute(query, variables)
    cursor.commit()
    db.close()
    cursor.close()
