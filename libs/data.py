import sqlite3
import datetime

class Database:
    
    def __init__(self) -> None:
        self.con = sqlite3.connect('data/data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.cur = self.con.cursor()

    def setTables(self):
        self.cur.execute("CREATE TABLE users(user_id VARCHAR(100), tea_key VARCHAR(100), tachi_key VARCHAR(100))")
        self.cur.execute("CREATE TABLE logs(user_id VARCHAR(100), date_tentative TIMESTAMP, status VARCHAR(100))")
        self.con.commit()
    
    def register(self, user_id, tea_key, tachi_key):
        if self.cur.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'").fetchone() is None:
            self.cur.execute(f"""
                INSERT INTO users VALUES
                    ('{user_id}', '{tea_key}', '{tachi_key}')
                """)
            self.con.commit()
            return 'REGISTRATION_DONE'
        else:
            return 'USER_ALREADY_BINDED'
        
    def getUserData(self, user_id):
        res = self.cur.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
        return res.fetchone()
    
    def insertLog(self, user_id, status):
        self.cur.execute(f"""
            INSERT INTO logs VALUES
                ('{user_id}', '{datetime.datetime.now()}', '{status}')
            """)
        self.con.commit()
        
    def getLogs(self, user_id):
        res = self.cur.execute(f"SELECT date_tentative, status FROM logs WHERE user_id = '{user_id}' ORDER BY date_tentative DESC")
        return res.fetchall()
    
    def cleanupLogs(self, user_id):
        self.cur.execute(f"DELETE * FROM logs WHERE user_id = '{user_id}'")
        self.con.commit()
    
    def close(self):
        self.cur.close()
        self.con.close()