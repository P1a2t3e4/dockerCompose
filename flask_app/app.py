from flask import Flask
import redis
import psycopg2
import os

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host="redis", port=6379)

# Connect to PostgreSQL
def get_postgres_connection():
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST')
    )

@app.route("/")
def home():
    # Redis logic: increment page visit count
    count = r.incr("hits")
    
    # PostgreSQL logic: fetch PostgreSQL version
    conn = get_postgres_connection()
    cur = conn.cursor()
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    cur.close()
    conn.close()

    return f"This page has been visited {count} times. PostgreSQL version: {db_version[0]}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
