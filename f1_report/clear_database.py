from create_db import BestTable, InvalidTable, db

db.close()

db.connect()

BestTable.delete().execute()
InvalidTable.delete().execute()

db.close()
