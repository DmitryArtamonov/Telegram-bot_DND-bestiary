import psycopg2
from log import log

def database_connection(query):
    # connect to the DATABASE
    connection = None
    try:
        connection = psycopg2.connect(
            database="DnD_Bestiary_bot",
            user='postgres',
            password='123',
            host='localhost',
            port='5432'
        )

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                try:
                    result = cursor.fetchall()
                    return result
                except:
                    return None

    except Exception as e:
        log.add(f'DataBase ERROR: {e}', f'Query: {query}')
        return('ERROR')

    finally:
        if connection is not None:
            connection.close()

def add_to_db(user, type, message):
    query = f'SELECT user_id FROM users WHERE user_id = {user.id}'
    res = database_connection(query)
    if not res: # if user not in database -> add user
        query = f"""INSERT INTO users (user_id, first_name, last_name, username)
        VALUES ({user.id}, '{user.first_name}', '{user.last_name}', '{user.username}')"""
        res = database_connection(query)
        if res != 'ERROR':
            log.add(f'user {user.id} added to database')

    query = f"INSERT INTO queries (user_id, type, message) VALUES ({user.id}, '{type}', '{message}')"
    res = database_connection(query)
    if res != 'ERROR':
        log.add(f'query from user {user.id} added to database')






