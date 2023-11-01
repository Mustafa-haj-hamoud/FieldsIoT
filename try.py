from cs50 import SQL



db = SQL("mysql://sql11654668:hdyALlvutz@sql11.freemysqlhosting.net:3306/sql11654668")


db.execute("CREATE TABLE users ( id INTEGER PRIMARY KEY AUTO_INCREMENT,firstname TEXT,lastname TEXT,username TEXT, hash TEXT)")

db.execute("CREATE TABLE fields ( id INTEGER PRIMARY KEY AUTO_INCREMENT, user_id INTEGER, field_name TEXT, value INTEGER,FOREIGN KEY (user_id) REFERENCES users(id) );")
