import sqlite3

con = sqlite3.connect("tasks.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN NOT NULL)")
res = cur.execute("SELECT COUNT(*) FROM tasks")
conteo = res.fetchone()[0]

if conteo == 0:
    cur.execute("INSERT INTO tasks (title, done) VALUES (\"Play LMU on the sim\", 0)")
    cur.execute("INSERT INTO tasks (title, done) VALUES (\"Go to the gym\", 0)")
    cur.execute("INSERT INTO tasks (title, done) VALUES (\"Walk the dog\", 0)")
    con.commit()
    print("3 tasks created.")
else:
    print(f"The database already contains {conteo} tasks. Insertion was omitted.")

res = cur.execute("SELECT id, title, done from tasks")
print(res.fetchall())

con.close()