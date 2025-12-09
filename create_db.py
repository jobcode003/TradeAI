import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Try connecting to default postgres database
        # We try a few common configurations
        configs = [
            {"user": "postgres", "host": "localhost", "password": "Jobuser123!"},
           {"user": "job", "host": "localhost"}, # Current user
        ]
        
        conn = None
        for config in configs:
            try:
                print(f"Trying connection with: {config}")
                conn = psycopg2.connect(dbname="postgres", **config)
                print("Connected successfully!")
                break
            except Exception as e:
                print(f"Failed: {e}")
        
        if conn:
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            
            # Check if db exists
            cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'tradeai_db'")
            exists = cur.fetchone()
            
            if not exists:
                print("Creating database tradeai_db...")
                cur.execute("CREATE DATABASE tradeai_db")
                print("Database created successfully.")
            else:
                print("Database tradeai_db already exists.")
                
            cur.close()
            conn.close()
        else:
            print("Could not connect to Postgres to create database.")
            
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == "__main__":
    create_database()
