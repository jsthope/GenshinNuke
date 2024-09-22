from requests import get
import sqlite3

def insert_weapon(conn, name,t,data):
    print('insert:',name)
    sql = '''INSERT INTO base_weapon(name,type,data)
             VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (name,t,data))
    conn.commit()
    return cur.lastrowid

weapons = get("https://genshin-db-api.vercel.app/api/v5/weapons?query=names&matchCategories=true").json()

with sqlite3.connect('db.sqlite3') as conn:
    conn.execute("DELETE FROM `base_weapon`")
    
    for weapon in weapons:
        r = get(f"https://genshin-db-api.vercel.app/api/v5/weapons?query={weapon}")
        insert_weapon(conn,weapon,r.json()['weaponType'],r.text)

