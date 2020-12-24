import os
import psycopg2


def database_creat_person():
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    create_table_query = '''CREATE TABLE IF NOT EXISTS person(
        record_num serial PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        birthday DATE NOT NULL,
        first_solo_album VARCHAR (50) NOT NULL,
        fav_song VARCHAR (50) NOT NULL,
    );'''

    cursor.execute(create_table_query)
    conn.commit()

    cursor.close()
    conn.close()

    # return message


def line_insert_record(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    table_columns = '(name, birthday , first_solo_album, fav_song)'
    postgres_insert_query = f"""INSERT INTO person {table_columns} VALUES (%s,%s,%s,%s)"""

    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    print(f"insert finish")

    cursor.close()
    conn.close()

    # return message
