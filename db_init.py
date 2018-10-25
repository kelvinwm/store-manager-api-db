import psycopg2
import sys
import os


# db_url = os.getenv(url)

def connection():
    # url = ""nlknl""
    conn = psycopg2.connect(database="store", user="postgres", password="123", host="127.0.0.1", port="5432")

    return conn


def create_tables():
    conn = connection()
    cur = conn.cursor()
    list_of_tables = tables()

    for table in list_of_tables:
        cur.execute(table)
    conn.commit()
    conn.close()


def tables():
    product = """CREATE TABLE IF NOT EXISTS products(
            ID  SERIAL PRIMARY KEY,
            product_name varchar(1000) NOT NULL UNIQUE,
            category varchar(100) NOT NULL,
            quantity numeric NOT NULL,
            price  numeric NOT NULL,
            date_created  DATE

    )"""
    users = """CREATE TABLE IF NOT EXISTS users(
             ID  SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL UNIQUE,
            role VARCHAR(20) NOT NULL,
            password VARCHAR(500) NOT NULL,
            date_created  DATE
    )"""
    blacklist = """CREATE TABLE IF NOT EXISTS blacklists(
             ID  SERIAL PRIMARY KEY,
             token VARCHAR(500) NOT NULL,
             date_created  DATE
    )"""
    categories = """CREATE TABLE IF NOT EXISTS categories(
             ID  SERIAL PRIMARY KEY,
             category VARCHAR(50) NOT NULL UNIQUE,
             date_created  DATE
    )"""
    table_list = [product, users, blacklist, categories]

    return table_list


def drop():
    db1 = """DROP TABLE IF EXISTS products CASCADE"""
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(db1)

        cur.close()
        cur.commit()
    except psycopg2.Error:
        raise SystemExit("Failed {}".format(sys.exc_info()))
