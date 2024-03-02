import sqlite3

con = sqlite3.connect("rooms.db")

ROOMS = "CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, name TEXT)"


def create_schema():
    curr = con.cursor()
    curr.execute(ROOMS)
    con.commit()

def create_room(room_id: int):
    try:
        data = (room_id, "testName")
        curr = con.cursor()
        curr.execute("INSERT INTO rooms VALUES (?, ?)", data)
        con.commit()
        print(f"Room {room_id} created successfully")
    except Exception as e:
        print(f"Error creating room: {e}")

