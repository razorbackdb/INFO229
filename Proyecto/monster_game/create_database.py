import mysql.connector
import os, time


def create_database(db_connection, db_name, cursor):
    cursor.execute(f"CREATE DATABASE {db_name};")
    cursor.execute(f"COMMIT;")
    cursor.execute(f"USE {db_name};")

    # Tabla news
    cursor.execute('''CREATE TABLE monsters (
		id_monster INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
		name VARCHAR(255),
		emoji VARCHAR(255),
		atk INT,
		def INT,
		hp INT,
        selected BOOL
		);''')
    
    cursor.execute('''CREATE TABLE battles (
		id_battle INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
		name VARCHAR(255),
		emoji VARCHAR(255),
		atk INT,
		def INT,
		hp INT,
        selected BOOL
		);''')

    cursor.execute("SET GLOBAL time_zone = 'UTC';")
    cursor.execute("SET SESSION time_zone = 'UTC';")

    cursor.execute("COMMIT;")


def insert_data(cursor):
    print("insert")
    cursor.execute('''INSERT INTO monsters (name, emoji, atk, def, hp, selected) VALUES
    ("Dragon",":dragon:", 100, 25, 500, 0);
    ''')
    cursor.execute("COMMIT;")
    cursor.execute('''INSERT INTO monsters (name, emoji, atk, def, hp, selected) VALUES
    ("Worm",":worm:", 10, 50, 100, 0);
    ''')
    cursor.execute("COMMIT;")
    cursor.execute('''INSERT INTO monsters (name, emoji, atk, def, hp, selected) VALUES
    ("Shark",":shark:", 50, 50, 250, 0);
    ''')
    cursor.execute("COMMIT;")
    cursor.execute('''INSERT INTO monsters (name, emoji, atk, def, hp, selected) VALUES
    ("Octopus",":octopus:", 25, 75, 300, 0);
    ''')
    cursor.execute("COMMIT;")


#######################


def main():
    print("start creating database...")

    DATABASE = "bot_game"

    DATABASE_IP = str(os.environ['DATABASE_IP'])

    DATABASE_USER = "root"
    DATABASE_USER_PASSWORD = "root"
    DATABASE_PORT = 3306

    not_connected = True

    while (not_connected):
        try:
            print(DATABASE_IP, "IP")
            db_connection = mysql.connector.connect(
                user=DATABASE_USER,
                host=DATABASE_IP,
                port=DATABASE_PORT,
                password=DATABASE_USER_PASSWORD)
            not_connected = False

        except Exception as e:
            time.sleep(3)
            print(e, "error!!!")
            print("can't connect to mysql server, might be intializing")

    cursor = db_connection.cursor()

    try:
        cursor.execute(f"USE {DATABASE}")
        print(f"Database: {DATABASE} already exists")
    except Exception as e:
        create_database(db_connection, DATABASE, cursor)
        insert_data(cursor)
        print(f"Succesfully created: {DATABASE}")
