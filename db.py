import sqlite3

db = sqlite3.connect('bot.db')
cursor = db.cursor()

class Database:

    async def guild_write(self):
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            member_id INTEGER,
                            balance BIGINT NOT NULL DEFAULT 1000,
                            xp BIGINT NOT NULL DEFAULT 0,
                            lvl INT NOT NULL DEFAULT 1
                        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS warn(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            member_id INTEGER,
                            warn INTEGER DEFAULT 0,
                            reason TEXT
                        )""")
    
    
    async def insert_new_member(self, member,table):
        cursor.execute(f"SELECT * FROM {table} WHERE member_id = ?", [member.id])
        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO {table} (member_id) VALUES (?)", [member.id])
        db.commit()
    
    async def update_member(self, query, values: list):
            await cursor.execute(query, values)
            await db.commit()
        
    
        