from app import db
Fhours = db.execute("SELECT SUM(hours) FROM logbook WHERE user_id = 3 ")[0]["SUM(hours)"]
Chours = db.execute("SELECT COUNT(hours) FROM logbook WHERE user_id = 3 ")[0]["COUNT(hours)"]
Avg = Fhours / Chours
list = [Fhours, Chours, Avg]
print(Fhours,
Chours,
Avg,
list)
username = db.execute("SELECT username FROM students WHERE id = 3")[0]["username"]
username = [username]
print(username)