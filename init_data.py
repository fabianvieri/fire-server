import sqlite3

conn = sqlite3.connect("sfh.sqlite");

cursor = conn.cursor();
query = "INSERT INTO user (name, address, phone) VALUES ('test_name', 'jalan 123 no.4', '081234567890')"
cursor.execute(query)
query = "INSERT INTO image (date, base64_image, user_id, status) VALUES ('2021-03-21 11:27:45', 'test_image', 1, 0)"
cursor.execute(query)

conn.commit()
conn.close()
print("Data Inserted Successfully")