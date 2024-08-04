import os
import psycopg2
import requests
import pandas as pd

def insert_row_schedule(dtime : str, host_name : str, guest_name : str):
    """
    Returns query (as string) that inputs given arguments to schedule table.
    """

    query_text = f"""
    INSERT INTO schedule (match_begin_time, host_name, guest_name)
    VALUES('{dtime}', '{host_name}', '{guest_name}');
    """

    return query_text


def main():
    print(f"Attempting to connect to database:")
    print(f"Host: {os.getenv('DATABASE_HOST')}")
    print(f"Port: {os.getenv('DATABASE_PORT')}")
    print(f"Database: {os.getenv('DATABASE_NAME')}")
    print(f"User: {os.getenv('DATABASE_USER')}")

    conn = psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT")
    )
    cur = conn.cursor()
    cur.execute('SELECT version();')
    db_version = cur.fetchone()
    print(f"Connected to PostgreSQL database! Version: {db_version[0]}")

    cur.execute(insert_row_schedule('2024-06-16 15:00:00', 'POLSKA', 'HOLANDIA'))
    cur.execute(insert_row_schedule('2024-06-21 18:00:00', 'POLSKA', 'AUSTRIA'))
    cur.execute(insert_row_schedule('2024-06-25 18:00:00', 'FRANCJA', 'POLSKA'))
    conn.commit()
    

    print("Printing schedule table from postgresql db:")
    print(pd.read_sql("SELECT * FROM schedule",conn))
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
