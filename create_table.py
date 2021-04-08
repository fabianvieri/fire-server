import sqlite3

conn = sqlite3.connect("sfh.sqlite");

cursor = conn.cursor();

query = """CREATE TABLE user (
    id integer PRIMARY KEY,
    name text,
    address text,
    phone text
)
"""
cursor.execute(query)

query = """CREATE TABLE notification (
    id integer PRIMARY KEY,
    date text,
    base64_image text,
    status text,
    user_id integer,
    FOREIGN KEY (user_id) REFERENCES user (id)
)
"""
cursor.execute(query)

query = """CREATE TABLE camera (
    id integer,
    date text,
    base64_image text,
    user_id integer,
    status integer,
    PRIMARY KEY (id, user_id),
    FOREIGN KEY (user_id) REFERENCES user (id)
)
"""
cursor.execute(query)

conn.commit()
conn.close()
print("Table Created Successfully")