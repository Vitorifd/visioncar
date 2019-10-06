import sqlite3

conn = sqlite3.connect('logs.db')
cursor = conn.cursor()

cursor.execute("""
  CREATE TABLE logs(
    id INT AUTO_INCREMENT,
    car_plate VARCHAR(10) NOT NULL,
    entry_time DATETIME NOT NULL,
    departure_time DATETIME,
    send_status BOOLEAN DEFAULT 0,
    PRIMARY KEY(id)
  );
""")