from database import Database


db = Database()
db.connect()

categories = db.fetch_all(
    "SELECT * FROM categories"
)

for category in categories:
    print(category)

db.close()