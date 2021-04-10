import sqlite3

conn = sqlite3.connect("sfh.sqlite");

cursor = conn.cursor();
query = "INSERT INTO user (name, address, phone) VALUES ('test_name', 'jalan 123 no.4', '081234567890')"
cursor.execute(query)
query = "INSERT INTO camera (id, date, base64_image, user_id, status) VALUES (1, '2021-03-21 11:27:45', 'test_image', 1, 0)"
cursor.execute(query)
query = "INSERT INTO firefighter (name, phone, address) VALUES ('Dinas Pemadam Kebakaran DKI Jakarta', '021-63858213', 'Jl. K.H.Zainul Arifin No.71')"
cursor.execute(query)

conn.commit()
conn.close()
print("Data Inserted Successfully")