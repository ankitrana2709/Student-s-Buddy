from app import db
Chours = db.execute("SELECT COUNT(hours) FROM logbook WHERE user_id = 3")[0]["COUNT(hours)"]
print(Chours)