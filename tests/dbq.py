import pymysql

#Establish connection to the production database

connection_one = pymysql.connect(host='localhost', port=3306, user='root', passwd='1Gia2Harley',
 db='blockchain', autocommit = True)


#Create cursors to interact with the databases
cur_1 = connection_one.cursor()


cur_1.execute("INSERT INTO PRE_FLOP_TBL VALUES ('%s', '%s')"%(float(botoplist[-1])*.01,  float(botopgroups[-1])*.01))
