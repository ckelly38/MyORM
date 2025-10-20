import sqlite3;
#WILL PROBABLY NEED OTHER DATABASE LIBRARY IMPORTS HERE. MAY WANT TO CONDITIONALLY IMPORT THEM.

#GS: Python how to connect to an external database like sql server
#https://www.youtube.com/watch?v=Y1OFbez9qK0
#https://www.youtube.com/watch?v=g69lFxZdcVQ
#GS: Python connect to mysql db example
#https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
#https://www.geeksforgeeks.org/how-to-connect-python-with-sql-database/
#GS: what python library can be used for connecting to any database
#GS: how to connect python to postgresql
#https://www.geeksforgeeks.org/postgresql-connecting-to-the-database-using-python/
#https://stackoverflow.com/questions/26496388/how-to-connect-python-to-postgresql
#For POSTGRESQL: I wrote a script to take the EXTERNAL DB URI and extract the needed connection params
#I can modify and or call that script here in this case and everything will be passed into the
#connection method
#My program currently does not do type enforcement for POSTGRESS, MONGODB, FIREBASE, and NOSQL.
#I probably will not use NO SQL at all because I have never used that before.
#SQLVARIANT = "LITE";#LITE, MYSQL, SQLSERVER
#DB_NAME = "swimleague";#set by the user.
#CONN = sqlite3.connect(DB_NAME + '.db');
#CURSOR = CONN.cursor();#PRETTY MUCH EVERY LIBRARY OUT THERE HAS A METHOD FOR GETTING THIS.
#isinit = False;
#def isInitialized(self): return isinit;

from myorm import MyDB;
mydb = MyDB.MyDB.newDBFromNameAndLib("swimleague", sqlite3, "LITE");
print(f"mydb.SQLVARIANT = {mydb.SQLVARIANT}");
