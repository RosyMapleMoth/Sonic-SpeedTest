import json
import os
import psycopg2
import uuid

with open("secreats.json") as f:
    secrets_json = json.load(f)
    conn = psycopg2.connect(
        host=secrets_json["database_host"],
        database=secrets_json["database_name"],
        user=secrets_json["database_user"],
        password=secrets_json["database_password"])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
# TODO change contact_id's name to api_key
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                 'name varchar (35) NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP,'
                                 'discord_at text NOT NULL,'
                                 'contact_id uuid DEFAULT gen_random_uuid())'
                                 )


cur.execute('DROP TABLE IF EXISTS sessions;')
cur.execute('CREATE TABLE sessions (id serial PRIMARY KEY,'
                                 'user_id INT NOT NULL,'
                                 'image_One TEXT,'
                                 'image_Two TEXT,'
                                 'image_Three TEXT,'
                                 'speed integer NOT NULL,'
                                 'date_added timestamp DEFAULT CURRENT_TIMESTAMP)'
                                 )
# Insert data into the table


conn.commit()

cur.close()
conn.close()

