# import quizmgmt
# import os
# import sqlite3 as db
#
#
#
# def auth(conn):
#     cur = conn.cursor()
#     un = input("enter username")
#     pwd = input("enter password")
#     authquery = f"select username,role from login where username=' {un}' and password='{pwd}' and"
#     cur.execute(authquery)
#     rs=cur.fetchone()
#     print(rs)
#     if(rs==None):
#         print("invalid username or password")
#     else:
#         print(f"welcome {rs[0]}")
#         manageAdmin(conn,rs[0])
#
#     cur.close()
#
# def manageAdmin(conn,username):
#     while True:
#         choice=int(input("""Main Menu
#         1)Login
#         2)create new user
#         3)change passaword
#         4)Exist
#         """))
#         if(choice==1):
#             quizmgmt.quizMgmt(conn)
#         elif choice==2:
#             createNewAdmin(conn)
#         elif choice==3:
#             changePassword(conn,username)
#         elif choice==4:
#             break
#         else:
#             print("invalid choice")
#
# def createNewAdmin(conn):
#     cur=conn.cursor()
#     un=input("enter username")
#     pwd=input("enter password")
#
#
#
#
#
#
#
#
#

import os
import sqlite3 as db
import quizmgmt  # Make sure you have a `quizmgmt.py` with quizMgmt(conn) function


def auth(conn):
    cur = conn.cursor()
    un = input("Enter username: ")
    pwd = input("Enter password: ")

    authquery = "SELECT username, role FROM login WHERE username = ? AND password = ?"
    cur.execute(authquery, (un, pwd))
    rs = cur.fetchone()

    if rs is None:
        print("Invalid username or password")
    else:
        print(f"Welcome {rs[0]} ({rs[1]})")
        manageAdmin(conn, rs[0])

    cur.close()


def manageAdmin(conn, username):
    while True:
        choice = int(input("""
Main Menu
1) Start Quiz
2) Create New User
3) Change Password
4) Exit
Enter choice: """))
        if choice == 1:
            quizmgmt.quizMgmt(conn)  # This function must be defined in quizmgmt.py
        elif choice == 2:
            createNewAdmin(conn)
        elif choice == 3:
            changePassword(conn, username)
        elif choice == 4:
            break
        else:
            print("Invalid choice")


def createNewAdmin(conn):
    cur = conn.cursor()
    un = input("Enter new username: ")
    pwd = input("Enter new password: ")
    role = input("Enter role (admin/user): ")

    # Check if username already exists
    cur.execute("SELECT * FROM login WHERE username = ?", (un,))
    if cur.fetchone():
        print("Username already exists.")
    else:
        cur.execute("INSERT INTO login (username, password, role) VALUES (?, ?, ?)", (un, pwd, role))
        conn.commit()
        print("New user created successfully.")

    cur.close()


def changePassword(conn, username):
    cur = conn.cursor()
    old_pwd = input("Enter current password: ")
    new_pwd = input("Enter new password: ")

    # Verify current password
    cur.execute("SELECT * FROM login WHERE username = ? AND password = ?", (username, old_pwd))
    if cur.fetchone():
        cur.execute("UPDATE login SET password = ? WHERE username = ?", (new_pwd, username))
        conn.commit()
        print("Password changed successfully.")
    else:
        print("Incorrect current password.")

    cur.close()


# Entry point for the app
if __name__ == "__main__":
    conn = db.connect("quiz.db")  # Update with your actual database path if different
    auth(conn)
    conn.close()
