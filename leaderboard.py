def printLeaders(conn):
    cur=conn.cursor()
    qry="select * from leaderboard order by percentage desc"
    cur.execute(qry)
    rs=cur.fetchall()
    print(f"{'name':<10} {'score':<6} {'limit':<6} {'percentage':<6}")
    for i in rs:
        print(f"""{i[0]:<10} {i[1]:<6} {i[2]:<6} {i[3]:<6}""")
    cur.close()
