import sqlite3
from datetime import datetime, timedelta

class pricesDB:
    def __init__(self, path, table):
        self.path=path
        self.table=table
        if not(self.checkIfTable()):
            self.createTable()


    
    def checkIfTable(self):
        self.start()
        self.c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table}';")
        rows=self.c.fetchall()
        result=len(rows)>0
        self.end()
        return result
    
    def createTable(self):
        self.start()
        self.c.execute("""
                CREATE TABLE main (
                timestamp INTEGER UNIQUE,
                date TEXT,
                time TEXT,
                price REAL
            )""")
        self.conn.commit()
        self.end()

    def start(self):
        self.conn=sqlite3.connect(self.path)
        self.c=self.conn.cursor()
    def end(self):
        self.conn.close()
    def add(self,timestamp,date,time,price):
        self.start()
        try:
            self.c.execute(f"INSERT INTO {self.table} VALUES ({timestamp},'{date}','{time}',{price})")
            self.conn.commit()
            success=True
        except sqlite3.IntegrityError:
            success=False        
        self.end()
        return success
    def deleteAll(self):
        self.start()
        self.c.execute(f"DELETE FROM {self.table};")
        self.conn.commit()
        self.end()
    def deleteOld(self,hours_old=48):
        unix_treshold=(datetime.now()-timedelta(hours=hours_old)).timestamp()
        self.start()
        self.c.execute(f"DELETE FROM {self.table} WHERE timestamp<{unix_treshold};")
        self.conn.commit()
        self.end()
    def getFuture(self,fields=["timestamp","price","time"]):
        time_now=(datetime.now()-timedelta(hours=1)).timestamp()
        field_string=','.join(tuple(fields))

        self.start()
        self.c.execute(f"SELECT {field_string} FROM {self.table} WHERE timestamp>{time_now};")
        rows = self.c.fetchall()
        self.end()

        return [dict(zip(fields,r)) for r in rows]

    def getFarTime(self):
        self.start()
        self.c.execute(f"SELECT MAX(timestamp) FROM {self.table};")
        rows = self.c.fetchall()
        self.end()        
        return rows[0][0]
