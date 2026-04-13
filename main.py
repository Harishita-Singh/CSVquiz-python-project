
import sqlite3
import admin
import quiz
import leaderboard

def main():
    global conn
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("quiz.db")

        while True:
            try:
                choice = int(input("""
Main Menu
1) Admin Login
2) Play Quiz Game
3) Show Leaderboard
4) Exit
Enter your choice: """))

                if choice == 1:
                    admin.auth(conn)
                elif choice == 2:
                    quiz.quizGame(conn)
                elif choice == 3:
                    leaderboard.printLeaders(conn)
                elif choice == 4:
                    print("Exiting... Goodbye!")
                    break
                else:
                    print("Invalid choice. Please choose from 1 to 4.")
            except ValueError:
                print("Please enter a valid number.")

    except sqlite3.Error as e:
        print("Database error:", e)

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
