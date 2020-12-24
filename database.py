import os
import psycopg2
import time


def database_create_person():
    #DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    DATABASE_URL = os.environ['DATABASE_URL']
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

    # return message


def line_insert_record(record_list):
    #DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    table_columns = '(name, birthday , first_solo_album, fav_song)'
    postgres_insert_query = f"""INSERT INTO person {table_columns} VALUES (%s,%s,%s,%s)"""

    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    print("insert finish")

    cursor.close()
    conn.close()


def database_select():
    #DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    postgres_select_query = f"""SELECT * FROM person"""
    cursor.execute(postgres_select_query)

    cursor.close()
    conn.close()

def database_list(text):

    #DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    if text.lower() == "list":
        postgres_select_query = f"""SELECT * FROM person"""

    cursor.execute(postgres_select_query)
    #message = f"恭喜您！ {cursor.fetchall()} "
    #print(message)

    result = cursor.fetchall()
    message = ""
    for row in result:
        message =message+"name = " + row[1] + "生日  = "+str(row[2])+"第一張solo = "+row[3]+"我的最愛 = "+ row[4]+"\n"
    cursor.close()
    conn.close()

    return message

def deleteData(text):
    #DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a f64061070').read()[:-1]
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    if "name" in text:
        sql_delete_query = """Delete from person where name = %s"""
    elif "birthday" in text:
        sql_delete_query = """Delete from person where birthday = %s"""
    elif "first_solo_album" in text:
        sql_delete_query = """Delete from person where  first_solo_album = %s"""
    elif "fav_song" in text:
        sql_delete_query = """Delete from person where birthday = %s"""
    # Update single record now

    text_input = text.split(' ')
    cursor.execute(sql_delete_query, (text_input[1],))

    conn.commit()
    cursor.close()
    conn.close()

