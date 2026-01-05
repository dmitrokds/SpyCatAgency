import aiosqlite
import config

async def create():
    async with aiosqlite.connect(config.DB_URL) as db:
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS spy_cats (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                years_of_exp INT NOT NULL,
                breed VARCHAR(200) NOT NULL,
                salary INT NOT NULL
            );'''
        )
        
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS missions (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                complete BOOLEAN NOT NULL DEFAULT 0,
                cat_id INT,
                FOREIGN KEY (cat_id) REFERENCES spy_cats(id) ON DELETE CASCADE
            );'''
        )
        
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS targets (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                country VARCHAR(200) NOT NULL,
                notes VARCHAR,
                complete BOOLEAN NOT NULL DEFAULT 0,
                mission_id INT,
                FOREIGN KEY (mission_id) REFERENCES missions(id) ON DELETE CASCADE
            );'''
        )
        await db.commit()
        
        
async def update(query):
    async with aiosqlite.connect(config.DB_URL) as db:
        cursor = await db.execute(query)
        
        await db.commit()
        
        id = cursor.lastrowid
        await cursor.close()
        
    return id


async def select(query):
    async with aiosqlite.connect(config.DB_URL) as db:
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            
    return rows
        