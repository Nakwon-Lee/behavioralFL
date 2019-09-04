import sqlite3

LOG_LENGTH = 38

cnt = sqlite3.connect('./tmp/mylogs.db')
cur = cnt.cursor()

querystr = ''

querystr += 'CREATE TABLE behavlog ('

for i in range(LOG_LENGTH):
    querystr = querystr + 'v' + str(i) + ' INTEGER, '

querystr += 'sflabel INTEGER)'

print(querystr)

cur.execute(querystr)
