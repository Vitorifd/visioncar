import sqlite3
import datetime


class Database:
	conn = sqlite3.connect('logs.db')
	cursor = conn.cursor()

    def insertLog(self, entry_time, departure_time, car_plate, send_status):
        self.cursor.execute("""
			INSERT INTO logs(entry_time, departure_time, car_plate, send_status) VALUES(?, ?, ?, ?);
		""", entry_time, departure_time, car_plate, send_status)
        return self.cursor.lastrowid

    def getLogs(self):
        self.cursor.execute("""
			SELECT * FROM logs;
		""")

    def getLogById(self, logId):
        self.cursor.execute("""
      		SELECT * FROM logs WHERE id=?;
    	""", (logId))
        return self.cursor.fetchAll()

    def getLogByCarPlate(self, car_plate):
        self.cursor.execute("""
      		SELECT * FROM logs WHERE car_plate=? AND departure_time IN NULL;
    	""", (car_plate))
        return self.cursor.fetchAll()

    def updateDepartureTime(self, logId, departure_time):
        self.cursor.execute("""
      		UPDATE logs SET departure_time=? WHERE id=?;
    	""", (departure_time, logId))

    def updateSendStatus(self, logId, send_status):
        self.cursor.execute("""
      		UPDATE logs SET send_status=? WHERE id=?;
    	""", (send_status, logId))


db = Database

print(db.insertLog( datetime.datetime.now(), None, 'ABC1234', False ))

conn.close()
