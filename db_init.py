import psycopg2
import os


def connection():
    conn = psycopg2.connect(database="store", user="postgres", password="123", host="127.0.0.1", port="5432")
    # DATABASE_URL = os.environ['DATABASE_URL']
    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    return conn


def create_tables():
    conn = connection()
    cur = conn.cursor()
    list_of_tables = tables()

    for table in list_of_tables:
        cur.execute(table)
        conn.commit()


def tables():
    product = """CREATE TABLE IF NOT EXISTS products(
            ID  SERIAL PRIMARY KEY,
            product_name varchar(1000) NOT NULL UNIQUE,
            category varchar(100) NOT NULL,
            quantity numeric NOT NULL,
            price  numeric NOT NULL,
            date_created  DATE

    )"""
    sales = """CREATE TABLE IF NOT EXISTS sales(
            ID  SERIAL PRIMARY KEY,
            username varchar(100) NOT NULL,
            product_id varchar(100) NOT NULL,
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
    table_list = [product, sales, users, blacklist, categories]

    return table_list


def tables_to_drop():
    db1 = """DROP TABLE IF EXISTS products CASCADE"""
    db2 = """DROP TABLE IF EXISTS sales CASCADE"""
    table_list = [db1, db2]
    return table_list


def drop_tables():
    conn = connection()
    cur = conn.cursor()
    drop_table = tables_to_drop()
    for table in drop_table:
        cur.execute(table)
        conn.commit()


def delete_record(email):
    query = "DELETE FROM users WHERE email = '{0}'".format(email)
    conn = connection()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()


def delete_category():
    query = "DROP TABLE IF EXISTS categories CASCADE"
    conn = connection()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
