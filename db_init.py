import psycopg2
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
            description varchar(1000) NOT NULL,
            quantity numeric NOT NULL,
            price  numeric NOT NULL,
            date_created  DATE

    )"""
    # sales = """CREATE TABLE IF NOT EXISTS sales(
    #         sale_id serial PRIMARY NOT NULL,
    #         attendant_name VARCHAR(100) NOT NULL,
    #         product_name VARCHAR(1000) NOT NULL,
    #         quantity numeric NOT NULL,
    #         price  numeric NOT NULL,
    #         total_price  numeric NOT NULL,
    #         date_created current_timestamp
    # )"""
    users = """CREATE TABLE IF NOT EXISTS users(
             ID  SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL UNIQUE,
            role VARCHAR(20) NOT NULL,
            password VARCHAR(500) NOT NULL,
            date_created  DATE
    )"""
    table_list = [product, users]

    return table_list
