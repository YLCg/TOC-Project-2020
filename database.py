import os
import psycopg2

def database_create_person():
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    #DATABASE_URL = os.environ['DATABASE_URL']
    print("in")

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    create_table_query = '''CREATE TABLE IF NOT EXISTS person(
            record_num serial PRIMARY KEY,
            name VARCHAR (50) NOT NULL,
            birthday DATE NOT NULL,
            first_solo_album VARCHAR (50) NOT NULL,
            fav_song VARCHAR (50) NOT NULL
            );'''

    cursor.execute(create_table_query)
    conn.commit()

    cursor.close()
    conn.close()


def line_insert_record(record_list):
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    #DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    table_columns = '( name, birthday , first_solo_album, fav_song)'
    postgres_insert_query = f"""INSERT INTO person {table_columns} VALUES (%s,%s,%s,%s)"""

    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    print("insert finish")

    cursor.close()
    conn.close()


def database_select():
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    #DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    postgres_select_query = f"""SELECT * FROM person"""
    cursor.execute(postgres_select_query)

    cursor.close()
    conn.close()

def database_list(text):

    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    #DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    if text.lower() == "list":
        postgres_select_query = f"""SELECT * FROM person"""
    else:
        postgres_select_query = f"""SELECT {text} FROM person"""
    cursor.execute(postgres_select_query)

    result = cursor.fetchall()
    message = "list:\n"
    for row in result:
        message = message + "id = " + str(row[0])+"/" + row[1] + "/" + str(row[2]) + "/" + row[3] + "/" + row[4]+"\n"


    cursor.close()
    conn.close()

    return message


def deleteData(text):
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    #DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    text_input = text.split(' ')
    #table_columns = '' + text_input[0]

    sql_delete_query = f"""Delete from person WHERE {text_input[0]} = %s"""

    cursor.execute(sql_delete_query, (text_input[1],))

    conn.commit()
    cursor.close()
    conn.close()


def updateData(text_set, text_con):

    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    #DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_update_query = f"""UPDATE person SET {text_set}  WHERE {text_con}"""
    cursor.execute(postgres_update_query)

    conn.commit()

    print("update finish")

    cursor.close()
    conn.close()
