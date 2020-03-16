#!/usr/bin/env python3
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    #Connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=postgres\
                            password=admin")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    #create sparkify database with UTF8 enconding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb TEMPLATE\
                template0")
    
    #Close connection to the default database with UTF8 enconding
    conn.close()
    
    #Connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres\
                            password=admin")
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Runs all the create table queries definied in sql_queries.py
    :param cur: cursor to the database
    :param conn: database connection reference
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
        
        
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
        
        
def main():
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    print("Table dropped successfully!")
    
    create_tables(cur, conn)
    print("Table created succesfully!")
    
    
if __name__ == '__main__':
    main()