
import sqlite3
import csv
import os

# Ensure the table exists
def initializeDatabase(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            qno INTEGER PRIMARY KEY,
            ques TEXT,
            a TEXT,
            b TEXT,
            c TEXT,
            d TEXT,
            correct TEXT,
            hint TEXT,
            explanation TEXT
        )
    """)
    conn.commit()
    cur.close()

# Load questions from a CSV file
def loadQuestions(conn):
    cur = conn.cursor()
    filename = input("Enter filename (e.g., quiz.csv): ")

    if not os.path.exists(filename):
        print("File not found.")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 9:
                    cur.execute("""
                        INSERT OR REPLACE INTO questions 
                        (qno, ques, a, b, c, d, correct, hint, explanation)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, row)
                else:
                    print(f"Skipping invalid row: {row}")
        conn.commit()
        print("Questions loaded from CSV.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()

# View all questions
def showAllQuestions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    rows = cur.fetchall()
    for row in rows:
        print(f"\nQ{row[0]}: {row[1]}")
        print(f"a) {row[2]}  b) {row[3]}  c) {row[4]}  d) {row[5]}  [Ans: {row[6]}]")
        print(f"Hint: {row[7]}")
        print(f"Explanation: {row[8]}")
    cur.close()

# Delete a question by Qno
def deleteQuestion(conn):
    cur = conn.cursor()
    qnos = input("Enter Qno(s) to delete (comma-separated): ")
    try:
        qno_list = [int(q.strip()) for q in qnos.split(",") if q.strip().isdigit()]
        if not qno_list:
            print("No valid Qno provided.")
            return
        placeholders = ','.join('?' for _ in qno_list)
        cur.execute(f"DELETE FROM questions WHERE qno IN ({placeholders})", qno_list)
        conn.commit()
        print("Selected questions deleted.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()

# Add a new question
def addQuestion(conn):
    cur = conn.cursor()
    try:
        qno = int(input("Qno: "))
        ques = input("Question: ")
        a = input("Option A: ")
        b = input("Option B: ")
        c = input("Option C: ")
        d = input("Option D: ")
        correct = input("Correct (a/b/c/d): ").lower()
        hint = input("Hint: ")
        exp = input("Explanation: ")
        cur.execute("""
            INSERT OR REPLACE INTO questions 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (qno, ques, a, b, c, d, correct, hint, exp))
        conn.commit()
        print("Question added.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()

# Admin menu
def quizMgmt(conn):
    initializeDatabase(conn)
    while True:
        try:
            ch = int(input("""
            ===== Admin Menu =====
            1) Load from CSV
            2) Add Question
            3) Delete Question
            4) View All Questions
            5) Exit
            Your choice: """))
            if ch == 1:
                loadQuestions(conn)
            elif ch == 2:
                addQuestion(conn)
            elif ch == 3:
                deleteQuestion(conn)
            elif ch == 4:
                showAllQuestions(conn)
            elif ch == 5:
                print("Exiting...")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

        # Run the app
    if __name__ == "__main__":
        conn = sqlite3.connect("quiz.db")
        quizMgmt(conn)
        conn.close()

